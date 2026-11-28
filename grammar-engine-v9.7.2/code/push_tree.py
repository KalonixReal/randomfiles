#!/usr/bin/env python3
"""Push the staged bundle tree to GitHub as grammar-engine-v9.7.1/ + READMEs,
then create release v9.7.1-bundle with the zip asset.

Git data API path: blobs -> tree (base_tree=main) -> commit -> ref.
Usage: python3 push_tree.py <TOKEN>
"""
import base64
import hashlib
import json
import os
import sys
import time

import urllib.request

API = "https://api.github.com/repos/KalonixReal/randomfiles"
STAGE = "/home/z/my-project/scripts/bundle_stage/grammar-engine-v9.7.1"
ZIP = "/home/z/my-project/download/grammar-engine-v9.7.1-complete.zip"
ROOT_README = "/home/z/my-project/download/README.md"
UA = "bundle-uploader"


def req(url, token, data=None, method=None, ctype="application/json", raw=None):
    headers = {"Authorization": f"token {token}", "User-Agent": UA}
    body = None
    if raw is not None:
        body = raw
        headers["Content-Type"] = ctype
    elif data is not None:
        body = json.dumps(data).encode()
        headers["Content-Type"] = ctype
    r = urllib.request.Request(url, data=body, headers=headers, method=method)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(r, timeout=300) as resp:
                return json.loads(resp.read() or b"{}")
        except urllib.error.HTTPError as e:
            detail = e.read()[:400].decode("utf-8", "replace")
            if e.code in (403, 429, 502, 503) and attempt < 4:
                wait = 20 * (attempt + 1)
                print(f"  HTTP {e.code} at {url[:80]}; retry in {wait}s; {detail[:120]}")
                time.sleep(wait)
                continue
            print(f"FAILED at {method or 'GET'} {url[:100]} -> {e.code}\n{detail}",
                  file=sys.stderr)
            raise


def main():
    token = sys.argv[1]
    if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
        token = sys.argv[2]

    # 0. current main head
    main_ref = req(f"{API}/git/refs/heads/main", token)
    base_commit = main_ref["object"]["sha"]
    print("main head:", base_commit)

    # 1. blobs for every staged file
    entries = []
    files = []
    for dirpath, _dirs, filenames in os.walk(STAGE):
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, STAGE)
            files.append((rel, full))
    files.sort()
    print(f"{len(files)} files to push")
    for i, (rel, full) in enumerate(files):
        content = open(full, "rb").read()
        blob = req(f"{API}/git/blobs", token, {
            "content": base64.b64encode(content).decode(),
            "encoding": "base64",
        }, method="POST")
        entries.append({"path": f"grammar-engine-v9.7.1/{rel}", "mode": "100644",
                        "type": "blob", "sha": blob["sha"]})
        if (i + 1) % 25 == 0 or i == len(files) - 1:
            print(f"  blob {i + 1}/{len(files)}: {rel} ({len(content)} B)")

    # 2. root README + DELIVERY_README updates
    for path, src in [("README.md", None), ("DELIVERY_README.md", None)]:
        text = open(ROOT_README if path == "README.md" else
                    "/home/z/my-project/scripts/bundle_README.md").read()
        blob = req(f"{API}/git/blobs", token, {
            "content": text.encode().decode(),
            "encoding": "utf-8",
        }, method="POST")
        entries.append({"path": path, "mode": "100644", "type": "blob",
                        "sha": blob["sha"]})

    # 3. tree on top of current main
    tree = req(f"{API}/git/trees", token, {
        "base_tree": req(f"{API}/git/commits/{base_commit}", token)["tree"]["sha"],
        "tree": entries,
    }, method="POST")
    print("tree:", tree["sha"], len(tree.get("tree", [])), "entries")

    # 4. commit + ref update
    commit = req(f"{API}/git/commits", token, {
        "message": "Add grammar-engine-v9.7.1: subject-clause wh FP fixes (rules-2.8), "
                   "singular -s noun guards, fresh-set comparison, tagger-veto "
                   "experiment; X2 F0.5 .923 / X3 .954 / FA 0 everywhere",
        "tree": tree["sha"],
        "parents": [base_commit],
    }, method="POST")
    print("commit:", commit["sha"])
    ref = req(f"{API}/git/refs/heads/main", token, {
        "sha": commit["sha"], "force": False}, method="PATCH")
    print("main ->", ref["object"]["sha"])

    # 5. release + zip asset
    body = ("The complete project bundle (239 files, hash-verified via "
            "BUNDLE_MANIFEST.json): the offline grammar Notepad v9.7.1 "
            "(rules-2.8, v9.3.4 suggestions UI, Hunspell+NZ spelling), the "
            "original baseline build, the trained model delivery, all code, "
            "all datasets (X2/X3 one-shot sets + the FRESH held-out "
            "comparison set), all results including the fresh-set "
            "v9.7.0/v9.7.1/tagger-veto comparison, the report, and "
            "screenshots. Download and unzip — everything is inside.")
    rel = req(f"{API}/releases", token, {
        "tag_name": "v9.7.0-bundle", "target_commitish": "main",
        "name": "Grammar Engine v9.7.0 - complete bundle", "body": body,
        "draft": False, "prerelease": False,
    }, method="POST")
    rid = rel.get("id")
    print("release id:", rid)
    with open(ZIP, "rb") as f:
        asset = req(
            f"https://uploads.github.com/repos/KalonixReal/randomfiles/releases/{rid}/assets?name=grammar-engine-v9.7.1-complete.zip",
            token, raw=f.read(), method="POST",
            ctype="application/zip")
    print("asset:", asset.get("name"), asset.get("size"), "bytes,",
          asset.get("state"), asset.get("digest"))
    print("url:", asset.get("browser_download_url"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

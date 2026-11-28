#!/usr/bin/env python3
"""Assemble the complete project bundle for delivery.

Builds a staging tree (grammar-engine-v9.5.0/) that is then zipped into
download/grammar-engine-v9.5.0-complete.zip. Code files are deduplicated by
hash so code/ contains every distinct script exactly once.

Run:  python3 scripts/make_bundle.py
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

ROOT = "/home/z/my-project"
STAGE = os.path.join(ROOT, "scripts", "bundle_stage")
BUNDLE = "grammar-engine-v9.7.0"
B = os.path.join(STAGE, BUNDLE)
ZIP_PATH = os.path.join(ROOT, "download", "grammar-engine-v9.7.0-complete.zip")


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def copy(src, dest_dir, dest_name=None):
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, dest_name or os.path.basename(src))
    shutil.copy2(src, dest)
    return dest


def main():
    if os.path.exists(STAGE):
        shutil.rmtree(STAGE)
    os.makedirs(B)

    # ---- 1. the two HTML files -------------------------------------------
    copy(f"{ROOT}/download/notepad-v9.7.0-grammar.html", B)
    copy(f"{ROOT}/download/notepad-v9.3.4-ORIGINAL.html", B)

    # ---- 2. model delivery, wholesale (keeps SHA256SUMS.json paths valid)
    shutil.copytree(f"{ROOT}/download/model", f"{B}/model")

    # ---- 3. all project code, deduped by hash ----------------------------
    code = f"{B}/code"
    os.makedirs(code)
    seen = {}  # sha -> filename already placed
    sources = [
        f"{ROOT}/download/model/code",
        f"{ROOT}/scripts",
    ]
    for src_dir in sources:
        for name in sorted(os.listdir(src_dir)):
            p = os.path.join(src_dir, name)
            if not os.path.isfile(p) or not name.endswith((".py", ".js", ".sh")):
                continue
            h = sha(p)
            if h in seen:
                continue
            copy(p, code)
            seen[h] = name
    # authored corpus generators
    os.makedirs(f"{code}/data_authored", exist_ok=True)
    for name in sorted(os.listdir(f"{ROOT}/scripts/data_authored")):
        copy(f"{ROOT}/scripts/data_authored/{name}", f"{code}/data_authored")
    # Harper exploration modules (from the archive of work/)
    harper_dir = f"{ROOT}/archive/harper-wasm-probe"
    os.makedirs(f"{code}/harper", exist_ok=True)
    for name in sorted(os.listdir(harper_dir)):
        if name.endswith((".js", ".b64", ".json")) and "package" not in name:
            copy(os.path.join(harper_dir, name), f"{code}/harper")

    # ---- 4. v1 dataset ----------------------------------------------------
    os.makedirs(f"{B}/data-v1")
    for name in sorted(os.listdir(f"{ROOT}/archive/data-v1")):
        copy(f"{ROOT}/archive/data-v1/{name}", f"{B}/data-v1")

    # ---- 5. results-extra: unique-by-hash result artifacts ----------------
    re_dir = f"{B}/results-extra"
    os.makedirs(re_dir)
    # known result-file hashes: model/results/*, model root exports, scripts/results_*.json
    known = set()
    for d in (f"{ROOT}/download/model/results", f"{ROOT}/download/model"):
        for name in os.listdir(d):
            p = os.path.join(d, name)
            if os.path.isfile(p) and name.endswith(".json"):
                known.add(sha(p))
    for name in os.listdir(f"{ROOT}/scripts"):
        p = os.path.join(f"{ROOT}/scripts", name)
        if os.path.isfile(p) and name.endswith(".json"):
            known.add(sha(p))
    candidates = [
        f"{ROOT}/scripts/export_out",
        f"{ROOT}/scripts",
    ]
    for cdir in candidates:
        for name in sorted(os.listdir(cdir)):
            p = os.path.join(cdir, name)
            if not os.path.isfile(p):
                continue
            if name in ("package.json", "package-lock.json"):
                continue
            if not name.endswith((".json", ".jsonl", ".log")):
                continue
            if sha(p) in known:
                continue
            copy(p, re_dir)
    # glm_full run logs wholesale (evidence of the rate-limited GLM runs)
    shutil.copytree(f"{ROOT}/scripts/export_out/glm_full", f"{re_dir}/glm_full")

    # ---- 6. report + figures ----------------------------------------------
    rep = f"{B}/report"
    os.makedirs(f"{rep}/figures")
    copy(f"{ROOT}/download/grammar-engine-results-report.docx", rep)
    copy(f"{ROOT}/download/README.md", B, dest_name="DELIVERY_README.md")
    copy(f"{ROOT}/download/grammar-engine-results-report.pdf", rep)
    for name in sorted(os.listdir(f"{ROOT}/scripts")):
        if name.startswith("report_fig") and name.endswith(".png"):
            copy(f"{ROOT}/scripts/{name}", f"{rep}/figures")

    # ---- 7. screenshots ----------------------------------------------------
    scr = f"{B}/screenshots"
    os.makedirs(scr)
    for name in sorted(os.listdir(f"{ROOT}/download")):
        if name.endswith(".png"):
            copy(f"{ROOT}/download/{name}", scr)

    # ---- 8. Harper WASM probe binaries ------------------------------------
    exp = f"{B}/experiments/harper-wasm-probe"
    os.makedirs(exp)
    for name in ("proof933_wasm.bin", "proof933_encoder.bin",
                 "proof933_decoder.bin", "proof933_tokenizer.bin"):
        copy(os.path.join(harper_dir, name), exp)

    # ---- 8b. bundle README (authored separately) ---------------------------
    readme_src = f"{ROOT}/scripts/bundle_README.md"
    if os.path.exists(readme_src):
        copy(readme_src, B, dest_name="README.md")

    # ---- 9. manifest of what went in ---------------------------------------
    manifest = []
    for dirpath, _dirnames, filenames in os.walk(B):
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, B)
            manifest.append({"file": rel, "bytes": os.path.getsize(full),
                            "sha256": sha(full)})
    with open(f"{B}/BUNDLE_MANIFEST.json", "w") as f:
        json.dump(manifest, f, indent=1)
    print(f"staged {len(manifest)} files, "
          f"{sum(m['bytes'] for m in manifest)/1e6:.1f} MB raw")

    # ---- 10. zip -----------------------------------------------------------
    if os.path.exists(ZIP_PATH):
        os.remove(ZIP_PATH)
    subprocess.run(["zip", "-r", "-9", "-q", ZIP_PATH, BUNDLE],
                   cwd=STAGE, check=True)
    print(f"zip written: {ZIP_PATH} "
          f"({os.path.getsize(ZIP_PATH)/1e6:.1f} MB)")

    # ---- 11. verify: every staged file round-trips through the zip --------
    res = subprocess.run(["unzip", "-qq", "-o", ZIP_PATH, "-d",
                         os.path.join(STAGE, "_verify")], check=True)
    bad = 0
    for m in manifest:
        got = os.path.join(STAGE, "_verify", BUNDLE, m["file"])
        if not os.path.exists(got) or sha(got) != m["sha256"]:
            print("MISMATCH:", m["file"])
            bad += 1
    print(f"zip round-trip verification: {len(manifest) - bad}/{len(manifest)} OK, {bad} bad")
    shutil.rmtree(os.path.join(STAGE, "_verify"))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

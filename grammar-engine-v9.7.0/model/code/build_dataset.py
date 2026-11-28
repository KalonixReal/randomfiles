# -*- coding: utf-8 -*-
"""Dataset builder: assembles authored + template data into 4 partitions with
manifests and hashes. Also provides the token/tag pipeline used by training
and by the browser engine.

Partitions (by author group):
  train: S1 S2 W1 W2 T1 T2 T3 (+ template data)
  dev   : D1 D2 (model selection)
  calib : K1 (threshold calibration)
  test  : X1 X2 X3 (final untouched)
"""
import hashlib
import re
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corrupt as C
import templates as TPL

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_built")
AUTH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_authored")

TRAIN_GROUPS = {"S1", "S2", "W1", "W2", "T1", "T2", "T3"}
DEV_GROUPS = {"D1", "D2"}
CALIB_GROUPS = {"K1"}
TEST_GROUPS = {"X1", "X2", "X3"}


def load_authored():
    """Returns list of dicts: {text, edits:[{start,end,orig,rep,type}], clean, domain,
    variety, group, origin} for error entries; clean entries have empty edits."""
    import importlib.util

    def load_mod(name):
        spec = importlib.util.spec_from_file_location(name, os.path.join(AUTH, name + ".py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def locate(text, bad, good):
        """Find span of `bad`; if not unique, expand with surrounding tokens
        (identical text appended/prepended to both bad and good) until unique.
        Returns (start, end, bad_expanded, good_expanded)."""
        b, g = bad, good
        # try suffix expansion first (up to 2 tokens), then prefix expansion
        for _ in range(3):
            if text.count(b) == 1 and b in text:
                idx = text.find(b)
                return idx, idx + len(b), b, g
            # append next token after the first occurrence
            m = re.search(re.escape(b) + r"(\s+[A-Za-z']+)?", text)
            if m:
                ext = m.group(1) or ""
                if ext:
                    b, g = b + ext, g + ext
                    continue
            # prepend previous token
            m = re.search(r"([A-Za-z']+\s+)" + re.escape(b), text)
            if m:
                ext = m.group(1)
                b, g = ext + b, ext + g
            else:
                break
        idx = text.find(b)
        assert idx >= 0, (bad, text)
        assert text.count(b) == 1, (bad, b, text)
        return idx, idx + len(b), b, g

    items = []
    for name in ["train_errors_school", "train_errors_work", "train_errors_tech",
                 "dev", "calib", "test_errors_a", "test_errors_b"]:
        mod = load_mod(name)
        for entry in getattr(mod, "E", []):
            text, edits, domain, variety, group = entry
            out_edits = []
            for (bad, good, typ) in edits:
                s, e, bexp, gexp = locate(text, bad, good)
                out_edits.append({"start": s, "end": e, "orig": bexp, "rep": gexp, "type": typ})
            clean = text
            for ed in reversed(out_edits):
                clean = clean[:ed["start"]] + ed["rep"] + clean[ed["end"]:]
            items.append({"text": text, "edits": out_edits, "clean": clean,
                          "domain": domain, "variety": variety, "group": group,
                          "origin": "authored"})
    # correct + adversarial files
    import glob
    for name in ["train_correct", "dev", "calib", "test_correct"]:
        mod = load_mod(name)
        for entry in getattr(mod, "C", []):
            text, domain, variety, group, note = entry
            items.append({"text": text, "edits": [], "clean": text, "domain": domain,
                          "variety": variety, "group": group, "origin": "authored-clean",
                          "note": note})
        for entry in getattr(mod, "A", []):
            text, domain, variety, group, note = entry
            items.append({"text": text, "edits": [], "clean": text, "domain": domain,
                          "variety": variety, "group": group, "origin": "adversarial",
                          "note": note})
    # dev.py has E,C,A already handled; dev 'C'/'A' handled above
    return items


def jaccard(a, b):
    ta = set(a.lower().split())
    tb = set(b.lower().split())
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def build(seed=11, n_template=30000):
    rng = random.Random(seed)
    authored = load_authored()
    # split authored by group
    train_pool = [x for x in authored if x["group"] in TRAIN_GROUPS]
    evals = {p: [x for x in authored if x["group"] in g]
             for p, g in (("dev", DEV_GROUPS), ("calib", CALIB_GROUPS), ("test", TEST_GROUPS))}

    # ---- natural-text training pairs: corrupt authored CLEAN sentences
    # (clean versions of train errors + authored-clean train entries)
    natural_clean = []
    for x in train_pool:
        if x["edits"]:
            natural_clean.append((x["clean"], x["domain"], x["variety"]))
        elif x["origin"] == "authored-clean":
            natural_clean.append((x["text"], x["domain"], x["variety"]))
    natural_items = []
    K_PER_SENTENCE = 24
    for si, (clean, domain, variety) in enumerate(natural_clean):
        rr = random.Random(seed * 200003 + si)
        # keep one pristine copy
        natural_items.append({"text": clean, "edits": [], "clean": clean, "domain": domain,
                              "variety": variety, "group": "NAT", "origin": "natural-clean"})
        # never corrupt protected-content sentences (currency, numbers, urls, emails)
        if C.PROTECT_RE.search(clean):
            continue
        made = 0
        attempts = 0
        while made < K_PER_SENTENCE and attempts < K_PER_SENTENCE * 3:
            attempts += 1
            n_err = 1 if rr.random() < 0.75 else (2 if rr.random() < 0.9 else 3)
            ctext, edits = C.corrupt(clean, rr, n_errors=n_err)
            if not edits or ctext == clean:
                continue
            natural_items.append({"text": ctext,
                                  "edits": [{"start": a, "end": b, "orig": o, "rep": r_, "type": t}
                                            for (a, b, o, r_, t) in edits],
                                  "clean": clean, "domain": domain, "variety": variety,
                                  "group": "NAT", "origin": "natural-corrupt"})
            made += 1
    print(f"natural corrupted variants: {len(natural_items)} from {len(natural_clean)} clean")

    # ---- template data -> train only
    tpl = TPL.generate(n_template, seed=seed)
    tpl_items = []
    for i, s in enumerate(tpl):
        r = rng.random()
        if r < 0.58:
            n_err = 1 if rng.random() < 0.72 else (2 if rng.random() < 0.85 else 3)
            ctext, edits = C.corrupt(s, random.Random(seed * 100003 + i), n_errors=n_err)
            if not edits or ctext == s:
                tpl_items.append({"text": s, "edits": [], "clean": s, "domain": "template",
                                  "variety": "US", "group": "TPL", "origin": "template-clean"})
                continue
            tpl_items.append({"text": ctext, "edits": [{"start": a, "end": b, "orig": o,
                               "rep": r_, "type": t} for (a, b, o, r_, t) in edits],
                              "clean": s, "domain": "template", "variety": "US",
                              "group": "TPL", "origin": "template-corrupt"})
        else:
            tpl_items.append({"text": s, "edits": [], "clean": s, "domain": "template",
                              "variety": "US", "group": "TPL", "origin": "template-clean"})

    train_all = train_pool + natural_items + tpl_items
    # near-duplicate guard: drop train items too similar to any eval item
    eval_texts = [x["text"] for part in evals.values() for x in part]
    eval_sigs = [set(t.lower().split()) for t in eval_texts]
    kept = []
    dropped = 0
    for x in train_all:
        sig = set(x["text"].lower().split())
        dup = False
        for es in eval_sigs:
            inter = len(sig & es)
            union = len(sig | es)
            if union and inter / union >= 0.7:
                dup = True
                break
        if not dup:
            kept.append(x)
        else:
            dropped += 1
    print(f"near-dup guard dropped {dropped} train items")
    train_all = kept
    # exact dup within train
    seen = set()
    final_train = []
    for x in train_all:
        if x["text"] in seen:
            continue
        seen.add(x["text"])
        final_train.append(x)
    return {"train": final_train, "dev": evals["dev"], "calib": evals["calib"], "test": evals["test"]}


def dump(part):
    os.makedirs(DATA_DIR, exist_ok=True)
    stats = {}
    for name, items in part.items():
        path = os.path.join(DATA_DIR, name + ".jsonl")
        h = hashlib.sha256()
        with open(path, "w", encoding="utf-8") as f:
            for x in items:
                line = json.dumps(x, ensure_ascii=False, sort_keys=True)
                h.update(line.encode("utf-8"))
                f.write(line + "\n")
        stats[name] = {
            "count": len(items),
            "with_errors": sum(1 for x in items if x["edits"]),
            "clean": sum(1 for x in items if not x["edits"]),
            "sha256": h.hexdigest(),
        }
    with open(os.path.join(DATA_DIR, "manifest.json"), "w") as f:
        json.dump(stats, f, indent=1)
    return stats


if __name__ == "__main__":
    part = build()
    stats = dump(part)
    print(json.dumps(stats, indent=1))
    # sample view
    for name in ("train", "dev", "test"):
        print(f"--- {name} samples ---")
        with open(os.path.join(DATA_DIR, name + ".jsonl")) as f:
            lines = [json.loads(next(f)) for _ in range(3)]
        for x in lines:
            print("  ", x["text"], "|", [(e["orig"], e["rep"], e["type"]) for e in x["edits"]])

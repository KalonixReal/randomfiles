# -*- coding: utf-8 -*-
"""Score GLM comparison outputs (glm_comparison.json) with the same
edit-level span matcher used everywhere else (score_edits.py)."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score_edits import extract_edits, match, norm_text

HERE = os.path.dirname(os.path.abspath(__file__))

def f05(p, r):
    b = 0.5
    return (1 + b * b) * p * r / (b * b * p + r) if (p + r) else 0.0

def score_prompt(items, prompt):
    tp = fp = fn = 0
    n_clean = n_clean_flag = 0
    meaning_risk = 0
    per_cat = {}
    for it in items:
        bad = it["text"]
        gold = [(e["start"], e["end"], e.get("rep", "")) for e in it["edits"]]
        out = it["results"].get(prompt)
        if out is None or str(out).startswith("ERROR"):
            pred = []
        else:
            pred = extract_edits(bad, out)
        matched = set()
        for pe in pred:
            hit = None
            for gi, ge in enumerate(gold):
                if gi in matched:
                    continue
                if match(pe, ge):
                    matched.add(gi); hit = gi; break
            if hit is not None:
                tp += 1
            else:
                fp += 1
        fn += len(gold) - len(matched)
        if not gold:
            n_clean += 1
            if pred:
                n_clean_flag += 1
                if any(norm_text(p[2]) and any(norm_text(p[2]) != norm_text(g[2]) for g in []) for p in pred):
                    pass
                meaning_risk += 0  # counted below via changed tokens
        # per-category
        for e in it["edits"]:
            c = e.get("type", "?")
            d = per_cat.setdefault(c, {"tp": 0, "fn": 0})
            if any(gi == i for i, gi in enumerate(matched)):
                pass
        for i, ge in enumerate(gold):
            c = it["edits"][i].get("type", "?")
            d = per_cat.setdefault(c, {"tp": 0, "fn": 0})
            if i in matched:
                d["tp"] += 1
            else:
                d["fn"] += 1
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    return {
        "prompt": prompt, "n": len(items),
        "P": round(p, 3), "R": round(r, 3), "F05": round(f05(p, r), 3),
        "F1": round(2 * p * r / (p + r), 3) if p + r else 0.0,
        "tp": tp, "fp": fp, "fn": fn,
        "clean_flag_rate": round(n_clean_flag / n_clean, 3) if n_clean else None,
        "n_clean": n_clean,
        "per_cat": {k: v for k, v in sorted(per_cat.items())},
    }

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "export_out", "glm_comparison.json")
    items = json.load(open(src))
    for prompt in ("standard", "strict"):
        print(json.dumps(score_prompt(items, prompt), indent=1))

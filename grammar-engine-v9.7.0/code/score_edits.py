"""Score GLM (or any corrector) outputs against gold: edit-level P/R/F1.

Edit extraction: align(s_bad -> corrected_output) token ops; a predicted edit
matches a gold edit if char spans overlap >=50% (either direction) AND the
replacement text is equal after normalisation. Non-matching predicted edits on
positions that gold doesn't edit = false positives. Missing gold edits =
misses. Also flags overcorrection (changed tokens gold kept) and, for clean
sentences, any change at all.
"""

import json, sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from align import tokenize

def extract_edits(bad, fixed):
    """char-span edits turning bad -> fixed (list of (s,e,text))."""
    if fixed is None:
        return []
    bt = tokenize(bad)
    # token-level mapping via difflib on words
    import difflib
    bw = [t["w"].replace("’", "'") for t in bt]
    ft = tokenize(fixed)
    fw = [t["w"].replace("’", "'") for t in ft]
    sm = difflib.SequenceMatcher(a=bw, b=fw, autojunk=False)
    edits = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        if tag in ("replace", "delete"):
            s = bt[i1]["s"] if i1 < len(bt) else (bt[-1]["e"] if bt else 0)
            e = bt[i2 - 1]["e"] if i2 > 0 and i2 <= len(bt) else s
            text = " ".join(fw[j1:j2]) if tag == "replace" else ""
            # normalise: collapse case-only changes to case marker
            edits.append((s, e, text))
        elif tag == "insert":
            anchor_s = bt[i1 - 1]["e"] if i1 > 0 else 0
            anchor_e = bt[i1]["s"] if i1 < len(bt) else anchor_s
            text = " ".join(fw[j1:j2])
            edits.append((anchor_s, anchor_e, text))
    return edits

def norm_text(t):
    return re.sub(r"\s+", " ", t.strip().lower())

def match(e_pred, e_gold):
    ps, pe, pt = e_pred
    gs, ge, gt = e_gold
    ov = max(0, min(pe, ge) - max(ps, gs))
    lenp, leng = max(pe - ps, 1), max(ge - gs, 1)
    if ov / min(lenp, leng) < 0.5:
        return False
    return norm_text(pt) == norm_text(gt)

def score(rows, outs, name, label):
    tp = fp = fn = 0
    over = 0  # clean-position changes (meaning/overcorrection risk)
    n_clean = n_clean_flagged = 0
    n_corr = 0
    per_cat = {}
    for o in outs:
        i = o["idx"]
        if i >= len(rows) or not o.get("ok"):
            continue
        row = rows[i]
        pred_edits = extract_edits(row["s_bad"], o["out"])
        gold_edits = [(ed["start"], ed["end"], ed["text"]) for ed in row["edits"]]
        cats = row["cats"] or ["CLEAN"]
        matched = set()
        for pe in pred_edits:
            hit = False
            for gi, ge in enumerate(gold_edits):
                if gi in matched:
                    continue
                if match(pe, ge):
                    matched.add(gi)
                    hit = True
                    break
            if hit:
                tp += 1
            else:
                fp += 1
        fn += len(gold_edits) - len(matched)
        if row["clean"]:
            n_clean += 1
            if pred_edits:
                n_clean_flagged += 1
        else:
            n_corr += 1
            if len(matched) == len(gold_edits) and not any(
                not match(pe, ge) for pe in pred_edits for ge in []
            ) and fp == 0:
                pass
        for c in cats:
            d = per_cat.setdefault(c, [0, 0, 0])
            for gi, ge in enumerate(gold_edits):
                if gi in matched:
                    d[0] += 1
                else:
                    d[1] += 1
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * p * r / (p + r) if p + r else 0.0
    res = {"system": label, "P": round(p, 4), "R": round(r, 4),
           "F1": round(f1, 4), "tp": tp, "fp": fp, "fn": fn,
           "clean_flag_rate": round(n_clean_flagged / n_clean, 4) if n_clean else None,
           "n_clean": n_clean, "n_corrupt": n_corr, "per_cat": per_cat}
    print(json.dumps(res, indent=1)[:1200])
    return res

if __name__ == "__main__":
    rows = [json.loads(l) for l in open(sys.argv[1])]
    outs = [json.loads(l) for l in open(sys.argv[2])]
    label = sys.argv[3] if len(sys.argv) > 3 else "system"
    score(rows, outs, sys.argv[1], label)

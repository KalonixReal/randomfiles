# -*- coding: utf-8 -*-
"""FN/FP analysis of the rules engine on dev (equivalent-effect scorer)."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine as E

spec = json.load(open(os.path.join(HERE := os.path.dirname(os.path.abspath(__file__)), "rules.json")))
dev = E.load_split("dev")

missed = {}
fps = []
for it in dev:
    props = E.rules_findings(it["text"], spec)
    tp, fp, fn = E.score(props, it["edits"], it["text"])
    # which gold edits were missed?
    for g in it["edits"]:
        geff = E._NORM(E._apply_edit(it["text"], g["start"], g["end"], g["rep"]))
        gkey = (g["start"], g["end"], g["rep"].strip().lower())
        covered = any(
            E._NORM(E._apply_edit(it["text"], f["start"], f["end"], f["rep"])) == geff
            or (f["start"], f["end"], f["rep"].strip().lower()) == gkey for f in props)
        if not covered:
            missed.setdefault(g["type"], []).append((it["text"], g["orig"], g["rep"]))
    if fp:
        for f in props:
            pass
        # count FPs on clean only
        if not it["edits"]:
            fps.append((it["text"], [(f["start"], f["end"], f["rep"]) for f in props]))

print("=== MISSED gold edits by type ===")
for t, lst in sorted(missed.items(), key=lambda kv: -len(kv[1])):
    print(f"\n[{t}] {len(lst)} missed")
    for text, orig, rep in lst[:6]:
        print(f"   {orig!r} -> {rep!r} | {text[:90]}")
print("\n=== clean-sentence FPs ===")
for text, f in fps[:12]:
    print(f"   {f} | {text[:80]}")

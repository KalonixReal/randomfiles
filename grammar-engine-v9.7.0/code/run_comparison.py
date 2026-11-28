# -*- coding: utf-8 -*-
"""Full engine comparison on a chosen split. Writes results JSON."""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine as E

HERE = os.path.dirname(os.path.abspath(__file__))
import gec_model as G
from collections import Counter


def attach_fallback(vocab):
    train = E.load_split("train")
    pair_c = Counter()
    for it in train:
        for e in it["edits"]:
            if e["rep"]:
                o = e["orig"].strip().split()
                r = e["rep"].strip().split()
                if len(o) == 1 and len(r) == 1:
                    pair_c[(o[0].lower(), r[0].lower())] += 1
    vocab.fallback_map = {o: r for (o, r) in pair_c}
    for b in G.VERB_BASES:
        if b.endswith(("s", "x", "z", "ch", "sh", "o")):
            s3v = b + "es"
        elif b.endswith("y") and len(b) > 1 and b[-2] not in "aeiou":
            s3v = b[:-1] + "ies"
        else:
            s3v = b + "s"
        vocab.fallback_map.setdefault(b, s3v)
        vocab.fallback_map.setdefault(b + "ed", b)
    for a, bb in G.HOMOPHONE_SWAPS + G.CONTR_EXPAND + G.PRONOUN_FIX + G.PLURAL_FIX:
        vocab.fallback_map.setdefault(a, bb)


def run(split="dev", thresholds=(0.5, 0.8, 0.9, 0.95, 0.98)):
    spec = json.load(open(os.path.join(HERE, "rules.json")))
    items = E.load_split(split)
    net, vocab = E.load_tagger("gru")
    attach_fallback(vocab)
    results = []

    def timed(name, fn, per_call_limit=None):
        t0 = time.time()
        r = E.evaluate_engine(fn, items, name, per_type=(name in ("rules", "harper", "t5")))
        r["wall_seconds"] = round(time.time() - t0, 1)
        results.append(r)
        print(json.dumps(r, default=str)[:220])

    # no-change
    timed("none", lambda it: [])
    # Harper (raw + FP-filtered)
    harp = E.harper_batch(items)
    timed("harper (raw)", lambda it: harp[items.index(it)])
    harp_f = [E.harper_filter(h, it["text"]) for it, h in zip(items, harp)]
    timed("harper (filtered)", lambda it: harp_f[items.index(it)])
    # T5 (existing neural model)
    E.t5_load()
    timed("t5", lambda it: E.t5_findings(it["text"]))
    # rules
    timed("rules", lambda it: E.rules_findings(it["text"], spec))
    # tagger at thresholds
    for th in thresholds:
        timed(f"tagger@{th}", lambda it, th=th: E.tagger_findings(net, vocab, it["text"], th))
    # rules + tagger
    for th in (0.9, 0.95):
        def combo(it, th=th):
            rs = E.rules_findings(it["text"], spec)
            tg = E.tagger_findings(net, vocab, it["text"], th)
            out = list(rs)
            for f in tg:
                if any(f["start"] < o["end"] and o["start"] < f["end"] for o in out):
                    continue
                out.append(f)
            return out
        timed(f"rules+tagger@{th}", combo)
    # original build combination: Harper + T5 contextual (dedup: Harper wins overlaps)
    def orig(it):
        i = items.index(it)
        rs = E.t5_findings(it["text"])
        add = [f for f in rs if not any(f["start"] < h["end"] and h["start"] < f["end"] for h in harp[i])]
        return harp[i] + add
    timed("harper+t5 (original build)", orig)
    def orig_f(it):
        i = items.index(it)
        rs = E.t5_findings(it["text"])
        add = [f for f in rs if not any(f["start"] < h["end"] and h["start"] < f["end"] for h in harp_f[i])]
        return harp_f[i] + add
    timed("harper+filt+t5 (orig+FPfilter)", orig_f)
    # new combined: Harper + rules + tagger (Harper wins overlaps)
    def newc(it):
        i = items.index(it)
        rs = E.rules_findings(it["text"], spec)
        tg = E.tagger_findings(net, vocab, it["text"], 0.95)
        add = []
        for f in rs + tg:
            if any(f["start"] < h["end"] and h["start"] < f["end"] for h in harp_f[i]):
                continue
            if any(f["start"] < o["end"] and o["start"] < f["end"] for o in add):
                continue
            add.append(f)
        return harp_f[i] + add
    timed("harper_f+rules+tagger@0.95 (new build)", newc)
    out = os.path.join(HERE, f"results_{split}.json")
    with open(out, "w") as f:
        json.dump(results, f, indent=1, default=str)
    print("saved", out)
    return results


if __name__ == "__main__":
    split = sys.argv[1] if len(sys.argv) > 1 else "dev"
    run(split)

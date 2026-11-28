# -*- coding: utf-8 -*-
"""Improved tagger training v2: bigger GRU + data augmentation + longer schedule.

Augmentation: re-corrupt every clean sentence in train (each gets up to 3 new
corruption variants), producing extra (text, edits) rows. All from train data
only — dev/calib/test untouched.

Usage: python3 train2.py [--epochs 30] [--hidden 192]
"""
import argparse
import json
import math
import os
import sys
import time
import random
from collections import Counter

import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gec_model import GRUTagger, Vocab, tokenize
import corrupt as C

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data_built")
CKPT = os.path.join(HERE, "checkpoints")


def load_split(name):
    return [json.loads(l) for l in open(os.path.join(DATA, name + ".jsonl"))]


def augment(train_items, variants=3, seed=17):
    rng = random.Random(seed)
    seen_texts = {it["text"] for it in train_items}
    out = []
    for it in train_items:
        clean = it.get("clean")
        if not clean:
            continue
        made = 0
        for _try in range(variants * 3):
            if made >= variants:
                break
            try:
                res = C.corrupt(clean, rng)
            except Exception:
                continue
            if not res:
                continue
            bad, edits = res
            if not edits or bad in seen_texts:
                continue
            dicts = [{"start": s, "end": e, "orig": bad[s:e], "rep": rep, "type": typ}
                     for (s, e, _orig, rep, typ) in edits]
            out.append({"text": bad, "clean": clean, "edits": dicts,
                        "origin": "aug-corrupt", "group": it.get("group"),
                        "variety": it.get("variety", "NZ"), "domain": it.get("domain")})
            seen_texts.add(bad)
            made += 1
    return out


def main(epochs, hidden, resume):
    torch.manual_seed(0)
    rng = random.Random(0)
    train_items = load_split("train")
    auth = [x for x in train_items if x["origin"].startswith("authored")]
    aug = augment(train_items, variants=1)
    train_items = train_items + aug + auth * 2
    print(f"train={len(train_items)} (aug +{len(aug)}, authored x4)")
    dev_items = load_split("dev")

    vocab, _ = Vocab.build(train_items)
    print(f"vocab: words={vocab.n_words} edits={len(vocab.edit2id)}")

    # fallback pair map
    pair_c = Counter()
    for it in train_items:
        for e in it["edits"]:
            if e["rep"]:
                o = e["orig"].strip().split()
                r = e["rep"].strip().split()
                if len(o) == 1 and len(r) == 1:
                    pair_c[(o[0].lower(), r[0].lower())] += 1
    fallback = {}
    for (o, r), c in pair_c.items():
        if o not in fallback or c > fallback[o][1]:
            fallback[o] = (r, c)
    vocab.fallback_map = {k: v[0] for k, v in fallback.items()}
    import gec_model as G
    for b in G.VERB_BASES:
        if b.endswith(("s", "x", "z", "ch", "sh", "o")):
            s3 = b + "es"
        elif b.endswith("y") and len(b) > 1 and b[-2] not in "aeiou":
            s3 = b[:-1] + "ies"
        else:
            s3 = b + "s"
        vocab.fallback_map.setdefault(b, s3)
        vocab.fallback_map.setdefault(b + "ed", b)
    for a, b in G.HOMOPHONE_SWAPS + G.CONTR_EXPAND + G.PRONOUN_FIX + G.PLURAL_FIX:
        vocab.fallback_map.setdefault(a, b)

    model = GRUTagger(vocab, hidden=hidden)
    start_ep = 0
    print(f"GRU hidden={hidden} params={sum(p.numel() for p in model.parameters())}")
    lr = 2e-3
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)
    best_f05 = -1.0
    ck_last = os.path.join(CKPT, "gru2_last.pt")
    if os.path.exists(ck_last):
        ck = torch.load(ck_last, weights_only=False)
        if ck.get("vocab_words") == vocab.word2id and ck.get("hidden") == hidden:
            model.load_state_dict(ck["model"])
            opt.load_state_dict(ck["opt"])
            start_ep = ck.get("epoch", -1) + 1
            best_f05 = ck.get("best_f05", -1.0) or -1.0
            if os.path.exists(os.path.join(CKPT, "gru2_best.json")):
                best_f05 = max(best_f05, json.load(open(os.path.join(CKPT, "gru2_best.json")))["dev_metrics"]["f05"])
            print(f"resumed from epoch {start_ep} best={best_f05:.4f}", flush=True)
    batch = 48
    steps_per_epoch = (len(train_items) + batch - 1) // batch
    total_steps = steps_per_epoch * epochs
    warmup = 300

    def lr_at(step):
        if step < warmup:
            return step / max(1, warmup)
        t = (step - warmup) / max(1, total_steps - warmup)
        return max(0.05, 0.5 * (1 + math.cos(math.pi * t)))

    step = start_ep * ((len(train_items) + 47) // 48)
    best_ep = -1
    history = []
    keep_ids = [vocab.edit2id["$KEEP"]]
    order = list(range(len(train_items)))
    gen = torch.Generator().manual_seed(0)
    patience = 0
    for ep in range(start_ep, epochs):
        perm = torch.randperm(len(train_items), generator=gen).tolist()
        model.train()
        t0 = time.time()
        losses = []
        for bi in range(0, len(perm), batch):
            chunk = [train_items[i] for i in perm[bi:bi + batch]]
            feats = [vocab.featurize(it["text"]) for it in chunk]
            toks = [tokenize(it["text"]) for it in chunk]
            lengths = [len(f) for f in feats]
            tgt = []
            for it in chunk:
                tgt.append(vocab.labels_for(it["text"], it["edits"]))
            B = len(chunk)
            T = max(lengths)
            tgt_t = torch.zeros(B, T, dtype=torch.long)
            for b in range(B):
                for i, v in enumerate(tgt[b]):
                    tgt_t[b, i] = v
            for g in opt.param_groups:
                g["lr"] = lr * lr_at(step)
            logits = model(feats, toks, lengths)
            mask = torch.zeros(B, T, dtype=torch.float)
            for b in range(B):
                mask[b, :lengths[b]] = 1.0
            w = mask * torch.where(tgt_t == keep_ids[0], 1.0, 8.0)
            loss = (F.cross_entropy(logits.reshape(-1, logits.size(-1)),
                                    tgt_t.reshape(-1), reduction="none").reshape(B, T) * w).sum() / w.sum()
            opt.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 3.0)
            opt.step()
            losses.append(float(loss))
            step += 1
        # dev eval (span-level, same scorer as the harness)
        from train_models import evaluate
        metrics = evaluate(model, vocab, dev_items, thresh=0.0)
        history.append({"epoch": ep, "loss": sum(losses) / max(1, len(losses)),
                        "dev": metrics, "time": time.time() - t0,
                        "train_items": len(train_items)})
        print(f"ep {ep} loss {sum(losses)/max(1,len(losses)):.4f} "
              f"dev P={metrics['precision']:.3f} R={metrics['recall']:.3f} "
              f"F05={metrics['f05']:.3f} FA={metrics['false_alert_rate']:.3f} "
              f"({time.time()-t0:.0f}s)", flush=True)
        ck = {"model": model.state_dict(), "opt": opt.state_dict(), "step": step,
              "epoch": ep, "best_f05": best_f05, "vocab_words": vocab.word2id,
              "vocab_edits": vocab.id2edit, "hidden": hidden,
              "fallback": vocab.fallback_map}
        torch.save(ck, os.path.join(CKPT, "gru2_last.pt"))
        if metrics["f05"] > best_f05:
            best_f05 = metrics["f05"]
            best_ep = ep
            patience = 0
            torch.save(ck, os.path.join(CKPT, "gru2_best.pt"))
            with open(os.path.join(CKPT, "gru2_best.json"), "w") as f:
                json.dump({"epoch": ep, "dev_metrics": metrics, "hidden": hidden}, f)
        else:
            patience += 1
            if patience >= 7:
                print(f"early stop at ep {ep} (best {best_f05:.3f} @ ep {best_ep})")
                break
    with open(os.path.join(CKPT, "gru2_history.json"), "w") as f:
        json.dump(history, f)
    print(f"BEST F05={best_f05:.4f} at epoch {best_ep}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--epochs", type=int, default=30)
    ap.add_argument("--hidden", type=int, default=192)
    ap.add_argument("--resume", default=None)
    a = ap.parse_args()
    main(a.epochs, a.hidden, a.resume)

# -*- coding: utf-8 -*-
"""Tagger training v3: hard-negative weighted + GLM-distilled data.

Changes vs train2.py:
- train + train_aug.jsonl (glm-error pairs, glm-clean + authored U2 hard negatives)
- hard-negative clean rows repeated x NEG_W to hammer KEEP on natural text
- dev LOSS computed each epoch -> train-vs-dev loss gap logged (overfit monitor)
- tagger-only false-alert rate on dev clean + U2/GLM clean measured each epoch
- saves gru3_* checkpoints (does not clobber gru2)

Usage: python3 train3.py [--epochs 12] [--hidden 192] [--neg_w 3]
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
from train_models import evaluate

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data_built")
CKPT = os.path.join(HERE, "checkpoints")


def load_split(name):
    p = os.path.join(DATA, name + ".jsonl")
    return [json.loads(l) for l in open(p)]


def main(epochs, hidden, neg_w, resume):
    torch.manual_seed(0)
    rng = random.Random(0)
    train_items = load_split("train")
    auth = [x for x in train_items if x["origin"].startswith("authored")]
    # augmentation: same corruption-augmentation as v2 (train-only)
    from train2 import augment  # reuse identical augmentation
    aug = augment(train_items, variants=1)
    train_aug = load_split("train_aug")
    hard_neg = [r for r in train_aug if not r["edits"]]
    glm_err = [r for r in train_aug if r["edits"]]
    train_items = train_items + aug + auth * 2 + glm_err * 2 + hard_neg * neg_w
    print(f"train={len(train_items)} "
          f"(aug +{len(aug)}, authored x4, glm-err x2={len(glm_err)*2}, "
          f"hard-neg x{neg_w}={len(hard_neg)*neg_w})", flush=True)
    dev_items = load_split("dev")
    neg_eval = hard_neg  # FP-rate probe set (NOT trained as eval gold; it IS trained - see note)

    vocab, _ = Vocab.build(train_items)
    print(f"vocab: words={vocab.n_words} edits={len(vocab.edit2id)}", flush=True)

    # fallback map (same construction as train2)
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
    print(f"GRU hidden={hidden} params={sum(p.numel() for p in model.parameters())}", flush=True)
    lr = 2e-3
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)
    best_key = -1.0
    ck_last = os.path.join(CKPT, "gru3_last.pt")
    if resume and os.path.exists(ck_last):
        ck = torch.load(ck_last, weights_only=False)
        if ck.get("vocab_words") == vocab.word2id and ck.get("hidden") == hidden:
            model.load_state_dict(ck["model"])
            opt.load_state_dict(ck["opt"])
            start_ep = ck.get("epoch", -1) + 1
            best_key = ck.get("best_key", -1.0) or -1.0
            print(f"resumed from epoch {start_ep} best_key={best_key:.4f}", flush=True)
    batch = 48
    steps_per_epoch = (len(train_items) + batch - 1) // batch
    total_steps = steps_per_epoch * epochs
    warmup = 300

    def lr_at(step):
        if step < warmup:
            return step / max(1, warmup)
        t = (step - warmup) / max(1, total_steps - warmup)
        return max(0.05, 0.5 * (1 + math.cos(math.pi * t)))

    step = start_ep * steps_per_epoch
    best_ep = -1
    history = []
    keep_ids = [vocab.edit2id["$KEEP"]]
    gen = torch.Generator().manual_seed(0)
    patience = 0

    def dev_loss():
        model.eval()
        tot, n = 0.0, 0
        with torch.no_grad():
            for bi in range(0, len(dev_items), batch):
                chunk = dev_items[bi:bi + batch]
                feats = [vocab.featurize(it["text"]) for it in chunk]
                toks = [tokenize(it["text"]) for it in chunk]
                lengths = [len(f) for f in feats]
                tgt = [vocab.labels_for(it["text"], it["edits"]) for it in chunk]
                B = len(chunk)
                T = max(lengths) if lengths else 1
                tgt_t = torch.zeros(B, T, dtype=torch.long)
                for b in range(B):
                    for i, v in enumerate(tgt[b]):
                        tgt_t[b, i] = v
                logits = model(feats, toks, lengths)
                mask = torch.zeros(B, T, dtype=torch.float)
                for b in range(B):
                    mask[b, :lengths[b]] = 1.0
                w = mask * torch.where(tgt_t == keep_ids[0], 1.0, 8.0)
                loss = (F.cross_entropy(logits.reshape(-1, logits.size(-1)),
                                        tgt_t.reshape(-1), reduction="none").reshape(B, T) * w).sum() / w.sum()
                tot += float(loss) * B
                n += B
        model.train()
        return tot / max(1, n)

    def neg_fa(thresh=0.995):
        """tagger-only findings on hard-negative clean text (want 0)."""
        from engine import tagger_findings
        flagged = 0
        for r in neg_eval:
            f = tagger_findings(model, vocab, r["text"], thresh)
            if f:
                flagged += 1
        return flagged / max(1, len(neg_eval))

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
            tgt = [vocab.labels_for(it["text"], it["edits"]) for it in chunk]
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
        metrics = evaluate(model, vocab, dev_items, thresh=0.0)
        dl = dev_loss()
        fa = neg_fa(0.995)
        train_loss = sum(losses) / max(1, len(losses))
        history.append({"epoch": ep, "loss": train_loss, "dev_loss": dl,
                        "gap": dl - train_loss, "dev": metrics,
                        "neg_fa0995": fa, "time": time.time() - t0,
                        "train_items": len(train_items)})
        print(f"ep {ep} loss {train_loss:.4f} devloss {dl:.4f} gap {dl - train_loss:+.4f} "
              f"dev P={metrics['precision']:.3f} R={metrics['recall']:.3f} "
              f"F05={metrics['f05']:.3f} FA={metrics['false_alert_rate']:.3f} "
              f"negFA={fa:.3f} ({time.time() - t0:.0f}s)", flush=True)
        ck = {"model": model.state_dict(), "opt": opt.state_dict(), "step": step,
              "epoch": ep, "best_key": best_key, "vocab_words": vocab.word2id,
              "vocab_edits": vocab.id2edit, "hidden": hidden,
              "fallback": vocab.fallback_map}
        torch.save(ck, ck_last)
        # selection key: dev F05 with a FA penalty (FP-focused)
        key = metrics["f05"] - 2.0 * max(0.0, metrics["false_alert_rate"] - 0.01) - 1.0 * fa
        if key > best_key:
            best_key = key
            best_ep = ep
            patience = 0
            torch.save(ck, os.path.join(CKPT, "gru3_best.pt"))
            with open(os.path.join(CKPT, "gru3_best.json"), "w") as f:
                json.dump({"epoch": ep, "dev_metrics": metrics, "neg_fa": fa,
                           "key": key, "hidden": hidden}, f)
        else:
            patience += 1
            if patience >= 7:
                print(f"early stop at ep {ep} (best_key {best_key:.4f} @ ep {best_ep})", flush=True)
                break
    with open(os.path.join(CKPT, "gru3_history.json"), "w") as f:
        json.dump(history, f)
    print(f"BEST key={best_key:.4f} at epoch {best_ep}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--epochs", type=int, default=12)
    ap.add_argument("--hidden", type=int, default=192)
    ap.add_argument("--neg_w", type=int, default=3)
    ap.add_argument("--resume", default=None)
    a = ap.parse_args()
    main(a.epochs, a.hidden, a.neg_w, a.resume)

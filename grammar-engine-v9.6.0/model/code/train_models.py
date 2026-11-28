# -*- coding: utf-8 -*-
import math
"""Training loop for both candidates + evaluation harness (decode, PR metrics).

Usage:
  python3 train_models.py --model gru
  python3 train_models.py --model transformer
  python3 train_models.py --model gru --resume ckpt.pt
"""
import argparse
import json
import os
import sys
import time

import re
import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gec_model import (GRUTagger, TinyTransformerTagger, Vocab, tokenize,
                       tokenize_with_offsets, KEEP, DELETE, CASE_CAP, REPLACE,
                       INSERT, APPEND, REPLACE_OOV, SPECIALS)

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_built")
CKPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "checkpoints")


def load_split(name):
    items = []
    with open(os.path.join(DATA, name + ".jsonl")) as f:
        for line in f:
            items.append(json.loads(line))
    return items


def decode(model, vocab, text, max_passes=2, thresh=0.0, use_fallback=True):
    """Greedy iterative decode. Returns proposals (start, end, replacement, tag, prob)
    with spans on the ORIGINAL `text`, derived by diffing original vs final text."""
    import corrupt as C
    model.eval()
    cur = text
    fallback = getattr(vocab, "fallback_map", None)
    for _p in range(max_passes):
        toks = tokenize_with_offsets(cur)
        feats = [vocab.featurize(cur)]
        tok_strs = [t for (t, a, b) in toks]
        with torch.no_grad():
            logits = model(feats, [tok_strs], [len(feats[0])])
        probs = F.softmax(logits[0], dim=-1)
        edited = False
        ops = []  # (start, end, replacement) on cur
        for i in range(1, len(toks) + 1):
            tag_id = int(probs[i].argmax())
            p = float(probs[i][tag_id])
            tag = vocab.id2edit[tag_id]
            if tag == KEEP or p < thresh:
                continue
            tok, ts, te = toks[i - 1]
            if tag == DELETE:
                # delete the token plus one adjacent space if present
                e2 = te
                if e2 < len(cur) and cur[e2] == " ":
                    e2 += 1
                elif ts > 0 and cur[ts - 1] == " ":
                    ts -= 1
                ops.append((ts, e2, ""))
                edited = True
            elif tag == CASE_CAP:
                ops.append((ts, te, tok.capitalize()))
                edited = True
            elif tag == REPLACE_OOV:
                if use_fallback and fallback and re.match(r"^[A-Za-z']+$", tok):
                    rep = fallback.get(tok.lower())
                    if rep and rep != tok:
                        ops.append((ts, te, _case_like(tok, rep)))
                        edited = True
            elif tag.startswith(REPLACE):
                rep = tag[len(REPLACE):]
                ops.append((ts, te, _case_like(tok, rep)))
                edited = True
            elif tag.startswith(INSERT):
                rep = tag[len(INSERT):]
                ops.append((ts, ts, rep + " "))
                edited = True
            elif tag.startswith(APPEND):
                rep = tag[len(APPEND):]
                pos = te
                pad = "" if (pos >= len(cur) or cur[pos] in " .,!?") else " "
                ops.append((pos, pos, rep + pad))
                edited = True
        if not edited:
            break
        cur2 = cur
        for (s, e, rep) in sorted(ops, key=lambda x: -x[0]):
            cur2 = cur2[:s] + rep + cur2[e:]
        if cur2 == cur:
            break
        cur = cur2
    if cur == text:
        return []
    final_ops = C.diff_edits(text, cur)  # spans on ORIGINAL text
    out = []
    for (s, e, rep) in final_ops:
        out.append((s, e, rep, "diff", 1.0))
    return out


def _case_like(src, rep):
    """Match capitalisation pattern of src on rep."""
    if src[0].isupper() and rep[0].isalpha():
        return rep[0].upper() + rep[1:]
    return rep


def score_proposals(proposals, gold_edits):
    """Span-based scoring. Returns (tp, fp, fn)."""
    def norm(e):
        return (e[0], e[1], e[2].strip().lower(), e[2])
    g = {(e["start"], e["end"], e["rep"].strip().lower()) for e in gold_edits}
    p = {(s, en, rep.strip().lower()) for (s, en, rep, tag, prob) in proposals}
    tp = len(g & p)
    fp = len(p - g)
    fn = len(g - p)
    return tp, fp, fn


def evaluate(model, vocab, items, thresh=0.0, max_passes=2, limit=None):
    model.eval()
    TP = FP = FN = 0
    false_alert_sentences = 0
    clean_sentences = 0
    err_sentences = 0
    caught = 0
    for it in (items[:limit] if limit else items):
        props = decode(model, vocab, it["text"], max_passes=max_passes, thresh=thresh)
        tp, fp, fn = score_proposals(props, it["edits"])
        TP += tp
        FP += fp
        FN += fn
        if not it["edits"]:
            clean_sentences += 1
            if fp > 0:
                false_alert_sentences += 1
        else:
            err_sentences += 1
            if tp > 0 and fn == 0:
                caught += 1
    prec = TP / (TP + FP) if TP + FP else 0.0
    rec = TP / (TP + FN) if TP + FN else 0.0
    f05 = (1 + 0.25) * prec * rec / (0.25 * prec + rec) if prec + rec else 0.0
    return {
        "precision": prec, "recall": rec, "f05": f05, "tp": TP, "fp": FP, "fn": FN,
        "false_alert_rate": false_alert_sentences / max(1, clean_sentences),
        "clean_n": clean_sentences, "err_n": err_sentences,
        "err_fully_corrected": caught / max(1, err_sentences),
    }


def train(model_name, epochs=10, batch=48, resume=None, seed=0):
    torch.manual_seed(seed)
    train_items = load_split("train")
    dev_items = load_split("dev")
    auth = [x for x in train_items if x["origin"].startswith("authored")]
    train_items = train_items + auth * 3  # authored x4 weight
    print(f"train={len(train_items)} dev={len(dev_items)} (authored upweighted x4)")
    vocab, edit_freq = Vocab.build(train_items)
    print(f"vocab: words={vocab.n_words} edits={len(vocab.edit2id)}")
    coverage = 0
    total = 0
    for it in train_items:
        for e in it["edits"]:
            total += 1
            if e["rep"] and (REPLACE + e["rep"]) in vocab.edit2id:
                coverage += 1
    print(f"edit-vocab coverage of replace targets: {coverage}/{total} = {coverage/max(1,total):.3f}")

    # word-pair fallback dictionary for REPLACE_OOV (single-token pairs from train data)
    from collections import Counter
    pair_c = Counter()
    for it in train_items:
        for e in it["edits"]:
            if e["rep"]:
                o_t = e["orig"].strip().split()
                r_t = e["rep"].strip().split()
                if len(o_t) == 1 and len(r_t) == 1:
                    pair_c[(o_t[0].lower(), r_t[0].lower())] += 1
    fallback = {}
    for (o, r), c in pair_c.items():
        if c >= 1 and (o not in fallback or c > fallback[o][1]):
            fallback[o] = (r, c)
    vocab.fallback_map = {k: v[0] for k, v in fallback.items()}
    # curated morphological fallbacks (both directions for common families)
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
    print(f"fallback map: {len(vocab.fallback_map)} entries")
    model = GRUTagger(vocab) if model_name == "gru" else TinyTransformerTagger(vocab)
    nparams = sum(p.numel() for p in model.parameters())
    print(f"model={model_name} params={nparams}")
    lr = 2e-3 if model_name == "gru" else 1e-3
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)
    steps_per_epoch = (len(train_items) + batch - 1) // batch
    warmup = 200
    total_steps = steps_per_epoch * epochs

    def lr_at(step):
        if step < warmup:
            return step / max(1, warmup)
        t = (step - warmup) / max(1, total_steps - warmup)
        return max(0.05, 0.5 * (1 + math.cos(math.pi * t)))

    step = 0
    start_ep = 0
    if resume and os.path.exists(resume):
        ck = torch.load(resume, weights_only=False)
        model.load_state_dict(ck["model"])
        opt.load_state_dict(ck["opt"])
        step = ck["step"]
        start_ep = ck.get("epoch", -1) + 1
        best_f05 = ck.get("best_f05", 0.0)
        print(f"resumed at step {step} epoch {start_ep}")
    os.makedirs(CKPT, exist_ok=True)
    best_f05 = 0.0
    history = []
    keep_ids = [vocab.edit2id[KEEP]]
    nonkeep_ids = [i for i in range(len(vocab.edit2id)) if i != keep_ids[0]]
    order = list(range(len(train_items)))
    rng = torch.Generator().manual_seed(seed)
    for ep in range(start_ep, epochs):
        perm = torch.randperm(len(train_items), generator=rng).tolist()
        model.train()
        t0 = time.time()
        losses = []
        for bi in range(0, len(perm), batch):
            if step >= total_steps:
                break
            chunk = [train_items[i] for i in perm[bi:bi + batch]]
            feats = [vocab.featurize(it["text"]) for it in chunk]
            toks = [tokenize(it["text"]) for it in chunk]
            lengths = [len(f) for f in feats]
            targets = []
            for it in feats:
                pass
            # labels
            tgt = []
            for it in chunk:
                ids = vocab.labels_for(it["text"], it["edits"])
                tgt.append(ids)
            B = len(chunk)
            T = max(lengths)
            tgt_t = torch.zeros(B, T, dtype=torch.long)
            for b in range(B):
                for i, v in enumerate(tgt[b]):
                    tgt_t[b, i] = v
            for g in opt.param_groups:
                g["lr"] = lr * lr_at(step)
            logits = model(feats, toks, lengths)
            # weighted CE: non-KEEP tokens get extra weight
            # length-based padding mask (KEEP is edit id 0 — never mask by id!)
            mask = torch.zeros(B, T, dtype=torch.float)
            for b in range(B):
                mask[b, :lengths[b]] = 1.0
            w = mask * torch.where(tgt_t == keep_ids[0], 1.0, 6.0)
            loss = (F.cross_entropy(logits.reshape(-1, logits.size(-1)),
                                    tgt_t.reshape(-1), reduction="none").reshape(B, T) * w).sum() / w.sum()
            opt.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 3.0)
            opt.step()
            losses.append(float(loss))
            step += 1
        metrics = evaluate(model, vocab, dev_items, thresh=0.0)
        history.append({"epoch": ep, "loss": sum(losses) / max(1, len(losses)),
                        "dev": metrics, "time": time.time() - t0})
        print(f"ep {ep} loss {sum(losses)/max(1,len(losses)):.4f} "
              f"dev P={metrics['precision']:.3f} R={metrics['recall']:.3f} "
              f"F05={metrics['f05']:.3f} FA={metrics['false_alert_rate']:.3f} "
              f"({time.time()-t0:.0f}s)")
        ck = {"model": model.state_dict(), "opt": opt.state_dict(), "step": step,
              "epoch": ep, "best_f05": best_f05, "vocab_words": vocab.word2id,
              "vocab_edits": vocab.id2edit}
        torch.save(ck, os.path.join(CKPT, f"{model_name}_last.pt"))
        if metrics["f05"] > best_f05:
            best_f05 = metrics["f05"]
            torch.save(ck, os.path.join(CKPT, f"{model_name}_best.pt"))
            with open(os.path.join(CKPT, f"{model_name}_best.json"), "w") as f:
                json.dump({"epoch": ep, "dev_metrics": metrics}, f)
    with open(os.path.join(CKPT, f"{model_name}_history.json"), "w") as f:
        json.dump(history, f)
    return model, vocab


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="gru", choices=["gru", "transformer"])
    ap.add_argument("--epochs", type=int, default=10)
    ap.add_argument("--resume", default=None)
    ap.add_argument("--eval-only", action="store_true")
    args = ap.parse_args()
    if args.eval_only:
        ck = torch.load(args.resume, weights_only=False)
        vocab = Vocab(ck["vocab_words"], ck["vocab_edits"])
        model = GRUTagger(vocab) if args.model == "gru" else TinyTransformerTagger(vocab)
        model.load_state_dict(ck["model"])
        dev_items = load_split("dev")
        print(json.dumps(evaluate(model, vocab, dev_items), indent=1))
    else:
        train(args.model, epochs=args.epochs, resume=args.resume)

# -*- coding: utf-8 -*-
"""Exports the selected model + rules + fallback to a self-contained JS worker.

Steps:
1. int8 symmetric quantization (per-tensor for GRU/linear, per-row for embeddings).
2. Emit engine94.js: tokenizer (identical regex), featurizer, GRU forward pass,
   rules engine (rules.json semantics), tagger decode, protected-span guards,
   Harper-format findings output.
3. Emit data blocks: weights (base64), vocab, rules, fallback.
4. Node equivalence test: JS engine findings == Python tagger_findings.
"""
import base64
import json
import os
import sys

import numpy as np
import torch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine as E
import gec_model as G
from gec_model import Vocab, GRUTagger

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "export_out")
os.makedirs(OUT, exist_ok=True)


def quantize_per_tensor(w):
    w = w.astype(np.float32)
    scale = float(np.max(np.abs(w))) / 127.0 or 1e-9
    q = np.clip(np.round(w / scale), -127, 127).astype(np.int8)
    return q, scale


def quantize_per_row(w):
    w = w.astype(np.float32)
    scales = (np.max(np.abs(w), axis=1) / 127.0)
    scales[scales == 0] = 1e-9
    q = np.clip(np.round(w / scales[:, None]), -127, 127).astype(np.int8)
    return q, scales.tolist()


def build_export():
    ck = torch.load((os.path.join(HERE, "checkpoints", "gru3_best.pt") if os.path.exists(os.path.join(HERE, "checkpoints", "gru3_best.pt")) else os.path.join(HERE, "checkpoints", "gru2_best.pt")), weights_only=False)
    vocab = Vocab(ck["vocab_words"], ck["vocab_edits"])
    net = GRUTagger(vocab, hidden=ck.get("hidden", 192))
    net.load_state_dict(ck["model"])
    net.eval()

    from run_comparison import attach_fallback
    attach_fallback(vocab)

    sd = net.state_dict()
    parts = {}

    def add(name, tensor, per_row=False):
        arr = tensor.detach().cpu().numpy()
        if per_row:
            q, scales = quantize_per_row(arr)
            parts[name] = {"shape": list(arr.shape), "q": q, "scales": scales}
        else:
            q, scale = quantize_per_tensor(arr)
            parts[name] = {"shape": list(arr.shape), "q": q, "scale": scale}

    add("word_emb", sd["enc.word_emb.weight"], per_row=True)
    add("hash_suf", sd["enc.hash_suf.weight"], per_row=True)
    add("hash_pre", sd["enc.hash_pre.weight"], per_row=True)
    add("proj_w", sd["enc.proj.weight"])
    add("proj_b", sd["enc.proj.bias"])
    add("gru_w_ih", sd["gru.weight_ih_l0"])
    add("gru_w_hh", sd["gru.weight_hh_l0"])
    add("gru_b_ih", sd["gru.bias_ih_l0"])
    add("gru_b_hh", sd["gru.bias_hh_l0"])
    add("gru_w_ih_r", sd["gru.weight_ih_l0_reverse"])
    add("gru_w_hh_r", sd["gru.weight_hh_l0_reverse"])
    add("gru_b_ih_r", sd["gru.bias_ih_l0_reverse"])
    add("gru_b_hh_r", sd["gru.bias_hh_l0_reverse"])
    add("out_w", sd["out.weight"])
    add("out_b", sd["out.bias"])

    # pack weights into one binary blob: int8 arrays + float32 scales
    blob = bytearray()
    meta = {}
    for name, p in parts.items():
        q = p["q"].tobytes()
        off = len(blob)
        blob.extend(q)
        entry = {"off": off, "n": p["q"].size, "shape": p["shape"]}
        if "scale" in p:
            entry["scale"] = p["scale"]
        else:
            entry["scales"] = p["scales"]
        meta[name] = entry
    wbytes = base64.b64encode(bytes(blob)).decode()

    data = {
        "words": vocab.word2id,
        "edits": vocab.id2edit,
        "fallback": vocab.fallback_map,
        "weights": meta,
        "threshold": 0.995,
    }
    with open(os.path.join(OUT, "engine94_weights.b64"), "w") as f:
        f.write(wbytes)
    with open(os.path.join(OUT, "engine94_data.json"), "w") as f:
        json.dump(data, f, separators=(",", ":"))
    rules = json.load(open(os.path.join(HERE, "rules2.json")))
    with open(os.path.join(OUT, "engine94_rules.json"), "w") as f:
        json.dump(rules, f, separators=(",", ":"))
    print("exported:", len(blob), "bytes int8,", len(wbytes), "b64 chars")
    print("vocab words:", len(vocab.word2id), "edits:", len(vocab.id2edit))
    return net, vocab, data


if __name__ == "__main__":
    build_export()

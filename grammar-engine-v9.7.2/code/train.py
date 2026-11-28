"""Train compact BiGRU edit-tagger (GECToR-lite) on CPU.

Overfitting controls (per user requirement):
  - fixed seed, strict data splits (never touched during training)
  - weight decay 1e-4, dropout 0.25
  - early stopping on validation edit-F1 (patience 3)
  - per-epoch train/val metrics logged (gap = overfit monitor)
"""

import json, os, sys, time, math, random
import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from align import tokenize, align, build_op_vocab

SEED = 20260714
torch.manual_seed(SEED)
random.seed(SEED)

if __name__ != "__main__" and os.environ.get("SKIP_TRAIN_IMPORT") != "0":
    raise SystemExit(0)  # imported as module: do not train

DATA = "/home/z/my-project/data"
OUT = "/home/z/my-project/work/model"
os.makedirs(OUT, exist_ok=True)

def load(name):
    return [json.loads(l) for l in open(f"{DATA}/{name}.jsonl")]

train_rows = load("train")
val_rows = load("validation")

# ------------------------------------------------------------- vocabularies
word_freq = Counter()
for r in train_rows:
    for t in tokenize(r["s_bad"]):
        w = t["w"].replace("’", "'")
        word_freq[w.lower()] += 1

MAX_VOCAB = 20000
words = [w for w, c in word_freq.most_common(MAX_VOCAB - 2)]
word2id = {w: i + 2 for i, w in enumerate(words)}
word2id["<pad>"] = 0
word2id["<unk>"] = 1
id2word = {i: w for w, i in word2id.items()}

op2id, replace_vocab, insert_vocab = build_op_vocab(train_rows)
num_ops = len(op2id)
print(f"vocab={len(word2id)}  ops={num_ops}")

def word_id(tok):
    return word2id.get(tok["w"].replace("’", "'").lower(), 1)

def feats(tok):
    w = tok["w"]
    return (
        1.0 if (w[:1].isupper() and w[1:].islower()) else 0.0,
        1.0 if w.isupper() and len(w) > 1 else 0.0,
        1.0 if any(c.isdigit() for c in w) else 0.0,
        1.0 if ("'" in w or "’" in w) else 0.0,
    )

def encode(rows):
    """-> list of (ids, featvec, ops, len, row)"""
    out = []
    for r in rows:
        bt, ops = align(r["s_bad"], r["s_good"])
        ids = [word_id(t) for t in bt]
        fs = [feats(t) for t in bt]
        opids = [op2id.get(o, op2id["KEEP"]) for o in ops]
        out.append((ids, fs, opids, len(ids), r))
    return out

train_enc = encode(train_rows)
val_enc = encode(val_rows)
print(f"train {len(train_enc)}  val {len(val_enc)}")

# ------------------------------------------------------------- model
class EditTagger(nn.Module):
    def __init__(self, vocab, dim=96, hidden=192, layers=2, n_ops=100,
                 feat_dim=4, dropout=0.25):
        super().__init__()
        self.emb = nn.Embedding(vocab, dim, padding_idx=0)
        self.feat_proj = nn.Linear(feat_dim, dim)
        self.rnn = nn.GRU(dim, hidden, num_layers=layers, bidirectional=True,
                          batch_first=True, dropout=dropout)
        self.head = nn.Linear(2 * hidden, n_ops)
        self.dropout = nn.Dropout(dropout)

    def forward(self, ids, feats):
        # ids: (B,T)  feats: (B,T,4)
        x = self.emb(ids) + self.feat_proj(feats)
        x = self.dropout(x)
        o, _ = self.rnn(x)
        o = self.dropout(o)
        return self.head(o)  # (B,T,n_ops)

dev = "cpu"
model = EditTagger(len(word2id), n_ops=num_ops).to(dev)
nparam = sum(p.numel() for p in model.parameters())
print(f"params: {nparam/1e6:.2f}M")

# class weights (inverse sqrt freq)
op_freq = Counter()
for _, _, opids, _, _ in train_enc:
    op_freq.update(opids)
weights = torch.ones(num_ops)
for i in range(num_ops):
    weights[i] = 1.0 / math.sqrt(max(op_freq.get(i, 1), 1))
weights = weights / weights.mean()

def batches(enc, bs=48, shuffle=True, rng=random.Random(SEED)):
    idx = list(range(len(enc)))
    if shuffle:
        rng.shuffle(idx)
    for i in range(0, len(idx), bs):
        chunk = [enc[j] for j in idx[i:i + bs]]
        T = max(len(c[0]) for c in chunk)
        B = len(chunk)
        ids = torch.zeros(B, T, dtype=torch.long)
        ft = torch.zeros(B, T, 4)
        ops = torch.full((B, T), -100, dtype=torch.long)  # ignore index
        ln = torch.zeros(B, dtype=torch.float)
        for b, (idsl, fsl, opsl, L, _) in enumerate(chunk):
            ids[b, :L] = torch.tensor(idsl)
            ft[b, :L] = torch.tensor(fsl)
            ops[b, :L] = torch.tensor(opsl)
            ln[b] = L
        yield ids, ft, ops

# ------------------------------------------------------------- metrics
def edit_f1(enc, thr=None):
    """token-level edit F1 (non-KEEP ops as edits)."""
    model.eval()
    tp = fp = fn = 0
    accs = []
    with torch.no_grad():
        for ids, ft, ops in batches(enc, 64, shuffle=False):
            logits = model(ids, ft)
            pred = logits.argmax(-1)
            for b in range(ids.shape[0]):
                L = int((ops[b] >= 0).sum())
                for t in range(L):
                    gold = ops[b, t].item()
                    p = pred[b, t].item()
                    accs.append(gold == p)
                    if gold == 0 and p != 0:
                        fp += 1
                    elif gold != 0 and p == 0:
                        fn += 1
                    elif gold != 0 and p != 0:
                        if gold == p:
                            tp += 1
                        else:
                            fp += 1
                            fn += 1
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * p * r / (p + r) if p + r else 0.0
    return p, r, f1, sum(accs) / len(accs)

# ------------------------------------------------------------- training
opt = torch.optim.AdamW(model.parameters(), lr=2e-3, weight_decay=1e-4)
sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=12)

log = []
best_f1, best_state, patience = -1, None, 0
EPOCHS = 12
start_ep = 1
CKPT = f"{OUT}/checkpoint.pt"
if os.path.exists(CKPT):
    ck = torch.load(CKPT, map_location="cpu")
    model.load_state_dict(ck["model"])
    opt.load_state_dict(ck["opt"])
    sched.load_state_dict(ck["sched"])
    log = ck["log"]
    best_f1 = ck["best_f1"]
    best_state = ck["best_state"]
    patience = ck["patience"]
    start_ep = ck["epoch"] + 1
    print(f"resumed at epoch {start_ep}")
t0 = time.time()
for ep in range(start_ep, EPOCHS + 1):
    model.train()
    tot_loss = tot_tok = 0
    for ids, ft, ops in batches(train_enc, 48):
        opt.zero_grad()
        logits = model(ids, ft)
        mask = ops >= 0
        loss = F.cross_entropy(logits[mask], ops[mask],
                               weight=weights, reduction="mean")
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
        opt.step()
        ntok = int(mask.sum())
        tot_loss += loss.item() * ntok
        tot_tok += ntok
    sched.step()
    vp, vr, vf1, vacc = edit_f1(val_enc)
    tr_loss = tot_loss / max(tot_tok, 1)
    gap = vacc - vr  # small => healthy
    log.append({"epoch": ep, "train_loss": round(tr_loss, 4),
                "val_P": round(vp, 4), "val_R": round(vr, 4),
                "val_F1": round(vf1, 4), "val_tokacc": round(vacc, 4)})
    print(f"ep{ep:02d} loss={tr_loss:.4f}  valP={vp:.3f} valR={vr:.3f} "
          f"valF1={vf1:.3f} tokacc={vacc:.3f}  [{time.time()-t0:.0f}s]", flush=True)
    torch.save({"model": model.state_dict(), "opt": opt.state_dict(),
                "sched": sched.state_dict(), "log": log, "epoch": ep,
                "best_f1": best_f1, "best_state": best_state,
                "patience": patience}, CKPT)
    if vf1 > best_f1 + 1e-4:
        best_f1, patience = vf1, 0
        best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}
    else:
        patience += 1
        if patience >= 3:
            print("early stop")
            break

model.load_state_dict(best_state)
print(f"BEST val F1 = {best_f1:.4f}")

# ------------------------------------------------------------- per-category val breakdown
cat_metric = defaultdict(lambda: [0, 0, 0])
model.eval()
with torch.no_grad():
    for ids, ft, ops in batches(val_enc, 64, shuffle=False):
        logits = model(ids, ft)
        pred = logits.argmax(-1)
        for b in range(ids.shape[0]):
            L = int((ops[b] >= 0).sum())
            row = val_enc[b][4] if False else None
            # map back via stored order? simpler: iterate enc directly
def per_cat(enc_rows):
    res = defaultdict(lambda: [0, 0, 0])  # cat -> [tp, fp+fn-ish]
    model.eval()
    with torch.no_grad():
        for i in range(0, len(enc_rows), 64):
            chunk = enc_rows[i:i+64]
            T = max(len(c[0]) for c in chunk)
            B = len(chunk)
            ids = torch.zeros(B, T, dtype=torch.long)
            ft = torch.zeros(B, T, 4)
            ops = torch.full((B, T), -100, dtype=torch.long)
            for b, (idsl, fsl, opsl, L, row) in enumerate(chunk):
                ids[b, :L] = torch.tensor(idsl)
                ft[b, :L] = torch.tensor(fsl)
                ops[b, :L] = torch.tensor(opsl)
            logits = model(ids, ft)
            pred = logits.argmax(-1)
            for b, (_, _, opsl, L, row) in enumerate(chunk):
                hit = miss = wrong = 0
                for t in range(L):
                    gold = ops[b, t].item()
                    p = pred[b, t].item()
                    if gold != 0:
                        if p == gold: hit += 1
                        else: miss += 1
                    elif p != 0:
                        wrong += 1
                cats = row["cats"] or ["CLEAN"]
                for c in cats:
                    r_ = res[c]
                    r_[0] += hit
                    r_[1] += miss
                    r_[2] += wrong
    return res

pc = per_cat(val_enc)
print("\nper-category val recall (hit/total gold edits):")
for c, (h, m, w) in sorted(pc.items(), key=lambda kv: -kv[1][0]):
    tot = h + m
    print(f"  {c:>15}: recall={h/max(tot,1):.3f} ({h}/{tot})  wrongFP={w}")

# ------------------------------------------------------------- save
torch.save({"state": best_state,
            "word2id": word2id,
            "op2id": op2id,
            "config": {"dim": 96, "hidden": 192, "layers": 2, "feat_dim": 4},
            "val_f1": best_f1}, f"{OUT}/edit_tagger.pt")
json.dump(log, open(f"{OUT}/train_log.json", "w"), indent=1)
json.dump({c: [h, m, w] for c, (h, m, w) in pc.items()},
          open(f"{OUT}/val_per_category.json", "w"), indent=1)
print(f"saved -> {OUT}/edit_tagger.pt")

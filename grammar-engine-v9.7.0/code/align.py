"""Token alignment: (s_bad, s_good, edits) -> token-level ops for tagging.

Ops:
  KEEP                     token is correct
  DELETE                   remove token
  CASE_CAP                 capitalize first letter
  CASE_LOW                 lowercase first letter
  REPLACE__<word>          replace token with word (word from REPLACE_VOCAB)
  INSERT__<word>           insert word AFTER this token (word from INSERT_VOCAB)

Tokenizer keeps char offsets so ops can be rendered back to char spans.
"""

import re, difflib, json
from collections import Counter, defaultdict

TOKEN_RE = re.compile(r"[A-Za-z'’]+|\d+(?:[.,]\d+)*|[^\sA-Za-z\d]")

def tokenize(s):
    toks = []
    for m in TOKEN_RE.finditer(s):
        toks.append({"w": m.group(0), "s": m.start(), "e": m.end()})
    return toks

def _norm(t):
    # normalise curly apostrophe to straight for matching
    return t.replace("’", "'")

def align(bad, good):
    """Return (bad_tokens, ops) where ops[i] is the op for bad_tokens[i]."""
    bt = tokenize(bad)
    gt = tokenize(good)
    bw = [_norm(t["w"]) for t in bt]
    gw = [_norm(t["w"]) for t in gt]
    ops = ["KEEP"] * len(bt)
    sm = difflib.SequenceMatcher(a=bw, b=gw, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        if tag == "replace":
            n_a, n_b = i2 - i1, j2 - j1
            n = min(n_a, n_b)
            for k in range(n):
                a_w, b_w = bw[i1 + k], gw[j1 + k]
                if a_w.lower() == b_w.lower() and a_w != b_w:
                    if a_w[0].islower() and b_w[0].isupper():
                        ops[i1 + k] = "CASE_CAP"
                    else:
                        ops[i1 + k] = "CASE_LOW"
                else:
                    ops[i1 + k] = "REPLACE__" + gw[j1 + k]
            for k in range(n, n_a):
                ops[i1 + k] = "DELETE"
        elif tag == "delete":
            for k in range(i1, i2):
                ops[k] = "DELETE"
        elif tag == "insert":
            # attach insertions to the token before the insertion point
            for k in range(j1, j2):
                anchor = i1 - 1
                if anchor < 0:
                    anchor = 0
                    # insertion at start: attach to token 0 as INSERT__ then
                    # the inserted token actually precedes; encode as
                    # REPLACE__<first good token> + DELETE is wrong; use
                    # INSERT__ on token 0 with note BEFORE
                    ops[anchor] = "INSERTB__" + gw[k]
                else:
                    ops[anchor] = "INSERT__" + gw[k]
    return bt, ops

def collect_vocab(rows):
    """Top REPLACE/INSERT target words across data."""
    rep, ins = Counter(), Counter()
    for r in rows:
        bt, ops = align(r["s_bad"], r["s_good"])
        for o in ops:
            if o.startswith("REPLACE__"):
                rep[o[9:]] += 1
            elif o.startswith("INSERT__"):
                ins[o[8:]] += 1
            elif o.startswith("INSERTB__"):
                ins[o[9:]] += 1
    return rep, ins

def build_op_vocab(rows, max_replace=400, max_insert=200):
    rep, ins = collect_vocab(rows)
    replace_vocab = [w for w, _ in rep.most_common(max_replace)]
    insert_vocab = [w for w, _ in ins.most_common(max_insert)]
    base = ["KEEP", "DELETE", "CASE_CAP", "CASE_LOW"]
    op_ids = list(base)
    for w in replace_vocab:
        op_ids.append("REPLACE__" + w)
    for w in insert_vocab:
        op_ids.append("INSERT__" + w)
        op_ids.append("INSERTB__" + w)
    op2id = {o: i for i, o in enumerate(op_ids)}
    return op2id, replace_vocab, insert_vocab

if __name__ == "__main__":
    rows = [json.loads(l) for l in open("/home/z/my-project/data/train.jsonl")]
    op2id, rv, iv = build_op_vocab(rows)
    print("num ops:", len(op2id))
    # coverage check: fraction of examples fully encodable
    full, partial = 0, 0
    missing = Counter()
    for r in rows:
        bt, ops = align(r["s_bad"], r["s_good"])
        if all(o in op2id for o in ops):
            full += 1
        else:
            partial += 1
            for o in ops:
                if o not in op2id:
                    missing[o] += 1
    print(f"fully encodable: {full}/{len(rows)}  partial: {partial}")
    print("top missing:", missing.most_common(12))
    # demonstrate alignment on samples
    import random
    rng = random.Random(3)
    for r in rng.sample([x for x in rows if not x["clean"]], 10):
        bt, ops = align(r["s_bad"], r["s_good"])
        marked = " ".join(f"{t['w']}[{o if o != 'KEEP' else ''}]" for t, o in zip(bt, ops))
        print(" ", marked, "  ->  ", r["s_good"])

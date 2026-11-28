# -*- coding: utf-8 -*-
"""Engine evaluation harness.

Engines (all offline, measured on the same held-out data):
  none      : no-change baseline
  harper    : the original build's Harper WASM (via Node harness)
  t5        : the original build's T5-Efficient-tiny ONNX (via onnxruntime)
  rules     : deterministic rule layer (rules.json)
  tagger    : trained neural tagger (GRU or transformer checkpoint)
  taggerR   : rules + tagger cascade (my complete engine)
  combined  : Harper + my complete engine (product-level combination)

Metrics: span-level precision/recall/F0.5, false-alert rate on clean sentences,
meaning-preservation on adversarial sentences, per-type breakdown.
"""
import json
import os
import re
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corrupt as C
from gec_model import Vocab, GRUTagger, TinyTransformerTagger

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data_built")
CKPT = os.path.join(HERE, "checkpoints")
PROT = C.PROTECT_RE


def load_split(name):
    return [json.loads(l) for l in open(os.path.join(DATA, name + ".jsonl"))]


# ---------------------------------------------------------------- rules engine
def rules_findings(text, spec):
    """Deterministic rule proposals on `text`. Protected-span aware, dedup overlaps."""
    out = []
    prot = [(m.start(), m.end()) for m in PROT.finditer(text)]
    for rule in spec["rules"]:
        flags = re.I if rule.get("case") == "i" else 0
        for m in re.finditer(rule["re"], text, flags):
            g = rule["apply"].get("group") or 0
            guard = rule.get("guard")
            if guard:
                if guard.get("end") and not text.rstrip().endswith(guard["end"]):
                    continue
                ng = guard.get("not_group")
                if ng and m.group(ng) and m.group(ng).lower() in [w.lower() for w in guard.get("words", [])]:
                    continue
                pn = guard.get("prev_not")
                if pn and m.start() > 0:
                    words = [t.group(0).lower() for t in re.finditer(r"[A-Za-z]+", text[:m.start()])]
                    prevtok = words[-1] if words else None
                    prev2 = words[-2] if len(words) >= 2 else None
                    import re as _r
                    if (prevtok and prevtok in [w.lower() for w in pn]) or \
                       (prev2 and _r.fullmatch(r"(%s)" % 'my|our|their|his|her|its|your|the|a|an|this|that|these|those|all|some|both|several|many|few|most|other|such|each|any|no|one|two|three|four|five|six|seven|eight|nine|ten', prevtok) and prev2 in [w.lower() for w in pn]):
                        continue
                if guard.get("no_plural") and m.group(g or 1) and m.group(g or 1).endswith("s"):
                    continue
                nc = guard.get("no_camel")
                if nc and m.group(nc) and re.search(r"[A-Z]", m.group(nc)[1:]):
                    continue
                fi = guard.get("first_in")
                if fi and m.group(0).split()[0].lower() in [w.lower() for w in fi]:
                    continue
                if guard.get("min_words") and len(text.split()) < guard["min_words"]:
                    continue
                pr = guard.get("prev_re")
                if pr:
                    re_str = pr if isinstance(pr, str) else pr.get("re", "")
                    window = (pr.get("window", 50) if isinstance(pr, dict)
                              else guard.get("window", 50))
                    seg = text[max(0, m.start() - window):m.start()]
                    try:
                        if not re.search(re_str, seg, re.I):
                            continue
                    except re.error:
                        continue
                pnr = guard.get("prev_not_re")
                if pnr:
                    re_str = pnr if isinstance(pnr, str) else pnr.get("re", "")
                    window = (pnr.get("window", 30) if isinstance(pnr, dict)
                              else guard.get("window", 30))
                    seg = text[max(0, m.start() - window):m.start()]
                    try:
                        if re.search(re_str, seg, re.I):
                            continue
                    except re.error:
                        continue
            span = m.span(g)
            if any(span[0] < pe and ps < span[1] for ps, pe in prot):
                continue
            kind = rule["apply"]["kind"]
            rep = None
            if kind == "map":
                key = m.group(g)
                mp = rule["apply"]["map"]
                rep = mp.get(key)
                if rep is None and key.islower():
                    rep = mp.get(key.capitalize())
                if rep is None and key.istitle():
                    low = mp.get(key.lower())
                    rep = _title_like(low) if low else None
                if rep is None:
                    continue
                if rep == m.group(g):
                    continue  # no-op self-map: never emit a non-edit
            elif kind == "template":
                rep = rule["apply"].get("template", "")
                groups = m.groups()
                for gi in range(1, len(groups) + 1):
                    rep = rep.replace("{%d}" % gi, m.group(gi) or "")
                span = (m.start(), m.end())
            elif kind == "to_of_ing":
                # "capable to fix" -> "capable of fixing"
                gg = rule["apply"].get("group") or 2
                w = m.group(gg)
                ger = (w[:-1] + "ing") if (len(w) > 2 and w.endswith("e") and not w.endswith("ee")) else w + "ing"
                rep = (m.group(1) or "") + " of " + ger
                span = (m.start(), m.end())
            elif kind == "g_ing":
                gs, ge = m.span(g)
                span = (gs, ge)
                w = m.group(g)
                # drop a single trailing 'e' (but never 'ee'): receive -> receiving
                rep = (w[:-1] + "ing") if (len(w) > 2 and w.endswith("e") and not w.endswith("ee")) else w + "ing"
            elif kind == "del_next":
                gs, ge = m.span(g)
                if ge < len(text) and text[ge] == " ":
                    ge += 1
                span = (gs, ge)
                rep = ""
            elif kind == "period_end":
                if not text.strip() or not re.match(r"^[A-Z]", text.strip()):
                    continue
                e = len(text.rstrip())
                span = (e, e)
                rep = "."
            elif kind == "capfirst":
                rep = text[0].upper()
                span = (m.start(), m.start() + 1)
            elif kind == "dup":
                w = m.group(0)
                span = (m.start() + len(w) // 2, m.end())
                rep = ""
            elif kind == "suffix_ing":
                rep = m.group(0) + "ing"
            elif kind == "swap":
                toks = m.group(0).split()
                rep = toks[0] + " " + toks[2] + " " + toks[1]
            if rep is None:
                continue
            out.append({"start": span[0], "end": span[1], "rep": rep,
                        "type": rule["type"], "src": "rule:" + rule["id"]})
    # dedup overlapping (keep first per span, drop later overlapping)
    out.sort(key=lambda x: (x["start"], x["end"]))
    kept = []
    for f in out:
        if any(f["start"] < k["end"] and k["start"] < f["end"] for k in kept):
            continue
        kept.append(f)
    return kept


def _title_like(low):
    parts = low.split(" ")
    return " ".join(p[:1].upper() + p[1:] for p in parts if p != "")


# ---------------------------------------------------------------- tagger engine
def load_tagger(model="gru", checkpoint=None):
    ck = torch_load(os.path.join(CKPT, (checkpoint or (model + "_best.pt"))))
    vocab = Vocab(ck["vocab_words"], ck["vocab_edits"])
    net = GRUTagger(vocab) if model == "gru" else TinyTransformerTagger(vocab)
    net.load_state_dict(ck["model"])
    net.eval()
    return net, vocab


def torch_load(path):
    import torch
    return torch.load(path, weights_only=False)


def tagger_findings(net, vocab, text, thresh, max_passes=2):
    """Neural tagger proposals with fallback dictionary for OOV replaces."""
    import torch
    import torch.nn.functional as F
    from gec_model import tokenize, tokenize_with_offsets, KEEP, DELETE, CASE_CAP, REPLACE, INSERT, APPEND, REPLACE_OOV
    cur = text
    fb = getattr(vocab, "fallback_map", None) or {}
    prot = [(m.start(), m.end()) for m in PROT.finditer(text)]
    for _p in range(max_passes):
        toks = tokenize_with_offsets(cur)
        feats = [vocab.featurize(cur)]
        with torch.no_grad():
            logits = net(feats, [[t for (t, a, b) in toks]], [len(feats[0])])
        probs = F.softmax(logits[0], dim=-1)
        ops = []
        edited = False
        for i in range(1, len(toks) + 1):
            tag_id = int(probs[i].argmax())
            p = float(probs[i][tag_id])
            tag = vocab.id2edit[tag_id]
            if tag == KEEP or p < thresh:
                continue
            tok, ts, te = toks[i - 1]
            if any(ts < pe and ps < te for ps, pe in prot):
                continue
            if tag == DELETE:
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
                if re.match(r"^[A-Za-z']+$", tok):
                    rep = fb.get(tok.lower())
                    if rep and rep != tok:
                        ops.append((ts, te, _case_like(tok, rep)))
                        edited = True
            elif tag.startswith(REPLACE):
                rep = tag[len(REPLACE):]
                ops.append((ts, te, _case_like(tok, rep)))
                edited = True
            elif tag.startswith(INSERT):
                ops.append((ts, ts, tag[len(INSERT):] + " "))
                edited = True
            elif tag.startswith(APPEND):
                pos = te
                pad = " " if (pos < len(cur) and cur[pos] not in " .,!?") else ""
                ops.append((pos, pos, tag[len(APPEND):] + pad))
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
    ops = C.diff_edits(text, cur)
    return [{"start": s, "end": e, "rep": r, "type": "tagger", "src": "tagger", "p": 1.0}
            for (s, e, r) in ops]


def _case_like(src, rep):
    if src[0].isupper() and rep[0].isalpha():
        return rep[0].upper() + rep[1:]
    return rep


# ---------------------------------------------------------------- T5 baseline
_T5 = None


def t5_load():
    global _T5
    import onnxruntime as ort
    from tokenizers import Tokenizer
    work = os.path.join(HERE, "..", "work")
    enc = ort.InferenceSession(os.path.join(work, "proof933_encoder.bin"),
                               providers=["CPUExecutionProvider"])
    dec = ort.InferenceSession(os.path.join(work, "proof933_decoder.bin"),
                               providers=["CPUExecutionProvider"])
    tok = Tokenizer.from_file(os.path.join(work, "proof933_tokenizer.bin"))
    _T5 = (enc, dec, tok)
    return _T5


def t5_correct(text):
    enc, dec, tok = _T5 or t5_load()
    ids = tok.encode(text).ids
    if not ids:
        return text
    if ids[-1] != 1:
        ids.append(1)
    if len(ids) > 128:
        raise ValueError("too long")
    inp = np.array([ids], dtype=np.int64)
    att = np.ones_like(inp)
    enc_out = enc.run(None, {"input_ids": inp, "attention_mask": att})
    hidden = enc_out[0]
    generated = [0]
    for _step in range(min(144, len(ids) + 24)):
        d_in = np.array([generated], dtype=np.int64)
        feeds = {}
        for name in [i.name for i in dec.get_inputs()]:
            if "attention_mask" in name:
                feeds[name] = att
            elif "hidden_states" in name:
                feeds[name] = hidden
            elif name.endswith("input_ids"):
                feeds[name] = d_in
            else:
                raise ValueError(name)
        res = dec.run(None, feeds)
        logits = [o for o in res if hasattr(o, "shape") and o.ndim == 3][0]
        nxt = int(np.argmax(logits[0][-1]))
        if nxt == 1:
            break
        generated.append(nxt)
    out_ids = [i for i in generated[1:]]
    corrected = tok.decode(out_ids, skip_special_tokens=True)
    return corrected.strip()


def t5_findings(text):
    corrected = t5_correct(text)
    if not corrected or corrected == text:
        return []
    ops = C.diff_edits(text, corrected)
    return [{"start": s, "end": e, "rep": r, "type": "t5", "src": "t5"} for (s, e, r) in ops]


# ---------------------------------------------------------------- Harper
_HARPER = {}


def harper_findings(text, language):
    key = (text, language)
    if key in _HARPER:
        return _HARPER[key]
    raise RuntimeError("use harper_batch for bulk; single call via node -e")


def normalize_harper(findings):
    """Harper lints -> engine proposal format (first suggestion)."""
    out = []
    for h in findings:
        sugg = h.get("suggestions") or []
        if not sugg or not isinstance(sugg[0], str):
            continue
        out.append({"start": h["start"], "end": h["end"], "rep": sugg[0],
                    "type": h.get("kind", "harper").lower(), "src": "harper:" + (h.get("rule") or "")})
    return out




# ---------------------------------------------------------------- Harper FP reduction
# Curated dictionary additions (NZ English, te reo Māori terms, workplace words)
# fed to Harper as personal-dictionary entries; plus shape-based suppression of
# spelling/typo findings on proper-noun-like and initialism tokens.
NZ_LEXICON = [
    "hui", "marae", "waka", "ama", "kai", "kaupapa", "whanau", "iwi", "hapu",
    "koha", "kōrero", "korero", "mihi", "waiata", "hāngī", "hangi", "kūmara",
    "kumara", "pavlova", "tramping", "tramp", "jandals", "chilly-bin", "togs",
    "dairy", "section", "paddock", "mate", "kauri", "pohutukawa", "rimu",
    "tui", "weka", "kereru", "weta", "kekeno", "kina", "tuatara", "moa",
    "Aotearoa", "Kāinga", "kainga", "Whanganui", "Rotorua", "Taupo", "Naseby",
    "Ōtākou", "Otakou", "Poneke", "Taranaki", "Waikato", "Northland", "Coromandel",
    "Wairarapa", "Maramarua", "Waihou", "Ngaio", "Kāpiti", "Kapiti", "Hokitika",
    "fitout", "prizegiving", "wetsuits", "cross subsidisation", "boxbed", "flatwhite",
    "longdrop", "batch", "crib", "tamariki", "rangatahi", "kaumatua", "kuia",
    "wānanga", "wananga", "pōtae", "potae", "kaiawhina", "manuhiri", "tangata",
    "whenua", "moana", "awa", "maunga", "rohe", "hapori", "kura", "punua",
    "Matariki", "Puanga", "Tangaroa", "Tāne", "Tane", "Tāmaki", "Tamaki",
    "Aroha", "Anahera", "Ihirangi", "Hemi", "Rewa", "Tama", "Sione", "Mei",
    "Amita", "Srinivasan", "Sandhu", "Chandra", "Fatima", "Yusuf", "Alvaro",
    "Nadia", "Kenji", "Priya", "Sione", "Kofi", "Ihaia", "Selma", "Ngaio",
]

MAORI_DET = {"Te", "Ngā", "Nga", "He", "Ki", "A", "O", "I", "Na", "Kei"}
_SUPPRESS_EXTRA = ["rostered", "annum", "relocks", "relock", "whaikorero", "wetsuits",
                   "fitout", "prizegiving", "kaumatua", "tangata", "whenua", "moana",
                   "shoulda", "yous", "fiord", "fiords", "wether", "heatpump",
                   "aeroengineer", "Taupō", "Āpirana", "Ngā", "Māori", "wētā",
                   "weta", "kōura", "pāua", "Tūī", "kākā", "kekeno", "Matariki",
                   "Puanga", "Whanganui", "Ōtautahi", "Tāmaki", "Aotearoa"]
INFORMAL_STARTERS = {"we", "them", "yous", "that", "no", "yeah", "nah", "hey",
                     "aye", "im", "ive", "id", "cant", "wont", "dont", "doesnt",
                     "aint", "gonna", "wasnt", "arent", "wouldnt", "couldnt",
                     "shouldnt", "shes", "hes", "theyre", "youre", "lets", "hows",
                     "whats", "cant", "sweet", "choice", "true", "fair", "true", "righto"}
NZ_SUPPRESS_SET = set(NZ_LEXICON) | set(_SUPPRESS_EXTRA)


def f_rep(h):
    return h.get("rep") or (h.get("suggestions") or [""])[0] or ""


def harper_filter(findings, text):
    """Suppress demonstrably unreliable Harper findings (measured FP classes).
    - spelling/typo/wordchoice findings on all-caps or digit-bearing initialisms
      (SH2, AGM, GST, PB) and on proper-noun-like tokens mid-sentence or after
      title initials, incl. possessives (Amita's)
    - Māori determiner constructs (Te Waihou) and lowercase te reo words are
      handled via the personal dictionary instead
    - capitalization fixes at sentence start (capital is correct) and inside
      file paths/extensions (auth.py)
    - WhomSubjectOfVerb when whom follows a preposition (fronted object)
    Trade-offs measured on dev: see results_dev_harper.json."""
    import re as _re
    out = []
    toks = list(_re.finditer(r"[A-Za-z]+", text))
    for h in findings:
        kind = (h.get("type") or h.get("kind") or "").lower()
        rule = (h.get("rule") or (h.get("src") or "").split(":", 1)[-1] or "")
        frag = text[h["start"]:h["end"]]
        # all-caps / digit initialisms: suppress for spelling/typo/wordchoice
        if kind in ("spelling", "typo", "wordchoice") and _re.match(r"^[A-Z0-9]{2,6}$", frag):
            continue
        # curated NZ / te reo / dictionary-gap words: suppress (incl. possessives)
        base = frag.rstrip("'s") if frag.endswith("'s") else frag
        if kind in ("spelling", "typo", "wordchoice") and (frag in NZ_SUPPRESS_SET or base in NZ_SUPPRESS_SET):
            continue
        # capitalization at sentence start: only suppress LOWERCASING suggestions
        if kind == "capitalization" and h["start"] == 0 and f_rep(h).islower():
            continue
        # informal sentence starters: valid casual style, do not capitalise
        if kind == "capitalization" and h["start"] == 0:
            first = text[: h["end"]].strip().split()[0].lower() if text[:h["end"]].strip() else ""
            if first in INFORMAL_STARTERS:
                continue
        # style/enhancement suggestions are out of scope for the grammar engine
        if kind in ("enhancement", "style", "miscellaneous"):
            continue
        # capitalization right after a no-space dot or slash (paths, extensions)
        if kind == "capitalization" and h["start"] > 0 and text[h["start"] - 1] in "./":
            continue
        # capitalized proper-noun-like token (incl. possessives)
        if kind in ("spelling", "typo") and _re.match(r"^[A-Z][a-z]{2,}(?:'s)?$", frag):
            idx = None
            for i, m in enumerate(toks):
                if m.start() == h["start"]:
                    idx = i
                    break
            if idx is not None and idx > 0:
                # mid-sentence or after title initial -> name; suppress
                continue
            if idx == 0 and frag in MAORI_DET:
                nxt = toks[1].group(0) if len(toks) > 1 else ""
                if nxt and nxt[0].isupper():
                    continue
        # Māori determiner construct anywhere (Te Waihou)
        if kind in ("spelling", "typo") and frag in MAORI_DET:
            k = None
            for i, m in enumerate(toks):
                if m.start() == h["start"]:
                    k = i
                    break
            if k is not None and k + 1 < len(toks) and toks[k + 1].group(0)[0].isupper():
                continue
        # whom-subject rule after preposition (fronted object)
        if rule == "WhomSubjectOfVerb":
            pre = text[max(0, h["start"] - 30):h["end"] + 2]
            if _re.search(r"(?:^|\s)(?:to|for|with|from|by|of)\s+whom\b", pre, _re.I):
                continue
        out.append(h)
    return out

def harper_batch(items, language_field="variety"):
    """Run Harper over items (dicts with text+variety). Returns list of findings lists."""
    proc = subprocess.run(
        ["node", os.path.join(HERE, "harper_batch.js")],
        input="\n".join(json.dumps({"id": i, "text": it["text"],
                                    "language": "GB" if it.get(language_field) in ("GB", "NZ") else "US",
                                    })
                        for i, it in enumerate(items)),
        capture_output=True, text=True, cwd=HERE, timeout=3000)
    out = {}
    for line in proc.stdout.splitlines():
        if not line.strip():
            continue
        d = json.loads(line)
        out[d["id"]] = normalize_harper(d.get("findings", []))
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr[:400])
    return [out.get(i, []) for i in range(len(items))]


# ---------------------------------------------------------------- combined engine
def combined_findings(text, variety, net, vocab, tagger_thresh, spec, harper):
    """My full engine = rules + tagger(threshold); combined with Harper:
    Harper findings kept, my non-overlapping additions merged (Harper wins overlaps)."""
    rules = rules_findings(text, spec)
    tagg = tagger_findings(net, vocab, text, tagger_thresh) if tagger_thresh < 1 else []
    mine = []
    used = []
    for f in rules + tagg:
        if any(f["start"] < h["end"] or h["start"] < f["end"] for h in harper):
            # overlap guard (simplified below with precise check)
            pass
        if any(f["start"] < h["end"] and h["start"] < f["end"] for h in harper):
            continue
        if any(f["start"] < u["end"] and u["start"] < f["end"] for u in mine):
            continue
        mine.append(f)
    return harper + mine


# ---------------------------------------------------------------- scoring
_NORM = lambda x: re.sub(r"\s+", " ", x).strip().lower()


def _apply_edit(text, s, e, rep):
    return text[:s] + rep + text[e:]


def score(proposals, gold_edits, text):
    """Equivalent-effect matching: a proposal is TP if applying it to the text
    yields the same corrected text as applying a gold edit (whitespace-normalised),
    or if it exactly matches a gold (span, replacement)."""
    if not gold_edits:
        return 0, len(proposals), 0
    gold_effects = set()
    for g in gold_edits:
        gold_effects.add(_NORM(_apply_edit(text, g["start"], g["end"], g["rep"])))
        gold_effects.add((g["start"], g["end"], g["rep"].strip().lower()))
    tp = fp = 0
    used = []
    for f in proposals:
        eff = _NORM(_apply_edit(text, f["start"], f["end"], f["rep"]))
        key = (f["start"], f["end"], f["rep"].strip().lower())
        hit = eff in gold_effects or key in gold_effects
        if hit:
            tp += 1
            used.append(f)
        else:
            fp += 1
    # recall side: gold edits covered by any proposal effect
    covered = 0
    for g in gold_edits:
        geff = _NORM(_apply_edit(text, g["start"], g["end"], g["rep"]))
        gkey = (g["start"], g["end"], g["rep"].strip().lower())
        if any(_NORM(_apply_edit(text, f["start"], f["end"], f["rep"])) == geff
               or (f["start"], f["end"], f["rep"].strip().lower()) == gkey for f in proposals):
            covered += 1
    fn = len(gold_edits) - covered
    return tp, fp, fn


def evaluate_engine(get_findings, items, name, per_type=False):
    TP = FP = FN = 0
    fa = clean_n = 0
    err_n = fully = 0
    type_hits = {}
    meaning_violations = []
    for it in items:
        props = get_findings(it)
        tp, fp, fn = score(props, it["edits"], it["text"])
        TP += tp
        FP += fp
        FN += fn
        if per_type:
            for f in props:
                type_hits.setdefault(f.get("type", "?"), [0, 0])
                type_hits[f.get("type", "?")][1] += 1
            for f in props:
                k = (f["start"], f["end"], f["rep"].strip().lower())
                if k in {(e["start"], e["end"], e["rep"].strip().lower()) for e in it["edits"]}:
                    type_hits.setdefault(f.get("type", "?"), [0, 0])[0] += 1
        if not it["edits"]:
            clean_n += 1
            if fp > 0:
                fa += 1
            if it.get("origin") == "adversarial" and len(props) > 0:
                meaning_violations.append((it["text"], props[:2]))
        else:
            err_n += 1
            if fn == 0 and tp > 0:
                fully += 1
    prec = TP / (TP + FP) if TP + FP else 0.0
    rec = TP / (TP + FN) if TP + FN else 0.0
    f05 = (1 + 0.25) * prec * rec / (0.25 * prec + rec) if prec + rec else 0.0
    res = {
        "engine": name, "precision": prec, "recall": rec, "f05": f05,
        "tp": TP, "fp": FP, "fn": FN,
        "false_alert_rate": fa / max(1, clean_n),
        "clean_n": clean_n, "err_n": err_n,
        "fully_corrected": fully / max(1, err_n),
        "meaning_violations": len(meaning_violations),
        "adversarial_n": sum(1 for x in items if x.get("origin") == "adversarial"),
    }
    if per_type:
        res["per_type"] = {k: (v[0], v[1]) for k, v in type_hits.items()}
    return res


if __name__ == "__main__":
    spec = json.load(open(os.path.join(HERE, "rules.json")))
    dev = load_split("dev")
    net, vocab = load_tagger("gru")
    # attach fallback
    from collections import Counter
    train = load_split("train")
    pair_c = Counter()
    for it in train:
        for e in it["edits"]:
            if e["rep"]:
                o = e["orig"].strip().split()
                r = e["rep"].strip().split()
                if len(o) == 1 and len(r) == 1:
                    pair_c[(o[0].lower(), r[0].lower())] += 1
    vocab.fallback_map = {o: r for (o, r) in pair_c}
    import gec_model as G
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

    harp = harper_batch(dev)
    results = []
    results.append(evaluate_engine(lambda it: [], dev, "none"))
    results.append(evaluate_engine(lambda it, i=_: [], dev, "none"))
    results.append(evaluate_engine(lambda it: harp[dev.index(it)], dev, "harper"))
    results.append(evaluate_engine(lambda it: t5_findings(it["text"]), dev, "t5"))
    results.append(evaluate_engine(lambda it: rules_findings(it["text"], spec), dev, "rules"))
    for th in (0.9, 0.95):
        results.append(evaluate_engine(lambda it: tagger_findings(net, vocab, it["text"], th), dev, f"tagger@{th}"))
    results.append(evaluate_engine(lambda it: rules_findings(it["text"], spec) + tagger_findings(net, vocab, it["text"], 0.95), dev, "rules+tagger@0.95"))
    results.append(evaluate_engine(lambda it, i=_: combined_findings(it["text"], it["variety"], net, vocab, 0.95, spec, harp[dev.index(it)]), dev, "harper+mine"))
    for r in results:
        print(json.dumps(r, default=str))

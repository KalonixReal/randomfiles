# -*- coding: utf-8 -*-
"""Shared token/tag pipeline + both candidate models (biGRU and tiny transformer).
GECToR-style per-token edit tagging over a fixed edit vocabulary.

Tokenization MUST match the JS engine implementation exactly (documented in the
exported engine code)."""
import json
import math
import os
import re
import sys

import torch
import torch.nn as nn
import torch.nn.functional as F

TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)*|[.,!?;:\"()]")


def tokenize(text):
    return TOKEN_RE.findall(text)


def tokenize_with_offsets(text):
    return [(m.group(0), m.start(), m.end()) for m in TOKEN_RE.finditer(text)]


KEEP = "$KEEP"
DELETE = "$DELETE"
CASE_CAP = "$CASE_CAP"
REPLACE = "REPLACE_"
INSERT = "INSERT_"
APPEND = "APPEND_"
REPLACE_OOV = "$REPLACE_OOV"
SPECIALS = [KEEP, DELETE, CASE_CAP, REPLACE_OOV]


def edit_label(tags, tag):
    return tag



VERB_BASES = ["walk", "talk", "run", "write", "read", "send", "make", "give", "take",
              "find", "know", "go", "do", "watch", "finish", "reach", "return", "arrive",
              "report", "receive", "play", "work", "study", "live", "need", "want", "use",
              "help", "call", "visit", "travel", "look", "seem", "become", "win", "lose",
              "eat", "speak", "teach", "learn", "lead", "grow", "build", "buy", "think",
              "drive", "sing", "hold", "meet", "keep", "sleep", "spend", "bring", "sit",
              "stand", "understand", "begin", "start", "join", "follow", "move", "pass",
              "review", "complete", "collect", "install", "deliver", "submit", "confirm",
              "attend", "check", "book", "cancel", "file", "sign", "share", "print"]
IRREG = {"go": ["went", "gone"], "do": ["did", "done"], "see": ["saw", "seen"],
         "eat": ["ate", "eaten"], "take": ["took", "taken"], "give": ["gave", "given"],
         "write": ["wrote", "written"], "run": ["ran", "run"], "come": ["came", "come"],
         "get": ["got", "gotten"], "make": ["made", "made"], "buy": ["bought", "bought"],
         "bring": ["brought", "brought"], "teach": ["taught", "taught"],
         "catch": ["caught", "caught"], "find": ["found", "found"],
         "speak": ["spoke", "spoken"], "swim": ["swam", "swum"], "sing": ["sang", "sung"],
         "win": ["won", "won"], "lose": ["lost", "lost"], "send": ["sent", "sent"],
         "build": ["built", "built"], "feel": ["felt", "felt"], "sleep": ["slept", "slept"],
         "grow": ["grew", "grown"], "know": ["knew", "known"], "drive": ["drove", "driven"],
         "begin": ["began", "begun"], "break": ["broke", "broken"], "choose": ["chose", "chosen"],
         "lead": ["led", "led"], "spend": ["spent", "spent"], "think": ["thought", "thought"],
         "hold": ["held", "held"], "meet": ["met", "met"], "keep": ["kept", "kept"],
         "leave": ["left", "left"], "read": ["read", "read"], "sit": ["sat", "sat"],
         "stand": ["stood", "stood"], "understand": ["understood", "understood"]}
BE_FORMS = ["is", "are", "was", "were", "am", "be", "been", "being"]
HAVE_FORMS = ["has", "have", "had"]
DO_FORMS = ["does", "do", "did", "done"]
HOMOPHONE_SWAPS = [("their", "there"), ("there", "their"), ("their", "they're"),
                   ("they're", "their"), ("there", "they're"), ("its", "it's"),
                   ("it's", "its"), ("your", "you're"), ("you're", "your"),
                   ("then", "than"), ("than", "then"), ("loose", "lose"),
                   ("past", "passed"), ("quiet", "quite"), ("weather", "whether"),
                   ("whether", "weather"), ("advice", "advise"), ("advise", "advice"),
                   ("affect", "effect"), ("effect", "affect"), ("except", "accept"),
                   ("accept", "except"), ("to", "too"), ("everyday", "every day")]
# contraction expansions for tags
CONTR_EXPAND = [("dont", "don't"), ("doesnt", "doesn't"), ("didnt", "didn't"),
                ("cant", "can't"), ("wont", "won't"), ("isnt", "isn't"),
                ("arent", "aren't"), ("wasnt", "wasn't"), ("werent", "weren't"),
                ("couldnt", "couldn't"), ("shouldnt", "shouldn't"), ("wouldnt", "wouldn't"),
                ("im", "I'm"), ("ive", "I've"), ("ill", "I'll"), ("id", "I'd"),
                ("hes", "he's"), ("shes", "she's"), ("theyre", "they're"),
                ("youre", "you're"), ("lets", "let's"), ("thats", "that's"),
                ("whats", "what's"), ("whos", "who's"), ("theyll", "they'll"),
                ("weve", "we've"), ("shouldve", "should've"), ("couldve", "could've"),
                ("wouldve", "would've"), ("idve", "")]
CONTR_EXPAND = [x for x in CONTR_EXPAND if x[1]]
ARTICLES = [("a", "an"), ("an", "a")]
PRONOUN_FIX = [("me", "I"), ("I", "me"), ("her", "she"), ("hisself", "himself"),
               ("themself", "themselves"), ("who", "whom"), ("whom", "who")]
PLURAL_FIX = [("childs", "children"), ("peoples", "people"), ("informations", "information"),
              ("equipments", "equipment"), ("advices", "advice"), ("staffs", "staff"),
              ("trainings", "training"), ("furnitures", "furniture")]

def _curated_tags():
    tags = []
    for b in VERB_BASES:
        if b.endswith(("s", "x", "z", "ch", "sh", "o")):
            s3 = b + "es"
        elif b.endswith("y") and len(b) > 1 and b[-2] not in "aeiou":
            s3 = b[:-1] + "ies"
        else:
            s3 = b + "s"
        tags.append("REPLACE_" + s3)   # base -> 3sg
        tags.append("REPLACE_" + b)     # 3sg -> base (via OOV-ish; also direct)
        tags.append("REPLACE_" + b + "ing")
        tags.append("REPLACE_" + b + "ed")
    for b, forms in IRREG.items():
        for f in forms:
            tags.append("REPLACE_" + f)
        tags.append("REPLACE_" + b)
    for w in BE_FORMS + HAVE_FORMS + DO_FORMS:
        tags.append("REPLACE_" + w)
    for a, b in HOMOPHONE_SWAPS + CONTR_EXPAND + ARTICLES + PRONOUN_FIX + PLURAL_FIX:
        tags.append("REPLACE_" + a)
        tags.append("REPLACE_" + b)
        tags.append("INSERT_" + b)
        tags.append("APPEND_" + b)
    # frequent insert words
    for w in ["to", "the", "a", "an", "is", "are", "was", "were", "of", "on", "in",
              "at", "for", "with", "have", "has", "had", "be", "been", "not", "will",
              "would", "can", "could", "do", "does", "did", "their", "there", "they",
              "he", "she", "it", "we", "you", "I", "me", "my", "our", "its", "his", "her"]:
        t = "INSERT_" + w
        if t not in tags:
            tags.append(t)
        t2 = "APPEND_" + w
        if t2 not in tags:
            tags.append(t2)
    return [t for t in tags if t.count("_") >= 1 and len(t) > 8]

CURATED_EDIT_TAGS = _curated_tags()


class Vocab:
    """Holds word vocab, char-hash params, and edit vocabulary."""

    def __init__(self, word2id, edit_list):
        self.word2id = word2id
        self.edit2id = {t: i for i, t in enumerate(edit_list)}
        self.id2edit = list(edit_list)
        self.n_words = len(word2id)

    @staticmethod
    def build(examples, max_words=24000, min_edit_freq=4, max_edits=900):
        word_freq = {}
        edit_freq = {}
        for ex in examples:
            for w in tokenize(ex["text"]):
                word_freq[w.lower()] = word_freq.get(w.lower(), 0) + 1
            for e in ex["edits"]:
                rep = e["rep"]
                if rep:
                    edit_freq[rep] = edit_freq.get(rep, 0) + 1
        words = sorted([w for w, c in word_freq.items() if c >= 2],
                       key=lambda w: -word_freq[w])[:max_words]
        word2id = {"<pad>": 0, "<unk>": 1, "<s>": 2, "</s>": 3}
        for w in words:
            word2id.setdefault(w, len(word2id))
        edit_list = list(SPECIALS)
        # curated morphological/homophone replacement tags first
        for tag in CURATED_EDIT_TAGS:
            if tag not in edit_list:
                edit_list.append(tag)
        reps = sorted([r for r, c in edit_freq.items() if c >= 2],
                      key=lambda r: -edit_freq[r])[:max_edits]
        # single-token replaces + multi-token replaces allowed (<=3 tokens, <=24 chars)
        for r in reps:
            toks = tokenize(r)
            if not toks or len(toks) > 3 or len(r) > 24:
                continue
            if any(not re.match(r"[A-Za-z0-9']", t) for t in toks):
                continue
            tag = REPLACE + r
            if tag not in edit_list:
                edit_list.append(tag)
        for r in reps:  # inserts after replaces to balance
            toks = tokenize(r)
            if len(toks) == 1 and len(r) <= 12 and re.match(r"^[A-Za-z0-9']+$", r):
                for tag in (INSERT + r, APPEND + r):
                    if tag not in edit_list:
                        edit_list.append(tag)
        return Vocab(word2id, edit_list), edit_freq

    # ---------------- features

    def token_features(self, tok):
        wl = tok.lower()
        wid = self.word2id.get(wl, 1)
        # char hashes: suffix and prefix
        suf = wl[-4:]
        pre = wl[:3]
        h_suf = (int(hashlib_light(suf)) & 4095) if suf else 0
        h_pre = (int(hashlib_light(pre)) & 4095) if pre else 0
        return (wid, h_suf, h_pre)

    def featurize(self, text):
        toks = ["<s>"] + tokenize(text) + ["</s>"]
        feats = []
        for t in toks:
            if t in ("<s>", "</s>"):
                feats.append((self.word2id[t], 0, 0))
                continue
            feats.append(self.token_features(t))
        return feats

    # ---------------- labeling

    def labels_for(self, text, edits):
        """Tag sequence for the tokens of `text` given ground-truth `edits`
        (spans on text). Returns list of tag ids aligned with featurize(text) tokens
        (incl. <s>/</s>)."""
        toks = tokenize_with_offsets(text)
        tags = [KEEP] * (len(toks) + 2)  # <s> + tokens + </s>
        for e in edits:
            s, en, rep, orig = e["start"], e["end"], e["rep"], e["orig"]
            if en == s:  # insertion at s
                idx = None
                for i, (t, ts, te) in enumerate(toks):
                    if ts >= s:
                        idx = i + 1  # +1 for <s>
                        break
                rep_clean = rep.strip()
                rep_toks = tokenize(rep_clean)
                tag = None
                if len(rep_toks) == 1:
                    if idx is None:
                        tag = APPEND + rep_clean
                    else:
                        tag = INSERT + rep_clean
                if tag and tag in self.edit2id and idx is not None and idx < len(tags):
                    tags[idx] = tag
                elif idx is not None and idx < len(tags):
                    tags[idx] = REPLACE_OOV if tags[idx] == KEEP else tags[idx]
                continue
            # find tokens overlapping [s, en)
            first = None
            for i, (t, ts, te) in enumerate(toks):
                if ts < en and te > s:
                    if first is None:
                        first = i
            if first is None:
                continue
            i1 = first + 1
            if rep == "":
                for i in range(i1, i1 + 1):
                    if i < len(tags):
                        tags[i] = DELETE
                # multi-token delete: mark covered tokens
                for i, (t, ts, te) in enumerate(toks):
                    if ts >= s and te <= en and tags[i + 1] == KEEP:
                        tags[i + 1] = DELETE
                continue
            if orig.lower() == rep.strip().lower() and len(orig) == len(rep.strip()):
                if i1 < len(tags):
                    tags[i1] = CASE_CAP
                continue
            tag = REPLACE + rep.strip()
            PUNCT = re.match(r"^[.,!?;:\"()]+$", orig.strip())
            if tag in self.edit2id and not PUNCT:
                if i1 < len(tags):
                    tags[i1] = tag
            elif PUNCT:
                pass  # punctuation edits stay KEEP (handled by dedicated rules)
            else:
                if i1 < len(tags):
                    tags[i1] = REPLACE_OOV
        return [self.edit2id[t] for t in tags]


def hashlib_light(s):
    h = 5381
    for ch in s:
        h = ((h << 5) + h + ord(ch)) & 0xFFFFFFFF
    return h % 1000003


# ---------------------------------------------------------------- feature dims
WORD_EMB = 64
HASH_EMB = 8
SHAPE_DIM = 8
FEAT_DIM = WORD_EMB + 2 * HASH_EMB + SHAPE_DIM


def shape_flags(tok):
    if not tok or tok in ("<s>", "</s>", "<pad>"):
        return [0, 0, 0, 0, 0, 1, 0, 0]
    caps = tok[0].isupper()
    allcaps = tok.isupper() and len(tok) > 1
    has_digit = any(c.isdigit() for c in tok)
    is_punct = bool(re.match(r"^[.,!?;:\"()]$", tok))
    ln = min(len(tok), 12)
    return [int(caps), int(allcaps), int(has_digit), int(is_punct),
            ln / 12.0, 0, int(tok == "<s>"), int(tok == "</s>")]


class FeatureEncoder(nn.Module):
    def __init__(self, vocab):
        super().__init__()
        self.vocab = vocab
        self.word_emb = nn.Embedding(vocab.n_words + 4, WORD_EMB, padding_idx=0)
        self.hash_suf = nn.Embedding(4096, HASH_EMB)
        self.hash_pre = nn.Embedding(4096, HASH_EMB)
        self.proj = nn.Linear(FEAT_DIM, 96)

    def forward(self, feats, lengths):
        # feats: list of lists of (wid, hsuf, hpre) -> padded tensor [B, T]
        # feats[b] includes <s> and </s>; toks (self._toks) excludes them: align +1.
        B = len(feats)
        T = max(lengths)
        wid = torch.zeros(B, T, dtype=torch.long)
        hs = torch.zeros(B, T, dtype=torch.long)
        hp = torch.zeros(B, T, dtype=torch.long)
        shape = torch.zeros(B, T, SHAPE_DIM)
        toks_cache = self._toks
        for b, (f, toks) in enumerate(zip(feats, toks_cache)):
            full = ["<s>"] + list(toks) + ["</s>"]
            for i, (w, s_, p_) in enumerate(f):
                wid[b, i] = w if w < self.word_emb.num_embeddings else 1
                hs[b, i] = s_ & 4095
                hp[b, i] = p_ & 4095
                if i < len(full):
                    shape[b, i] = torch.tensor(shape_flags(full[i]), dtype=torch.float)
        e = self.word_emb(wid)
        es = self.hash_suf(hs)
        ep = self.hash_pre(hp)
        x = torch.cat([e, es, ep, shape], dim=-1)
        return self.proj(x)


class GRUTagger(nn.Module):
    """Candidate A: bidirectional GRU edit tagger."""

    def __init__(self, vocab, hidden=96):
        super().__init__()
        self.vocab = vocab
        self.enc = FeatureEncoder(vocab)
        self.gru = nn.GRU(96, hidden, num_layers=1, bidirectional=True, batch_first=True)
        self.drop = nn.Dropout(0.3)
        self.out = nn.Linear(hidden * 2, len(vocab.edit2id))

    def forward(self, feats, toks, lengths):
        self.enc._toks = toks
        x = self.enc(feats, lengths)
        out, _ = self.gru(x)
        return self.out(self.drop(out))


class TinyTransformerTagger(nn.Module):
    """Candidate B: 2-layer transformer encoder tagger."""

    def __init__(self, vocab, d=96, heads=3, ff=384, layers=2, maxlen=64):
        super().__init__()
        self.vocab = vocab
        self.enc = FeatureEncoder(vocab)
        self.pos = nn.Embedding(maxlen, 96)
        layer = nn.TransformerEncoderLayer(96, heads, ff, dropout=0.25,
                                           batch_first=True, norm_first=True,
                                           activation="gelu")
        self.tr = nn.TransformerEncoder(layer, layers)
        self.drop = nn.Dropout(0.3)
        self.out = nn.Linear(96, len(vocab.edit2id))

    def forward(self, feats, toks, lengths):
        self.enc._toks = toks
        x = self.enc(feats, lengths)
        T = x.size(1)
        pos = self.pos(torch.arange(T, device=x.device))[None]
        x = x + pos
        mask = torch.arange(T)[None] >= torch.tensor(lengths)[:, None]
        x = self.tr(x, src_key_padding_mask=mask)
        return self.out(self.drop(x))

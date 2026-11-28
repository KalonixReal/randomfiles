# -*- coding: utf-8 -*-
"""Rule-based corruption generators for training data.

Each corruption: (start, end, replacement, error_type) applied to a CLEAN sentence,
producing an erroneous sentence with exact ground-truth span.

Requirements (from the brief): recorded transformation type, preserved clean target,
reproducible randomness, limited simultaneous errors, unit tests.
"""
import difflib
import random
import re

WORD = re.compile(r"[A-Za-z0-9']+|[.,!?;:($£€%]")

# ---------------------------------------------------------------- helpers

def tokens_of(text):
    return WORD.findall(text)

def find_token_span(text, pred):
    """Return (start, end, tok) for the first token satisfying pred."""
    for m in WORD.finditer(text):
        if pred(m.group(0), m.start()):
            return m.start(), m.end(), m.group(0)
    return None

def apply_edit(text, start, end, replacement):
    return text[:start] + replacement + text[end:]

# ---------------------------------------------------------------- lexicons

IRREGULAR = {  # base -> past ; errors: past->base swap or overregularized
    "go": "went", "see": "saw", "eat": "ate", "take": "took", "give": "gave",
    "write": "wrote", "run": "ran", "come": "came", "get": "got", "make": "made",
    "buy": "bought", "bring": "brought", "teach": "taught", "catch": "caught",
    "find": "found", "speak": "spoke", "swim": "swam", "sing": "sang", "win": "won",
    "lose": "lost", "send": "sent", "build": "built", "feel": "felt", "sleep": "slept",
}
IRREGULAR_PP = {  # base -> past participle ; errors: have went style
    "go": "gone", "see": "seen", "eat": "eaten", "take": "taken", "write": "written",
    "give": "given", "do": "done", "speak": "spoken", "break": "broken", "forget": "forgotten",
    "know": "known", "grow": "grown", "begin": "begun", "drive": "driven", "choose": "chosen",
    "come": "come", "bring": "brought", "teach": "taught", "catch": "caught", "send": "sent",
}
THIRD_SING_VERBS = ["walks", "talks", "runs", "writes", "reads", "sends", "makes",
                    "gives", "takes", "finds", "knows", "goes", "does", "watches",
                    "finishes", "reaches", "returns", "arrives", "reports", "receives"]
PLURAL_SUBJ = ["they", "we", "you", "those", "people", "students", "children"]
SING_SUBJ = ["she", "he", "it", "everyone", "nobody", "somebody", "the team"]
A_VOWELS = "aeiou"
HOMOPHONES = {
    "their": "there", "there": "their", "they're": "their", "its": "it's", "it's": "its",
    "your": "you're", "you're": "your", "then": "than", "than": "then",
    "loose": "lose", "past": "passed", "quiet": "quite",
    "weather": "whether", "advice": "advise", "affect": "effect", "except": "accept",
    "everyday": "every day", "principal": "principle",
}
CONTRACTIONS_APOS = {
    "don't": "dont", "doesn't": "doesnt", "didn't": "didnt", "can't": "cant",
    "won't": "wont", "isn't": "isnt", "aren't": "arent", "wasn't": "wasnt",
    "weren't": "werent", "couldn't": "couldnt", "shouldn't": "shouldnt",
    "wouldn't": "wouldnt", "haven't": "havent", "hasn't": "hasnt", "I'm": "im",
    "I've": "ive", "I'll": "ill", "I'd": "id", "he's": "hes", "she's": "shes",
    "they're": "theyre", "we're": "were2", "you're": "youre", "it's": "its2",
    "let's": "lets", "that's": "thats", "what's": "whats", "who's": "whos",
    "he'd": "hed", "she'd": "shed", "they'll": "theyll", "you'll": "youd",
    "we've": "weve", "should've": "shouldve", "could've": "couldve", "would've": "wouldve",
}
# fix we're/it's placeholder values
CONTRACTIONS_APOS["we're"] = "were"  # ambiguous; excluded below
CONTRACTIONS_APOS["it's"] = "its"    # ambiguous; excluded below
CONTRACTIONS_APOS["you'll"] = "youll"
AMBIG_APOS = {"we're", "it's"}  # never corrupt these (post-corrupt text ambiguous)

# ---------------------------------------------------------------- generators
# each: fn(text, rng) -> (start, end, replacement, type) or None

def gen_sva_drop_s(text, rng):
    """She walks -> She walk (3rd person singular -s dropped)."""
    toks = list(WORD.finditer(text))
    cands = []
    for i, m in enumerate(toks):
        w = m.group(0)
        if w.lower() in THIRD_SING_VERBS and i > 0:
            prev = toks[i - 1].group(0).lower()
            if prev in ("she", "he", "it", "and") or prev.rstrip(".,") in ("she", "he", "it"):
                cands.append(m)
    if not cands:
        return None
    m = rng.choice(cands)
    w = m.group(0)
    if w.endswith("ies") and len(w) > 4:
        base = w[:-3] + "y"
    elif w[-3:] in ("hes", "ses", "ches", "shes", "xes", "zes", "oes", "sses"):
        base = w[:-2]
    else:
        base = w[:-1]
    if not base:
        return None
    return m.start(), m.end(), base, "sva"

def gen_sva_add_s(text, rng):
    """They walk -> They walks."""
    toks = list(WORD.finditer(text))
    cands = []
    for i, m in enumerate(toks):
        w = m.group(0).lower()
        if w in ("walk", "talk", "run", "write", "read", "send", "make", "give",
                 "take", "find", "know", "go", "do", "watch", "finish", "reach",
                 "return", "arrive", "report", "receive", "play", "work", "study",
                 "live", "need", "want", "use", "help", "call", "visit", "travel"):
            if i > 0 and toks[i - 1].group(0).lower() in PLURAL_SUBJ:
                cands.append(m)
    if not cands:
        return None
    m = rng.choice(cands)
    w = m.group(0)
    if w.endswith(("s", "x", "z", "ch", "sh", "o")):
        new = w + "es"
    elif w.endswith("y") and len(w) > 1 and w[-2] not in "aeiou":
        new = w[:-1] + "ies"
    else:
        new = w + "s"
    return m.start(), m.end(), new, "sva"

def gen_be_agreement(text, rng):
    """Swap is/are and was/were in either direction (input is clean, so any swap is an error)."""
    pairs = {"is": "are", "are": "is", "was": "were", "were": "was"}
    toks = list(WORD.finditer(text))
    cands = []
    for i, m in enumerate(toks):
        w = m.group(0).lower()
        if w in pairs and i > 0:
            prev = toks[i - 1].group(0).lower().rstrip(".,")
            pluralish = prev in PLURAL_SUBJ or (prev.endswith("s") and len(prev) > 3 and not prev.endswith("ss")) or prev in ("children", "people", "men", "women", "feet")
            singularish = prev in ("she", "he", "it", "there", "this", "that", "one", "nobody", "everyone", "somebody", "each")
            if pluralish or singularish:
                cands.append((m, pairs[w]))
    if not cands:
        return None
    m, new = rng.choice(cands)
    return m.start(), m.end(), new, "sva"

def gen_have_agreement(text, rng):
    pairs = {"has": "have", "have": "has"}
    toks = list(WORD.finditer(text))
    cands = []
    for i, m in enumerate(toks):
        w = m.group(0).lower()
        if w in pairs and i > 0:
            prev = toks[i - 1].group(0).lower().rstrip(".,")
            pluralish = prev in PLURAL_SUBJ or (prev.endswith("s") and len(prev) > 3 and not prev.endswith("ss")) or prev in ("children", "people", "men", "women")
            singularish = prev in ("she", "he", "it", "there", "nobody", "everyone", "each")
            if pluralish or singularish:
                cands.append((m, pairs[w]))
    if not cands:
        return None
    m, new = rng.choice(cands)
    return m.start(), m.end(), new, "sva"

def gen_do_agreement(text, rng):
    pairs = {"does": "do", "do": "does", "doesn't": "don't", "don't": "doesn't"}
    toks = list(WORD.finditer(text))
    cands = []
    for i, m in enumerate(toks):
        w = m.group(0).lower()
        if w in pairs and i > 0:
            prev = toks[i - 1].group(0).lower().rstrip(".,")
            pluralish = prev in PLURAL_SUBJ
            singularish = prev in ("she", "he", "it")
            if (w in ("does", "doesn't") and pluralish) or (w in ("do", "don't") and singularish):
                cands.append((m, pairs[w]))
    if not cands:
        return None
    m, new = rng.choice(cands)
    return m.start(), m.end(), new, "sva"

def gen_past_to_base(text, rng):
    """Yesterday I send -> sent is reversed: clean 'sent' -> corrupt 'send'."""
    toks = list(WORD.finditer(text))
    cands = []
    for i, m in enumerate(toks):
        w = m.group(0).lower()
        if w in IRREGULAR.values() and i > 0:
            cands.append((m, [b for b, p in IRREGULAR.items() if p == w][0]))
    if not cands:
        return None
    m, base = rng.choice(cands)
    return m.start(), m.end(), base, "tense"

def gen_past_overregular(text, rng):
    """clean 'went' -> corrupt 'goed' (overregularization)."""
    toks = list(WORD.finditer(text))
    cands = []
    for m in toks:
        w = m.group(0).lower()
        if w in IRREGULAR.values():
            cands.append((m, [b for b, p in IRREGULAR.items() if p == w][0] + "ed"))
    if not cands:
        return None
    m, new = rng.choice(cands)
    return m.start(), m.end(), new, "verbform"

def gen_pp_to_past(text, rng):
    """have gone -> have went."""
    toks = list(WORD.finditer(text))
    cands = []
    for i, m in enumerate(toks):
        w = m.group(0).lower()
        if i >= 1 and w in IRREGULAR_PP.values():
            prev = toks[i - 1].group(0).lower()
            if prev in ("have", "has", "had"):
                cands.append((m, _IRREGULAR_PP_inverse(w)))
    if not cands:
        return None
    m, new = rng.choice(cands)
    return m.start(), m.end(), new, "participle"

def _IRREGULAR_PP_inverse(w):
    for b, p in IRREGULAR_PP.items():
        if p == w:
            return IRREGULAR.get(b, b + "ed")
    return w

def gen_pp_to_base(text, rng):
    """has finished -> has finish."""
    toks = list(WORD.finditer(text))
    cands = []
    for i, m in enumerate(toks):
        w = m.group(0).lower()
        if i >= 1 and toks[i - 1].group(0).lower() in ("have", "has", "had") and w.endswith("ed") and len(w) > 4:
            cands.append(m)
    if not cands:
        return None
    m = rng.choice(cands)
    w = m.group(0)
    return m.start(), m.end(), w[:-2] if not w.endswith("ied") else w[:-3] + "y", "verbform"

def gen_modal_past(text, rng):
    """can went style: clean 'go' after modal -> 'went'."""
    toks = list(WORD.finditer(text))
    cands = []
    for i, m in enumerate(toks):
        w = m.group(0).lower()
        if i >= 1 and toks[i - 1].group(0).lower() in ("can", "will", "must", "may", "should", "would", "could"):
            if w in IRREGULAR:
                cands.append((m, IRREGULAR[w]))
            elif w.endswith("ed") and len(w) > 4:
                cands.append((m, w[:-2]))
    if not cands:
        return None
    m, new = rng.choice(cands)
    return m.start(), m.end(), new, "modal"

def gen_modal_to(text, rng):
    """must submit -> must to submit (insert 'to')."""
    toks = list(WORD.finditer(text))
    cands = []
    for i, m in enumerate(toks):
        if m.group(0).lower() in ("must", "should", "will", "can", "may") and i + 1 < len(toks):
            nxt = toks[i + 1].group(0).lower()
            if nxt == "to":
                continue
            if nxt in ("submit", "submit", "review", "confirm", "send", "return", "complete", "attend", "apply", "register", "deliver", "pay", "check", "reply", "verify", "sign", "attend"):
                cands.append(m)
    if not cands:
        return None
    m = rng.choice(cands)
    return m.end(), m.end(), " to", "modal"

def gen_article_an(text, rng):
    """a apple -> an apple / an test -> a test."""
    toks = list(WORD.finditer(text))
    cands = []
    for i, m in enumerate(toks):
        w = m.group(0).lower()
        if w in ("a", "an") and i + 1 < len(toks):
            nxt = toks[i + 1].group(0)
            if not nxt[0].isalpha():
                continue
            cands.append((m, "an" if w == "a" else "a"))
    if not cands:
        return None
    m, new = rng.choice(cands)
    return m.start(), m.end(), new, "article"

def gen_article_drop(text, rng):
    """drop 'the/a' before a mid-sentence noun."""
    toks = list(WORD.finditer(text))
    cands = []
    for i, m in enumerate(toks):
        w = m.group(0).lower()
        if w in ("the", "a", "an") and 0 < i < len(toks) - 2:
            prev = toks[i - 1].group(0).lower()
            if prev in ("to", "of", "in", "at", "for", "with", "and", "or", "on", "from", "into"):
                nxt = toks[i + 1].group(0)
                if nxt[0].isalpha() and nxt[0].islower():
                    cands.append((m, i))
    if not cands:
        return None
    m, i = rng.choice(cands)
    end = m.end()
    while end < len(text) and text[end] == " ":
        end += 1
    return m.start(), end, "", "article"

def gen_plural_noun(text, rng):
    """three file -> three files / five boxes -> five box"""
    NUMS = ("two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "several", "many", "few")
    toks = list(WORD.finditer(text))
    cands = []
    for i, m in enumerate(toks):
        if i + 1 < len(toks):
            w = m.group(0).lower()
            nxt = toks[i + 1].group(0)
            if w in NUMS and nxt[0].isalpha() and nxt[0].islower() and not nxt.endswith("s"):
                cands.append(toks[i + 1])
    if not cands:
        return None
    m = rng.choice(cands)
    w = m.group(0)
    if w.endswith(("s", "x", "z", "ch", "sh")):
        new = w + "es"
    elif w.endswith("y") and len(w) > 1 and w[-2] not in "aeiou":
        new = w[:-1] + "ies"
    else:
        new = w + "s"
    return m.start(), m.end(), new, "plural"

def gen_plural_strip(text, rng):
    """the books is fine -> corrupt 'the book is' only when followed by singular verb."""
    toks = list(WORD.finditer(text))
    cands = []
    for i, m in enumerate(toks):
        w = m.group(0)
        if i + 1 < len(toks) and w.endswith("s") and len(w) > 4 and not w.endswith("ss"):
            nxt = toks[i + 1].group(0).lower()
            if nxt in ("is", "was", "has", "does"):
                cands.append(m)
    if not cands:
        return None
    m = rng.choice(cands)
    w = m.group(0)
    new = w[:-1] if not w.endswith(("es", "ies")) else (w[:-2] if w.endswith("es") else w[:-3] + "y")
    return m.start(), m.end(), new, "plural"

def gen_pronoun_case(text, rng):
    """me and John -> my friend and I ... simplified: 'X and me' -> 'me and X'; I -> me after prep."""
    toks = list(WORD.finditer(text))
    cands = []
    for i, m in enumerate(toks):
        w = m.group(0)
        if w == "I" and i >= 2:
            if toks[i - 1].group(0).lower() == "and":
                subj = toks[i - 2].group(0)
                if subj[0].isupper() or subj.islower():
                    # "Ana and I" -> "Ana and me" (object position unknown; only when preceded by preposition)
                    j = i - 2
                    if j >= 1 and toks[j - 1].group(0).lower() in ("to", "for", "with", "from", "between"):
                        cands.append((m, "me"))
        elif w == "me" and i >= 1 and toks[i - 1].group(0).lower() in ("to", "for", "with", "from", "between"):
            pass
    if not cands:
        return None
    m, new = rng.choice(cands)
    return m.start(), m.end(), new, "pronoun"

def gen_subject_me(text, rng):
    """'My friend and I went' -> 'Me and my friend went' (start-of-sentence)."""
    m = re.match(r"(?:[A-Z][a-z]+|my|our|the) [a-z]+ and I ", text)
    if not m:
        return None
    s = m.group(0)
    parts = s.split(" and ")
    if not parts or "I " != parts[1]:
        return None
    first = parts[0]
    new = "Me and " + first.lower() if first[0].isupper() and first not in ("My", "Our", "The") else "Me and " + first
    return 0, len(s), new + " ", "pronoun"

def gen_homophone(text, rng):
    """swap a homophone that is present."""
    toks = list(WORD.finditer(text))
    cands = []
    for m in toks:
        w = m.group(0)
        wl = w.lower()
        if wl in HOMOPHONES:
            rep = HOMOPHONES[wl]
            if w[0].isupper():
                rep = rep.capitalize()
            cands.append((m, rep))
    if not cands:
        return None
    m, new = rng.choice(cands)
    return m.start(), m.end(), new, "homophone"

def gen_contraction_apos(text, rng):
    """don't -> dont (drop apostrophe)."""
    toks = list(WORD.finditer(text))
    cands = []
    for m in toks:
        w = m.group(0)
        if "'" in w and w.lower() in CONTRACTIONS_APOS and w.lower() not in AMBIG_APOS:
            cands.append((m, CONTRACTIONS_APOS[w.lower()]))
    if not cands:
        return None
    m, new = rng.choice(cands)
    return m.start(), m.end(), new, "punct"

def gen_dup_word(text, rng):
    """duplicate a short function word: 'the the'."""
    toks = list(WORD.finditer(text))
    cands = []
    for i, m in enumerate(toks):
        w = m.group(0).lower()
        if w in ("the", "a", "to", "is", "was", "will", "that", "of", "in", "on", "and") and i + 1 < len(toks):
            nxt = toks[i + 1].group(0).lower()
            if nxt != w:
                cands.append(m)
    if not cands:
        return None
    m = rng.choice(cands)
    return m.end(), m.end(), " " + m.group(0), "dup"

def gen_drop_word(text, rng):
    """drop a short function word (to/of/is/that)."""
    toks = list(WORD.finditer(text))
    cands = []
    for i, m in enumerate(toks):
        w = m.group(0).lower()
        if w in ("to", "of", "that", "is", "are", "a", "the") and 0 < i < len(toks) - 2:
            cands.append(m)
    if not cands:
        return None
    m = rng.choice(cands)
    start, end = m.start(), m.end()
    if end < len(text) and text[end] == " ":
        end += 1
    return start, end, "", "missing"

def gen_cap_lower(text, rng):
    """lowercase the first letter of the sentence, or 'I' -> 'i'."""
    cands = []
    m = re.match(r"[A-Z]", text)
    if m:
        cands.append((0, 1, text[0].lower(), "capit"))
    for m in re.finditer(r"\bi\b", text):
        cands.append((m.start(), m.end(), "i", "capit"))
    if not cands:
        return None
    s, e, new, typ = rng.choice(cands)
    return s, e, new, typ

def gen_advform(text, rng):
    """quickly -> quick (adverb to adjective before verb)."""
    ADV = ("quickly", "carefully", "immediately", "significantly", "beautifully",
           "badly", "rapidly", "sharply", "efficiently", "successfully", "quietly", "easily")
    toks = list(WORD.finditer(text))
    cands = []
    for i, m in enumerate(toks):
        w = m.group(0).lower()
        if w in ADV and i + 1 < len(toks) and toks[i + 1].group(0)[0].islower():
            cands.append((m, w[:-2]))
    if not cands:
        return None
    m, new = rng.choice(cands)
    return m.start(), m.end(), new, "advform"

def gen_preposition(text, rng):
    PREPS = {"for": "of", "on": "in", "in": "on", "at": "in", "with": "of", "about": "on", "to": "at"}
    toks = list(WORD.finditer(text))
    cands = []
    for m in toks:
        w = m.group(0).lower()
        if w in PREPS:
            cands.append((m, PREPS[w]))
    if not cands:
        return None
    m, new = rng.choice(cands)
    return m.start(), m.end(), new, "preposition"

def gen_compar_double(text, rng):
    """better -> more better."""
    toks = list(WORD.finditer(text))
    for i, m in enumerate(toks):
        w = m.group(0).lower()
        if w in ("better", "worse", "easier", "faster", "harder", "cheaper", "bigger", "smaller") and i >= 1:
            prev = toks[i - 1].group(0).lower()
            if prev != "more" and prev != "most":
                return m.start(), m.start(), "more ", "compar"
    return None

def gen_modal_of(text, rng):
    """could have -> could of (only after a modal)."""
    toks = list(WORD.finditer(text))
    for i, m in enumerate(toks):
        if m.group(0).lower() == "have" and i >= 1:
            prev = toks[i - 1].group(0).lower()
            if prev in ("could", "should", "would", "must", "might", "can't", "couldn't", "shouldn't", "wouldn't"):
                return m.start(), m.end(), "of", "homophone"
    return None

def gen_ing_after_to(text, rng):
    """used to waking -> wrong; skip. 'looking forward to see' -> 'to seeing'."""
    for m in re.finditer(r"looking forward to [a-z]+", text):
        w = m.group(0).split()[-1]
        if not w.endswith("ing") and len(w) > 4:
            return m.start() + len(m.group(0)) - len(w), m.end(), w + "ing", "verbform"
    return None

def gen_participle_adj(text, rng):
    """interested -> interesting swap after am/are/is/was/were/feel/felt... keep simple: after 'am/are/is/was/were/been/being'."""
    PART = ("interested", "boring", "excited", "confused", "surprised", "tired")
    toks = list(WORD.finditer(text))
    for i, m in enumerate(toks):
        w = m.group(0).lower()
        if w in ("bored", "excited", "confused", "surprised") and i >= 1:
            prev = toks[i - 1].group(0).lower()
            if prev in ("am", "is", "are", "was", "were", "be", "being", "been", "feel", "feels", "felt"):
                swap = {"bored": "boring", "excited": "exciting", "confused": "confusing", "surprised": "surprising"}[w]
                return m.start(), m.end(), swap, "participle"
        if w in ("boring", "exciting", "confusing", "surprising") and i >= 1:
            prev = toks[i - 1].group(0).lower()
            if prev in ("am", "feel", "feels", "felt"):
                swap = {"boring": "bored", "exciting": "excited", "confusing": "confused", "surprising": "surprised"}[w]
                return m.start(), m.end(), swap, "participle"
    return None

def gen_inversion_q(text, rng):
    """question inversion: 'Where are you going' -> 'Where you are going' (only questions)."""
    if not text.endswith("?"):
        return None
    m = re.match(r"(?:Where|What|When|Why|How|Who) (?:are|is|was|were|do|does|did|can|will|would|should) ([a-z]+ )", text)
    if not m:
        return None
    aux = m.group(0).split()[1]
    subj = m.group(1)
    # find positions
    first = text.index(aux)
    substart = first + len(aux) + 1
    return first, first + len(aux) + 1 + len(subj), subj + aux + " ", "inversion"

def gen_everyday(text, rng):
    for m in re.finditer(r"every day", text):
        return m.start(), m.end(), "everyday", "homophone"
    return None

def gen_negation_double(text, rng):
    """didn't go -> didn't went NO. Instead: 'do not have no' style double negative."""
    for m in re.finditer(r"don't have (?:any|no) ", text):
        return m.end() - 3, m.end(), "no ", "negation"
    return None

GEN_WEIGHTS = [
    (gen_sva_drop_s, 4.0), (gen_sva_add_s, 4.0), (gen_be_agreement, 4.0),
    (gen_have_agreement, 3.0), (gen_do_agreement, 2.0), (gen_past_to_base, 3.0),
    (gen_past_overregular, 1.0), (gen_pp_to_past, 2.0), (gen_pp_to_base, 2.0),
    (gen_modal_past, 2.0), (gen_modal_to, 0.6), (gen_article_an, 3.0),
    (gen_article_drop, 0.25), (gen_plural_noun, 1.5), (gen_plural_strip, 0.8),
    (gen_pronoun_case, 1.0), (gen_subject_me, 1.0), (gen_homophone, 3.0),
    (gen_contraction_apos, 2.5), (gen_dup_word, 1.2), (gen_drop_word, 0.5),
    (gen_cap_lower, 2.5), (gen_advform, 1.5), (gen_preposition, 0.8),
    (gen_compar_double, 1.0), (gen_ing_after_to, 0.8), (gen_participle_adj, 1.5),
    (gen_inversion_q, 0.8), (gen_everyday, 0.6), (gen_modal_of, 1.5),
]

ALL = [
    gen_sva_drop_s, gen_sva_add_s, gen_be_agreement, gen_have_agreement,
    gen_do_agreement, gen_past_to_base, gen_past_overregular, gen_pp_to_past,
    gen_pp_to_base, gen_modal_past, gen_modal_to, gen_article_an,
    gen_article_drop, gen_plural_noun, gen_plural_strip, gen_pronoun_case,
    gen_subject_me, gen_homophone, gen_contraction_apos, gen_dup_word,
    gen_drop_word, gen_cap_lower, gen_advform, gen_preposition,
    gen_compar_double, gen_ing_after_to, gen_participle_adj,
    gen_inversion_q, gen_everyday, gen_modal_of,
]

def diff_edits(a, b):
    """Token-aligned diff from text a to text b: list of (start, end, replacement)
    with spans on text a. Insertions are positioned at the START of the next
    token in a (or the end of a)."""
    ta = list(WORD.finditer(a))
    tb = list(WORD.finditer(b))
    wa = [m.group(0) for m in ta]
    wb = [m.group(0) for m in tb]
    sm = difflib.SequenceMatcher(None, wa, wb, autojunk=False)
    out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        if tag == "replace":
            span_start = ta[i1].start()
            span_end = ta[i2 - 1].end()
            rep = b[tb[j1].start():tb[j2 - 1].end()]
            out.append([span_start, span_end, rep])
        elif tag == "delete":
            span_start = ta[i1].start()
            span_end = ta[i2 - 1].end()
            # absorb one adjacent space so reconstruction is exact
            if span_end < len(a) and a[span_end] == " ":
                span_end += 1
            elif span_start > 0 and a[span_start - 1] == " " and (span_end >= len(a) or a[span_end] != " "):
                span_start -= 1
            out.append([span_start, span_end, ""])
        elif tag == "insert":
            rep = b[tb[j1].start():tb[j2 - 1].end()]
            if i1 < len(ta):
                pos = ta[i1].start()
                if pos == 0 or a[pos - 1] == " ":
                    rep = rep + " "
                else:
                    rep = " " + rep + " "
            else:
                pos = len(a)
                if pos == 0 or a[pos - 1] != " ":
                    rep = " " + rep
            out.append([pos, pos, rep])
    return [tuple(x) for x in out]

PROTECT_RE = re.compile(
    r"\$[\d,.]+|\b\d[\d,.]*\b|\b\d{1,2}:\d{2}\b|https?://\S+"
    r"|[\w.+-]+@[\w-]+\.[A-Za-z]+|\b(?:19|20)\d{2}\b|\b[A-Z]{2,}\d+\b")


def protected_spans(text):
    return [(m.start(), m.end()) for m in PROTECT_RE.finditer(text)]


def corrupt(text, rng, n_errors=1, exclude_spans=None):
    """Apply up to n_errors non-overlapping corruptions to CLEAN text.
    Returns (corrupted_text, edits) where each edit is
    (start, end, orig, replacement, type) with the span on the CORRUPTED text
    and the replacement taken from the clean text (ground truth)."""
    applied = []
    exclude = list(exclude_spans or [])
    cur = text
    weights = {g.__name__: w for g, w in GEN_WEIGHTS}
    pool = [g for g in ALL]
    wts = [weights.get(g.__name__, 1.0) for g in pool]
    for _ in range(n_errors):
        for _attempt in range(12):
            g = rng.choices(pool, weights=wts, k=1)[0]
            e = g(cur, rng)
            if not e:
                continue
            start, end, rep, typ = e
            if any(start < x[1] and x[0] < end for x in exclude):
                continue
            if any(start < pe and ps < end for (ps, pe) in protected_spans(cur)):
                continue
            new = apply_edit(cur, start, end, rep)
            if new == cur or not new.strip():
                continue
            applied.append(typ)
            exclude.append((start, end))
            cur = new
            break
    if cur == text:
        return text, []
    ops = diff_edits(cur, text)  # spans on corrupted text, replacements from clean
    out = []
    for i, (s, e, rep) in enumerate(ops):
        typ = applied[i] if i < len(applied) else "misc"
        out.append((s, e, cur[s:e], rep, typ))
    # verification: applying the edits to the corrupted text must rebuild the clean text
    fixed = cur
    for (s, e, o, rep, typ) in reversed(out):
        fixed = apply_edit(fixed, s, e, rep)
    assert fixed == text, (fixed, text)
    return cur, out

# ---------------------------------------------------------------- unit tests

def _tests():
    # deterministic per-generator tests
    rng = random.Random(0)
    # sva: direct generator call
    e = gen_sva_drop_s("She walks to the station.", rng)
    assert e is not None and e[2] == "walk", e
    e = gen_sva_add_s("They walk to school.", rng)
    assert e is not None and e[2].startswith("walks"), e
    # be agreement
    e = gen_be_agreement("The students are ready for the test.", rng)
    assert e is not None and e[2] == "is", e
    e = gen_be_agreement("She is at home today.", rng)
    assert e is not None and e[2] == "are", e
    # have agreement
    e = gen_have_agreement("They have finished the work.", rng)
    assert e is not None and e[2] == "has", e
    # past/participle
    e = gen_past_to_base("Yesterday I sent the letter.", rng)
    assert e is not None and e[2] == "send", e
    e = gen_pp_to_past("He has gone home.", rng)
    assert e is not None and e[2] == "went", e
    e = gen_pp_to_base("She has finished the report.", rng)
    assert e is not None and e[2] == "finish", e
    # modal
    e = gen_modal_past("You can go home now.", rng)
    assert e is not None and e[2] == "went", e
    e = gen_modal_of("You could have won.", rng)
    assert e is not None and e[2] == "of", e
    # articles
    e = gen_article_an("We bought a pear.", rng)
    assert e is not None and e[2] == "an", e
    # inversion
    e = gen_inversion_q("Where are you going tonight?", rng)
    assert e is not None, e
    # homophone case preserved
    e = gen_homophone("Their house is by the beach.", rng)
    assert e is not None and e[2].lower() in ("there", "they're"), e
    # contraction apostrophe
    e = gen_contraction_apos("I don't know the answer.", rng)
    assert e is not None and e[2] == "dont", e
    # duplicate word
    e = gen_dup_word("The report was late.", rng)
    assert e is not None and e[2].lower() == " the", e
    # corrupt() round-trip: apply edit then restore
    t, edits = corrupt("She walks to the station.", random.Random(0), exclude_spans=[])
    for (s, en, orig, rep, typ) in reversed(edits):
        t = apply_edit(t, s, en, rep)
    assert t == "She walks to the station.", t
    # determinism
    a = corrupt("They walk to school every day.", random.Random(7))
    b = corrupt("They walk to school every day.", random.Random(7))
    assert a == b
    # multiple errors bounded
    t3, e3 = corrupt("The manager has finished the report today.", random.Random(3), n_errors=3)
    assert 1 <= len(e3) <= 3, e3
    print("corrupt unit tests OK")

if __name__ == "__main__":
    _tests()
    # demo
    rng = random.Random(42)
    demos = [
        "She walks to the station every morning.",
        "They have finished their homework already.",
        "The manager will review the proposal tomorrow.",
        "We are looking forward to see the results.",
        "Where are you going after the meeting?",
        "My friend and I went to the library.",
        "The team is working quickly on the fix.",
        "I don't have any money for the bus.",
        "He has gone home for the weekend.",
        "Yesterday I sent the letter to Auckland.",
    ]
    for d in demos:
        t, e = corrupt(d, random.Random(11))
        print(f"{d!r} -> {t!r}  edits={[(x[2], x[3], x[4]) for x in e]}")

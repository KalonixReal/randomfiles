# -*- coding: utf-8 -*-
"""Builds rules.json — the shared deterministic grammar rule spec consumed by
the Python evaluation harness AND the browser engine (identical semantics).

Every rule replaces ONE captured group; maps carry case variants.
kind: "map" (group -> map[match]), "rep" (group -> fixed text),
      "capfirst", "dup" (delete second word), "suffix_ing" (add -ing),
      "swap" (wh-question reorder).
guards: {"end": "?"} requires the sentence to end with ?; "not_group"/"words"
        suppresses the match when that group's word is in the list.
"""
import json
import os
import re

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rules.json")

BASES = sorted(set(["walk", "talk", "run", "write", "read", "send", "make", "give",
                    "take", "find", "know", "say", "see", "come", "want", "need",
                    "like", "think", "play", "work", "live", "look", "feel", "seem",
                    "become", "win", "lose", "eat", "speak", "teach", "learn", "lead",
                    "grow", "build", "buy", "drive", "sing", "hold", "meet", "keep",
                    "sleep", "spend", "bring", "sit", "stand", "understand", "begin",
                    "start", "join", "follow", "move", "pass", "review", "complete",
                    "collect", "install", "deliver", "submit", "confirm", "attend",
                    "check", "book", "cancel", "file", "sign", "share", "print",
                    "open", "close", "finish", "reach", "return", "arrive", "report",
                    "receive", "borrow", "study", "travel", "call", "visit", "answer",
                    "explain", "ask", "tell", "use", "help", "prefer", "train",
                    "practise", "rehearse", "perform"]))


def s3(b):
    if b.endswith(("s", "x", "z", "ch", "sh", "o")):
        return b + "es"
    if b.endswith("y") and len(b) > 1 and b[-2] not in "aeiou":
        return b[:-1] + "ies"
    return b + "s"


S3 = {b: s3(b) for b in BASES}
PAST_BASE = {"went": "go", "saw": "see", "ate": "eat", "took": "take",
             "gave": "give", "wrote": "write", "ran": "run", "came": "come",
             "got": "get", "made": "make", "bought": "buy", "brought": "bring",
             "taught": "teach", "caught": "catch", "found": "find",
             "spoke": "speak", "swam": "swim", "sang": "sing", "won": "win",
             "lost": "lose", "sent": "send", "built": "build", "felt": "feel",
             "slept": "sleep", "knew": "know", "drove": "drive", "grew": "grow",
             "began": "begin", "chose": "choose", "broke": "break",
             "forgot": "forget", "met": "meet", "kept": "keep", "spent": "spend",
             "meant": "mean", "held": "hold", "told": "tell"}
PP_MAP = {"went": "gone", "saw": "seen", "ate": "eaten", "took": "taken",
          "gave": "given", "wrote": "written", "did": "done", "spoke": "spoken",
          "broke": "broken", "forgot": "forgotten", "knew": "known",
          "grew": "grown", "began": "begun", "drove": "driven", "chose": "chosen",
          "came": "come"}
CONTR = {"dont": "don't", "doesnt": "doesn't", "didnt": "didn't",
         "cant": "can't", "wont": "won't", "isnt": "isn't", "arent": "aren't",
         "wasnt": "wasn't", "werent": "weren't", "couldnt": "couldn't",
         "shouldnt": "shouldn't", "wouldnt": "wouldn't", "havent": "haven't",
         "hasnt": "hasn't", "hadnt": "hadn't", "im": "I'm", "ive": "I've",
         "hes": "he's", "shes": "she's",
         "theyre": "they're", "youre": "you're", "lets": "let's",
         "thats": "that's", "whats": "what's", "whos": "who's",
         "theyll": "they'll", "theyve": "they've", "weve": "we've",
         "shouldve": "should've", "couldve": "could've", "wouldve": "would've",
         "youve": "you've", "youd": "you'd", "hed": "he'd",
         "arent2": "x"}
del CONTR["arent2"]
TOO_ADJ = ["much", "many", "late", "early", "long", "short", "old", "young",
           "big", "small", "hot", "cold", "slow", "fast", "tired", "busy",
           "soon", "expensive", "cheap", "difficult", "easy", "hard", "loud",
           "quiet", "full", "empty", "heavy", "light", "far", "close",
           "bright", "dark"]
AN_EXC = ["one", "once", "united", "university", "unicorn", "uniform",
          "unique", "useful", "user", "usual", "european", "europe",
          "eucalyptus", "eulogy", "ubiquitous"]
AN_KEEP = ["hour", "honest", "honor", "honour", "heir", "herb", "honored"]
PLURAL_FIX = {"peoples": "people",
               "informations": "information", "equipments": "equipment",
               "advices": "advice", "furnitures": "furniture",
               "staffs": "staff", "trainings": "training",
               "luggages": "luggage", "feedbacks": "feedback",
               "softwares": "software", "hardwares": "hardware",
               "knowledges": "knowledge", "researches": "research",
               "homeworks": "homework", "moneys": "money",
               "fishes": "fish", "sheeps": "sheep"}
COMPAR = ["better", "worse", "easier", "faster", "harder", "cheaper",
          "bigger", "smaller", "larger", "older", "younger", "nicer",
          "cleaner", "quicker", "greater", "stronger", "weaker", "taller",
          "shorter", "longer"]
DUP_WORDS = ["the", "a", "an", "to", "of", "in", "on", "at", "for", "with",
             "is", "are", "was", "were", "will", "would", "can", "could",
             "should", "must", "might", "do", "does", "did", "has", "have",
             "had", "and", "but", "or", "not", "it", "he", "she", "we",
             "they", "i", "you", "that", "this", "there", "their", "them",
             "then", "than", "from", "by", "as", "if", "when", "how", "what",
             "which", "who", "been", "be"]

rules = []


def add(id_, re_src, apply_, type_, case="i", guard=None):
    rules.append({"id": id_, "re": re_src, "case": case, "apply": apply_,
                  "type": type_, **({"guard": guard} if guard else {})})


verbs_alt = "|".join(BASES)
s3alt = "|".join(sorted(set(S3.values())))
past_alt = "|".join(sorted(PAST_BASE))
pp_alt = "|".join(sorted(PP_MAP))
contr_alt = "|".join(sorted(CONTR))
too_alt = "|".join(TOO_ADJ)
comp_alt = "|".join(COMPAR)
dup_alt = "|".join(sorted(set(DUP_WORDS)))

# 1. subject-verb agreement (pronoun subjects)
add("sva_sing_base", r"\b(she|he|it) (" + verbs_alt + r")\b",
    {"kind": "map", "group": 2, "map": S3}, "sva")
add("sva_plur_s3", r"\b(they|we|you|i) (" + s3alt + r")\b",
    {"kind": "map", "group": 2, "map": {s3(b): b for b in BASES}}, "sva")
add("be_was_plural", r"\b(they|we|you) (was)\b",
    {"kind": "map", "group": 2, "map": {"was": "were", "Was": "Were"}}, "sva")
add("be_were_sing", r"\b(she|he|it|this|that) (were)\b",
    {"kind": "map", "group": 2, "map": {"were": "was", "Were": "Was"}}, "sva")
add("have_has", r"\b(she|he|it) (have)\b",
    {"kind": "map", "group": 2, "map": {"have": "has", "Have": "Has"}}, "sva")
add("has_have", r"\b(they|we|you|i) (has)\b",
    {"kind": "map", "group": 2, "map": {"has": "have", "Has": "Have"}}, "sva")
add("do_doesnt", r"\b(she|he|it) (don't)\b",
    {"kind": "map", "group": 2, "map": {"don't": "doesn't", "Don't": "Doesn't"}}, "sva")
add("does_dont", r"\b(they|we|you|i) (doesn't)\b",
    {"kind": "map", "group": 2, "map": {"doesn't": "don't", "Doesn't": "Don't"}}, "sva")
add("there_is_plural", r"\bthere (is|was) (many|several|some|two|three|four|five|six|seven|eight|nine|ten|few|lots|people|children|students|things|issues)\b",
    {"kind": "map", "group": 1, "map": {"is": "are", "was": "were", "Is": "Are"}}, "sva")
add("there_are_sing", r"\bthere (are|were) (a|an|one|the)\b",
    {"kind": "map", "group": 1, "map": {"are": "is", "were": "was", "Are": "Is"}}, "sva")

# 2. verb morphology
add("modal_past", r"\b(?:can|will|should|would|must|might|could|cannot|can't|won't|shouldn't|wouldn't|mustn't) (" + past_alt + r")\b",
    {"kind": "map", "group": 1, "map": PAST_BASE}, "verbform")
add("dosupport_past", r"\b(?:did|didn't|didnt|does|doesn't|doesnt|do|don't|dont) (" + past_alt + r")\b",
    {"kind": "map", "group": 1, "map": PAST_BASE}, "verbform")
add("have_pp", r"\b(?:have|has|had) (" + pp_alt + r")\b",
    {"kind": "map", "group": 1, "map": PP_MAP}, "participle")

# 3. contractions
add("contraction_apos", r"\b(" + contr_alt + r")\b",
    {"kind": "map", "group": 1, "map": CONTR}, "punct", case="i")

# 4. homophones (context-checked)
add("their_is", r"\b(their) (?:is|was)\b",
    {"kind": "map", "group": 1, "map": {"their": "there", "Their": "There"}}, "homophone")
add("there_noun", r"\b(there) (?:house|car|family|mother|father|dog|cat|book|job|parents|phone|room|office|garden|idea|report|money|homework|work)\b",
    {"kind": "map", "group": 1, "map": {"there": "their", "There": "Their"}}, "homophone")
add("its_verb_ing", r"\b(its) (?:raining|snowing|getting|going|becoming|freezing|boiling|working|looking|been|not|important|clear|possible|true|fine|great|hard|easy|okay|ok|too|so|very|just|really|time|the)\b",
    {"kind": "map", "group": 1, "map": {"its": "it's", "Its": "It's", "ITS": "IT's"}}, "homophone")
add("its_a", r"\b(its) (?:a|an|the|going to|not going to)\b",
    {"kind": "map", "group": 1, "map": {"its": "it's", "Its": "It's", "ITS": "IT's"}}, "homophone")
add("your_ing", r"\b(your) (?:going|coming|doing|being|not|welcome|right|wrong|late|tired|busy|very|so|too|just|really|the|a|an)\b",
    {"kind": "map", "group": 1, "map": {"your": "you're", "Your": "You're"}}, "homophone")
add("youre_noun", r"\b(you're) (?:house|car|family|mother|father|dog|cat|name|book|job|money|parents|phone|room|office|garden|idea)\b",
    {"kind": "map", "group": 1, "map": {"you're": "your", "You're": "Your"}}, "homophone")
add("then_after_comp", r"\b(?:" + comp_alt + r"|more|less|rather|other|no sooner) (then)\b",
    {"kind": "map", "group": 1, "map": {"then": "than", "Then": "Than"}}, "homophone")
add("to_adj", r"\b(to) (" + too_alt + r")\b",
    {"kind": "map", "group": 1, "map": {"to": "too", "To": "Too"}}, "homophone")
add("modal_of", r"\b(?:could|should|would|must|might|can|will) (of)\b",
    {"kind": "map", "group": 1, "map": {"of": "have", "Of": "Have"}}, "homophone")
add("modalnt_of", r"\b(?:could|should|would|must|might)n't (of)\b",
    {"kind": "map", "group": 1, "map": {"of": "have", "Of": "Have"}}, "homophone")
add("everyday_start", r"\b(everyday) (?:i|we|they|he|she|it|you)\b",
    {"kind": "map", "group": 1, "map": {"everyday": "every day", "Everyday": "Every day"}}, "homophone")
add("weather_decide", r"\b(weather) (?:or not|to)\b",
    {"kind": "map", "group": 1, "map": {"weather": "whether", "Weather": "Whether"}}, "homophone")
add("advise_noun", r"\b(?:my|your|his|her|our|their|some|good|excellent|useful|legal|medical|further) (advise)\b",
    {"kind": "map", "group": 1, "map": {"advise": "advice", "Advise": "Advice"}}, "homophone")

# 5. a/an
add("a_vowel", r"\b(a) ([aeiou]\w*?)\b",
    {"kind": "map", "group": 1, "map": {"a": "an", "A": "An"}}, "article",
    guard={"not_group": 2, "words": AN_EXC, "no_plural": True})
add("an_consonant", r"\b(an) ([bcdfghjklmnpqrstvwxyz]\w*)\b",
    {"kind": "map", "group": 1, "map": {"an": "a", "An": "A"}}, "article",
    guard={"not_group": 2, "words": AN_KEEP})

# 6. comparatives
add("more_compar", r"\b(more) (" + comp_alt + r")\b",
    {"kind": "map", "group": 1, "map": {"more": "", "More": ""}}, "compar")

# 7. plural fixes
plur_alt = "|".join(sorted(PLURAL_FIX))
add("plural_fix", r"\b(" + plur_alt + r")\b",
    {"kind": "map", "group": 1, "map": PLURAL_FIX}, "plural")
add("this_plural", r"\b(this) (?:books|files|folders|letters|reports|things|items|words|pages|chapters|notes|ideas|rules|guidelines|tables|figures|examples|questions|answers)\b",
    {"kind": "map", "group": 1, "map": {"this": "these", "This": "These"}}, "agr")

# 7b. plural noun subjects + singular be/aux (guarded by mass-noun and
# preposition-object exclusions)
MASS_NOUNS = ["news", "physics", "mathematics", "economics", "politics", "series",
              "species", "gymnastics", "aerobics", "measles", "mumps", "billiards",
              "darts", "dominoes", "electronics", "dynamics", "kinetics",
              "thermodynamics", "statistics", "linguistics", "informatics",
              "civics", "ethics", "classics", "analytics", "rabies", "diabetes",
              "tennis", "chess", "molasses", "billiards", "genetics", "logistics",
              "obstetrics", "pediatrics", "psychiatrics", "tactics", "aerodynamics"]
PREPS = ["about", "of", "with", "for", "from", "in", "on", "at", "by", "to",
         "near", "under", "over", "without", "within", "into", "onto", "upon",
         "during", "between", "among", "across", "against", "along", "behind",
         "beyond", "despite", "except", "inside", "outside", "past", "through",
         "throughout", "toward", "towards", "until", "up", "down", "off",
         "aboard", "beneath", "beside"]
add("plural_subj_be", r"\b([a-z]{3,}s) (was|is|has|does)\b",
    {"kind": "map", "group": 2, "map": {"was": "were", "is": "are", "has": "have",
                                        "does": "do", "Was": "Were", "Is": "Are"}},
    "sva", guard={"not_group": 1, "words": MASS_NOUNS, "prev_not": PREPS})

# 8. duplicated function words
add("dup_word", r"\b(" + dup_alt + r") \1\b",
    {"kind": "dup", "group": 0}, "dup")

# 9. capitalisation
INFORMAL_STARTERS = ["we", "them", "yous", "that", "no", "yeah", "nah", "hey",
                     "aye", "im", "ive", "id", "cant", "wont", "dont", "doesnt",
                     "aint", "gonna", "wasnt", "arent", "wouldnt", "couldnt",
                     "shouldnt", "shes", "hes", "theyre", "youre", "lets", "hows",
                     "whats", "sweet", "choice", "true", "fair", "righto", "id",
                     "wanna", "kinda", "dunno", "gotta", "lemme", "gimme"]
add("cap_start", r"^[a-z]+", {"kind": "capfirst"}, "capit", case="",
    guard={"first_in": INFORMAL_STARTERS})
add("cap_i", r"\b(i) (am|have|was|will|would|do|did|think|know|believe|hope|guess|need|want|can|could|should|may|might|see|saw|said|say)\b",
    {"kind": "map", "group": 1, "map": {"i": "I"}}, "capit", case="")

# 10. question inversion
add("q_inversion", r"^(where|what|when|why|how|who|which|whose) (you|they|we|he|she|it|i) (are|is|was|were|do|does|did|can|will|would|should|have|has|had)\b",
    {"kind": "swap", "group": 0}, "inversion", guard={"end": "?"})

# 11. fixed preposition swaps
add("responsible_of", r"\bresponsible (of)\b",
    {"kind": "map", "group": 1, "map": {"of": "for", "Of": "For"}}, "preposition")
add("depend_of", r"\b(?:depend|depends|depended) (of)\b",
    {"kind": "map", "group": 1, "map": {"of": "on", "Of": "On"}}, "preposition")
add("arrived_to", r"\b(?:arrive|arrives|arrived) (to)\b",
    {"kind": "map", "group": 1, "map": {"to": "at", "To": "At"}}, "preposition")
add("discussed_about", r"\b(?:discuss|discusses|discussed) (about)\b",
    {"kind": "map", "group": 1, "map": {"about": "", "About": ""}}, "preposition")
add("married_with", r"\b(?:married|marrying) (with)\b",
    {"kind": "map", "group": 1, "map": {"with": "to", "With": "To"}}, "preposition")
add("interested_about", r"\binterested (about)\b",
    {"kind": "map", "group": 1, "map": {"about": "in", "About": "In"}}, "preposition")
add("good_in_activity", r"\bgood (in) (?:mathematics|english|science|history|geography|physics|chemistry|biology|art|music|sport|writing|reading|coding)\b",
    {"kind": "map", "group": 1, "map": {"in": "at", "In": "At"}}, "preposition")

# 12. looking forward to + base
add("looking_fwd", r"\blooking forward to (see|meet|hear|work|visit|join|receive|read|watch|play|talk|speak|learn|start)\b",
    {"kind": "suffix_ing", "group": 0}, "verbform")

# 13. must to
add("must_to", r"\b(?:must|should|will|can|may) (to) (?:submit|review|confirm|send|return|complete|attend|apply|register|deliver|pay|check|reply|verify|sign)\b",
    {"kind": "map", "group": 1, "map": {"to": "", "To": ""}}, "modal")

with open(OUT, "w") as f:
    json.dump({"rules": rules, "version": "rules-1.0"}, f, indent=0)
print(f"rules.json written: {len(rules)} rules")


# ---------------- self-test (reference semantics)
def run_rules(text, spec):
    out = []
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
                if pn and span_start > 0:
                    prevtok = None
                    for tm in re.finditer(r"[A-Za-z]+", text[:span_start]):
                        prevtok = tm.group(0).lower()
                    if prevtok and prevtok in [w.lower() for w in pn]:
                        continue
                if guard.get("no_plural") and m.group(g or 1) and m.group(g or 1).endswith("s"):
                    continue
            span = m.span(g)
            kind = rule["apply"]["kind"]
            if kind == "map":
                key = m.group(g)
                mp = rule["apply"]["map"]
                rep = mp.get(key)
                if rep is None and key.islower():
                    rep = mp.get(key.capitalize())
                if rep is None and key.istitle():
                    rep = mp.get(key.lower())
                if rep is None:
                    continue
                out.append((span[0], span[1], rep, rule["type"]))
            elif kind == "rep":
                out.append((span[0], span[1], rule["apply"]["text"], rule["type"]))
            elif kind == "capfirst":
                out.append((0, 1, text[0].upper(), rule["type"]))
            elif kind == "dup":
                w = m.group(0)
                second = m.start() + len(w) // 2 + 1
                out.append((second - 1, m.end(), "", rule["type"]))
            elif kind == "suffix_ing":
                out.append((span[0], span[1], m.group(0) + "ing", rule["type"]))
            elif kind == "swap":
                toks = m.group(0).split()
                out.append((span[0], span[1],
                            toks[0] + " " + toks[2] + " " + toks[1], rule["type"]))
    return out


spec = json.load(open(OUT))
tests = [
    "She walk to school.",
    "They walks to school.",
    "He don't like it.",
    "They doesn't understand.",
    "I dont know the answer.",
    "Your going to love it.",
    "Their is a problem with the tap.",
    "Its raining again today.",
    "Its a beautiful day.",
    "He can went home now.",
    "We didnt saw the sign.",
    "She has went home.",
    "He have finished the report.",
    "They was late again.",
    "She were happy with it.",
    "The soup is better then the old one.",
    "It is to late to start.",
    "I could of won the race.",
    "I ate a apple and an pear.",
    "This books are overdue.",
    "The the report was late.",
    "i think its going to rain.",
    "Where you are going after class?",
    "He is responsible of the budget.",
    "It is more better then before.",
    "He must to submit the form.",
    "We are looking forward to see you.",
    "The childs were playing outside.",
    "A useful feature.",
    "I waited an hour at the station.",
    "We bought a one-day pass.",
]
for t in tests:
    rs = run_rules(t, spec)
    print(f"{t!r:52s} -> {rs}")

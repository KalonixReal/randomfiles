"""Sentence builders + corruption specs.
Each builder returns list of dicts:
  {clean, domain, cors:[{cat, find, repl}]}
`find` must be unique in the sentence (asserted by driver).
Protected tokens never appear inside `find`."""

import random
from lexicon import (VERBS, NOUNS, ADJ, ADV, SUBJ_SING, SUBJ_PL,
                     INTRO_PHRASE, TIME_PAST, TIME_FUT, PLACES,
                     MISSPELL, CONFUSABLES, DOUBLE_NEG, CONTRACT_MISS,
                     PROPER_LOWER)

R = random.Random(20260714)

def _v(base):  return VERBS[base]
def _3sg(b):   return _v(b)[0]
def _past(b):  return _v(b)[1]
def _ing(b):   return _v(b)[2]

# ---------------------------------------------------------------- SVA
def build_sva():
    out = []
    for s in SUBJ_SING:
        for b in ("have", "do", "go", "be", "watch", "play", "make"):
            if b == "be":
                clean = f"{s.capitalize()} is at the library today."
                cors = [{"cat": "sva", "find": " is ", "repl": " are "}]
            elif b == "have":
                clean = f"{s.capitalize()} has finished the homework already."
                cors = [{"cat": "sva", "find": "has", "repl": "have"}]
            elif b == "do":
                clean = f"{s.capitalize()} does not like cold coffee."
                cors = [{"cat": "sva", "find": "does not", "repl": "do not"}]
            elif b == "go":
                clean = f"{s.capitalize()} goes to the market on Saturdays."
                cors = [{"cat": "sva_3sg", "find": "goes", "repl": "go"}]
            elif b == "watch":
                clean = f"{s.capitalize()} watches the news every evening."
                cors = [{"cat": "sva_3sg", "find": "watches", "repl": "watch"}]
            elif b == "play":
                clean = f"{s.capitalize()} plays the guitar beautifully."
                cors = [{"cat": "sva_3sg", "find": "plays", "repl": "play"}]
            else:
                clean = f"{s.capitalize()} makes breakfast for the family."
                cors = [{"cat": "sva_3sg", "find": "makes", "repl": "make"}]
            out.append({"clean": clean, "domain": "essay", "cors": cors})
    for s in SUBJ_PL:
        clean = f"{s.capitalize()} were excited about the trip."
        out.append({"clean": clean, "domain": "essay",
                    "cors": [{"cat": "sva", "find": "were", "repl": "was"}]})
        clean = f"{s.capitalize()} are working on the science project."
        out.append({"clean": clean, "domain": "essay",
                    "cors": [{"cat": "sva", "find": "are", "repl": "is"}]})
    # I / you special
    out.append({"clean": "I have two brothers and one sister.",
                "domain": "essay", "cors": [{"cat": "sva", "find": "have", "repl": "has"}]})
    out.append({"clean": "You were very kind to the visitors.",
                "domain": "essay", "cors": [{"cat": "sva", "find": "were", "repl": "was"}]})
    return out

# ---------------------------------------------------------------- past tense
def build_past():
    out = []
    verbs_past = ["went", "saw", "ate", "ran", "came", "gave", "took",
                  "wrote", "drove", "spoke", "drank", "sang", "began",
                  "broke", "won", "met", "sent", "built", "bought", "flew",
                  "grew", "knew", "threw", "drew", "fell", "held", "heard",
                  "wore", "found", "left", "made", "kept", "felt", "slept",
                  "taught", "caught"]
    for t in TIME_PAST:
        for s in ("I", "we", "they", "my friend", "our team", "she", "he"):
            for b in ("go", "see", "eat", "write", "read", "win", "meet",
                      "buy", "send", "take"):
                clean = f"{t.capitalize()}, {s} {_past(b)} to the new exhibition at the museum."
                out.append({"clean": clean, "domain": "essay",
                            "cors": [{"cat": "past", "find": _past(b), "repl": _v(b)[0] if s in ("She", "He") else b}]})
    # irregular past confusion: saw->seen / went->gone after have/has
    for s in ("I", "She", "He", "They", "We"):
        clean = f"{s} have {_v('go')[2].rstrip('ing')+''}" if False else ""
    for s in ("I", "She", "He"):
        clean = f"{s} has gone to the library twice this week."
        out.append({"clean": clean, "domain": "essay",
                    "cors": [{"cat": "verb_form", "find": "gone", "repl": "went"}]})
    for s in ("I", "They", "We"):
        clean = f"{s} have seen that film at least three times."
        out.append({"clean": clean, "domain": "essay",
                    "cors": [{"cat": "verb_form", "find": "seen", "repl": "saw"}]})
    for s in ("I", "They"):
        clean = f"{s} have done all the exercises in chapter four."
        out.append({"clean": clean, "domain": "essay",
                    "cors": [{"cat": "verb_form", "find": "done", "repl": "did"}]})
    return [r for r in out if r["clean"]]

# ---------------------------------------------------------------- articles
def build_articles():
    out = []
    an_words = ["apple", "orange", "egg", "umbrella", "hour", "honest man",
                "old car", "easy question", "interesting book", "important meeting",
                "exam", "opportunity", "award", "idea", "engineer", "artist",
                "address", "island", "envelope", "onion", "elephant"]
    a_words = ["book", "car", "house", "dog", "cat", "pen", "chair",
               "letter", "job", "uniform", "university", "European city",
               "one-way street", "unique chance", " useful tool", "square box"]
    for w in an_words:
        clean = f"She bought an {w} at the market last weekend."
        out.append({"clean": clean, "domain": "essay",
                    "cors": [{"cat": "article", "find": f"an {w}", "repl": f"a {w}"}]})
        clean = f"He wants to be an {w} when he grows up." if w in ("engineer", "artist", "honest man") else None
        if clean:
            out.append({"clean": clean, "domain": "essay",
                        "cors": [{"cat": "article", "find": f"an {w}", "repl": f"a {w}"}]})
    for w in a_words:
        clean = f"He needs a {w.strip()} for the school project."
        out.append({"clean": clean, "domain": "essay",
                    "cors": [{"cat": "article", "find": f"a {w.strip()}", "repl": f"an {w.strip()}"}]})
    return out

# ---------------------------------------------------------------- plurals / quantifiers
def build_plural():
    out = []
    counts = ["two", "three", "four", "five", "six", "several", "many",
              "some new", "ten"]
    for n in counts:
        for sng, pl in [(a, b) for a in NOUNS["singular"][:24]
                        for b in NOUNS["plural"][:24] if b == a + "s"][:0] or []:
            pass
    for n in counts:
        for i, sng in enumerate(NOUNS["singular"][:30]):
            pl = NOUNS["plural"][i] if i < len(NOUNS["plural"]) else sng + "s"
            clean = f"My classmates bought {n} {pl} for the school library."
            out.append({"clean": clean, "domain": "essay",
                        "cors": [{"cat": "plural", "find": pl, "repl": sng}]})
    # irregular plurals
    irr = [("child", "children"), ("man", "men"), ("woman", "women"),
           ("person", "people"), ("foot", "feet"), ("tooth", "teeth")]
    for n in ("three", "four", "five", "six", "several"):
        for s, p in irr:
            clean = f"The teacher praised the {p} in class {n.replace('several','') and ''}".strip() + f" {n} {p}" if False else f"We met {n} {p} at the community centre."
            out.append({"clean": clean, "domain": "essay",
                        "cors": [{"cat": "irr_plural", "find": p, "repl": s + "s"}]})
    # quantifier
    clean = "There are too much people in the room."
    out.append({"clean": "There are too many people in the waiting room.",
                "domain": "essay",
                "cors": [{"cat": "quantifier", "find": "many", "repl": "much"}]})
    out.append({"clean": "She drank much water after the race.",
                "domain": "essay",
                "cors": [{"cat": "quantifier", "find": "much water", "repl": "many water"}]})
    out.append({"clean": "We have less time than we thought.",
                "domain": "professional",
                "cors": [{"cat": "quantifier", "find": "less time", "repl": "fewer time"}]})
    out.append({"clean": "The library has fewer books than before.",
                "domain": "essay",
                "cors": [{"cat": "quantifier", "find": "fewer", "repl": "less"}]})
    return out

# ------------------------------------------------- possessives & confusables
def build_confusables():
    out = []
    # their / there / they're
    for s, o in [("Their house is near the harbour.", None),
                 ("Their teacher praised the whole class.", None),
                 ("Their project received first prize.", None)]:
        out.append({"clean": s, "domain": "essay",
                    "cors": [{"cat": "confusable", "find": "Their", "repl": "There"},
                             {"cat": "confusable", "find": "Their", "repl": "They're"}]})
    for s in ["There is a bakery near the station.",
              "There are several books on the shelf.",
              "There was a long queue outside the shop."]:
        out.append({"clean": s, "domain": "essay",
                    "cors": [{"cat": "confusable", "find": "There", "repl": "Their"},
                             {"cat": "confusable", "find": "There", "repl": "They're"}]})
    for s in ["They're going to the beach tomorrow.",
              "They're learning Spanish this year.",
              "They're planning a trip to Wellington."]:
        out.append({"clean": s, "domain": "essay",
                    "cors": [{"cat": "confusable", "find": "They're", "repl": "Their"},
                             {"cat": "confusable", "find": "They're", "repl": "There"}]})
    # your / you're
    for s in ["Your essay was the best in the class.",
              "Your parents will love this photograph.",
              "I really enjoyed your presentation this morning."]:
        out.append({"clean": s, "domain": "essay",
                    "cors": [{"cat": "confusable", "find": "Your", "repl": "You're"}]})
    for s in ["You're welcome to join our study group.",
              "You're doing a great job this term.",
              "You're invited to the school gala on Friday."]:
        out.append({"clean": s, "domain": "essay",
                    "cors": [{"cat": "confusable", "find": "You're", "repl": "Your"}]})
    # its / it's
    for s in ["The cat licked its paws after dinner.",
              "The company revised its privacy policy.",
              "The tree lost its leaves in autumn."]:
        out.append({"clean": s, "domain": "essay",
                    "cors": [{"cat": "confusable", "find": "its", "repl": "it's"}]})
    for s in ["It's raining heavily in Auckland today.",
              "It's important to check the references.",
              "It's the first time I've travelled by train."]:
        out.append({"clean": s, "domain": "essay",
                    "cors": [{"cat": "confusable", "find": "It's", "repl": "Its"}]})
    # to / too
    for s in ["I want to read the new chapter tonight.",
              "She went to the office before lunch.",
              "We are going to the museum on Monday."]:
        out.append({"clean": s, "domain": "essay",
                    "cors": [{"cat": "confusable", "find": "to", "repl": "too"}]})
    for s in ["The soup is too hot to eat right now.",
              "This bag is too heavy for the flight.",
              "He spoke too quickly during the interview."]:
        out.append({"clean": s, "domain": "essay",
                    "cors": [{"cat": "confusable", "find": "too", "repl": "to"}]})
    # then / than
    for s in ["She is taller than her older brother.",
              "The exam was harder than the practice test.",
              "He arrived earlier than the others."]:
        out.append({"clean": s, "domain": "essay",
                    "cors": [{"cat": "confusable", "find": "than", "repl": "then"}]})
    for s in ["We finished lunch, then we played chess.",
              "First we studied, then we walked home."]:
        out.append({"clean": s, "domain": "essay",
                    "cors": [{"cat": "confusable", "find": "then", "repl": "than"}]})
    # lose/loose, quiet/quite, accept/except, etc.
    for clean, f, r in [
        ("Don't lose your ticket before the concert.", "lose", "loose"),
        ("This shirt is too loose around the neck.", "loose", "lose"),
        ("Please keep quiet during the examination.", "quiet", "quite"),
        ("The library is quite busy on Saturdays.", "quite", "quiet"),
        ("Everyone attended the seminar except Priya.", "except", "accept"),
        ("Please accept our sincere apologies.", "accept", "except"),
        ("The weather affects our travel plans.", "affects", "effects"),
        ("The medicine had an immediate effect.", "effect", "affect"),
        ("We need your advice before Friday.", "advice", "advise"),
        ("I advise you to check the schedule.", "advise", "advice"),
        ("She took a deep breath before speaking.", "breath", "breathe"),
        ("It's hard to breathe in the smoke.", "breathe", "breath"),
        ("The team's success was the principal reason for celebration.", "principal", "principle"),
        ("Honesty is her strongest principle.", "principle", "principal"),
        ("Weather permitting, we will hike tomorrow.", "Weather", "Whether"),
        ("I asked whether the parcel had arrived.", "whether", "weather"),
        ("I don't know whose notebook this is.", "whose", "who's"),
        ("She is the colleague who's leading the project.", "who's", "whose"),
        ("The coach led the team to victory.", "led", "lead"),
        ("Their proposal passed the review stage.", "passed", "past"),
    ]:
        out.append({"clean": clean, "domain": "professional",
                    "cors": [{"cat": "confusable", "find": f, "repl": r}]})
    return out

# ---------------------------------------------------------------- negation
def build_negation():
    out = []
    for wrong in DOUBLE_NEG:
        right = DOUBLE_NEG[wrong]
        sent = right[0].upper() + right[1:] + " last night."
        out.append({"clean": sent, "domain": "essay",
                    "cors": [{"cat": "double_neg", "find": right, "repl": wrong}]})
    # clean negation sentences (never corrupted - protected)
    for s in ["I didn't see anything unusual at the beach.",
              "Nobody in the team knew the answer.",
              "Hardly anyone noticed the small change.",
              "She never says anything unkind.",
              "We couldn't find any parking near the venue.",
              "There wasn't anybody at reception this morning.",
              "I haven't told anybody about the results yet.",
              "They don't need anything else from the shop.",
              "Scarcely a week passes without a new report.",
              "We have never been anywhere so remote."]:
        out.append({"clean": s, "domain": "essay", "cors": []})
    return out

# ---------------------------------------------------------------- adj/adv
def build_adjadv():
    out = []
    pairs = [("quickly", "quick"), ("slowly", "slow"), ("carefully", "careful"),
             ("loudly", "loud"), ("quietly", "quiet"), ("happily", "happy"),
             ("easily", "easy"), ("fluently", "fluent"), ("clearly", "clear"),
             ("gently", "gentle"), ("boldly", "bold"), ("patiently", "patient"),
             ("politely", "polite"), ("safely", "safe"), ("softly", "soft"),
             ("swiftly", "swift"), ("wisely", "wise"), ("bravely", "brave"),
             ("calmly", "calm"), ("eagerly", "eager")]
    for adv, adj in pairs:
        for verb in ("speaks", "works", "reads", "writes", "drives",
                     "listens", "practises", "answers"):
            clean = f"Our teacher {verb} {adv} during the lesson."
            out.append({"clean": clean, "domain": "essay",
                        "cors": [{"cat": "adjadv", "find": adv, "repl": adj}]})
    for adv, adj in pairs[:10]:
        clean = f"The train arrived {adv} at the station."
        out.append({"clean": clean, "domain": "professional",
                    "cors": [{"cat": "adjadv", "find": adv, "repl": adj}]})
    return out

# ---------------------------------------------------------------- comparatives
def build_comparative():
    out = []
    for adj in ("better", "easier", "harder", "faster", "cheaper",
                "stronger", "taller", "cleaner", "simpler", "younger"):
        clean = f"This route is {adj} than the old one."
        out.append({"clean": clean, "domain": "essay",
                    "cors": [{"cat": "comparative", "find": adj, "repl": f"more {adj}"}]})
    for sup in ("easiest", "hardest", "fastest", "cheapest", "strongest",
                "tallest", "cleanest", "simplest", "youngest", "busiest"):
        clean = f"That was the {sup} exam of the term."
        out.append({"clean": clean, "domain": "essay",
                    "cors": [{"cat": "comparative", "find": sup, "repl": f"most {sup}"}]})
    return out

# ---------------------------------------------------------------- contractions
def build_contractions():
    out = []
    frames = [
        ("I don't need any help today.", "dont"),
        ("We can't attend the morning session.", "cant"),
        ("He won't finish before Friday.", "wont"),
        ("She doesn't live here anymore.", "doesnt"),
        ("They didn't receive the invitation.", "didnt"),
        ("It isn't ready for publication yet.", "isnt"),
        ("You aren't on the guest list.", "arent"),
        ("I wasn't at the workshop yesterday.", "wasnt"),
        ("They weren't impressed by the demo.", "werent"),
        ("She hasn't replied to my email.", "hasnt"),
        ("We haven't booked the venue.", "havent"),
        ("I hadn't read the appendix.", "hadnt"),
        ("They couldn't find the document.", "couldnt"),
        ("You shouldn't ignore the warning.", "shouldnt"),
        ("I wouldn't change the design.", "wouldnt"),
        ("I'm writing to confirm the details.", "im"),
        ("I've attached the latest draft.", "ive"),
        ("They're moving to Dunedin in March.", "theyre"),
        ("You're eligible for the discount.", "youre"),
        ("We've extended the deadline.", "weve"),
        ("There's a new café near the office.", "theres"),
        ("She's leading the design review.", "shes"),
        ("He's responsible for the budget.", "hes"),
        ("Let's review the figures again.", "lets"),
    ]
    for clean, wrong in frames:
        c = wrong.replace("'", "")
        good = clean.replace(wrong if "'" not in wrong else wrong, clean and "")
        # find contraction in clean, replace with stripped version
        import re as _re
        m = _re.search(r"\w+'\w+", clean)
        if m:
            out.append({"clean": clean, "domain": "professional",
                        "cors": [{"cat": "contraction", "find": m.group(0),
                                  "repl": m.group(0).replace("'", "")}]})
    return out

# ---------------------------------------------------------------- capitalization
def build_capitalization():
    out = []
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
            "Saturday", "Sunday"]
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November",
              "December"]
    cities = ["Auckland", "Wellington", "Christchurch", "Dunedin",
              "Hamilton", "Queenstown", "Rotorua", "London", "Sydney",
              "Melbourne", "Tokyo", "Paris"]
    for d in days:
        clean = f"The meeting is scheduled for {d} next week."
        out.append({"clean": clean, "domain": "professional",
                    "cors": [{"cat": "capitalization", "find": d, "repl": d.lower()}]})
    for m in months:
        clean = f"The report is due at the end of {m}."
        out.append({"clean": clean, "domain": "professional",
                    "cors": [{"cat": "capitalization", "find": m, "repl": m.lower()}]})
    for c in cities:
        clean = f"Our branch office in {c} is closing early."
        out.append({"clean": clean, "domain": "professional",
                    "cors": [{"cat": "capitalization", "find": c, "repl": c.lower()}]})
    for lang in ("English", "French", "Māori", "Japanese", "Chinese"):
        clean = f"She is fluent in {lang} and {('German' if lang != 'German' else 'English')}."
        out.append({"clean": clean, "domain": "essay",
                    "cors": [{"cat": "capitalization", "find": lang, "repl": lang.lower()}]})
    # sentence-start lowercase
    starters = ["After the meeting, we reviewed the notes.",
                 "Before lunch, she checked her inbox.",
                 "During the holidays, we visitedRotorua.".replace("visitedRotorua", "visited Rotorua"),
                 "Yesterday, the team completed the audit.",
                 "This morning, I answered all my emails.",
                 "In the afternoon, we toured the campus.",
                 "On Friday, the library closes early.",
                 "Next week, our class starts the new module."]
    for s in starters:
        out.append({"clean": s, "domain": "professional",
                    "cors": [{"cat": "capitalization", "find": s[:1], "repl": s[:1].lower()}]})
    # lowercase i
    for s in ["When I arrived, the room was full.",
              "My teacher said I had improved.",
              "Before I left, I checked the timetable.",
              "Last week I joined the debating club.",
              "Believe me, I tried my best."]:
        out.append({"clean": s, "domain": "essay",
                    "cors": [{"cat": "capitalization", "find": " I ", "repl": " i "}]})
    return out

# ---------------------------------------------------------------- punctuation: period
def build_period():
    out = []
    for s in ["We finished the survey and submitted the form",
              "The committee approved the new policy",
              "Our team completed the migration on schedule",
              "She attended all four workshops",
              "The students organised the fundraiser",
              "I have attached the revised draft"]:
        out.append({"clean": s + ".", "domain": "professional",
                    "cors": [{"cat": "punct_period", "find": ".", "repl": ""}]})
    for s in ["Did you finish the assignment",
              "Can you send the invoice today",
              "Will the office be open tomorrow",
              "Have they signed the contract",
              "Is the workshop still on Friday"]:
        out.append({"clean": s + "?", "domain": "professional",
                    "cors": [{"cat": "punct_question", "find": "?", "repl": "."}]})
    return out

# ---------------------------------------------------------------- word repetition
def build_repetition():
    out = []
    for art in ("the", "a", "my", "our", "their", "his", "her"):
        for noun in ("report", "letter", "meeting", "project", "invoice",
                     "ticket", "essay", "chapter", "summary", "receipt",
                     "package", "book", "photo", "file"):
            clean = f"I filed {art} {noun} in the cabinet yesterday."
            out.append({"clean": clean, "domain": "professional",
                        "cors": [{"cat": "repetition",
                                  "find": f"{art} {noun}",
                                  "repl": f"{art} {art} {noun}"}]})
    return out

# ---------------------------------------------------------------- prepositions
def build_prepositions():
    out = []
    pairs = [
        ("different from", "different than"),
        ("depends on", "depends of"),
        ("consists of", "consists in"),
        ("married to", "married with"),
        ("good at", "good in"),
        ("interested in", "interested to"),
        ("afraid of", "afraid from"),
        ("similar to", "similar with"),
        ("capable of", "capable to"),
        ("responsible for", "responsible of"),
        ("famous for", "famous in"),
        ("keen on", "keen of"),
    ]
    frames = ["This design is {} the previous version.",
              "The outcome {} the weather conditions.",
              "The kit {} three main components.",
              "My cousin is {} a nurse from Rotorua.",
              "She is {} solving difficult problems.",
              "They are {} joining the chess club.",
              "He is {} large dogs.",
              "This approach is {} the old method.",
              "The team is {} delivering on time.",
              "The city is {} its farmers market.",
              "We are {} trying new recipes."]
    for good, bad in pairs:
        for f in frames[:4]:
            clean = f.format(good) if "{}" in f else None
            if clean and good not in ("married to",):
                out.append({"clean": clean, "domain": "professional",
                            "cors": [{"cat": "preposition", "find": good,
                                      "repl": bad}]})
    # fixed frames for specific pairs
    out.append({"clean": "Priya is married to a nurse from Rotorua.",
                "domain": "professional",
                "cors": [{"cat": "preposition", "find": "married to", "repl": "married with"}]})
    out.append({"clean": "He is afraid of large dogs.",
                "domain": "essay",
                "cors": [{"cat": "preposition", "find": "afraid of", "repl": "afraid from"}]})
    out.append({"clean": "She is interested in joining the chess club.",
                "domain": "essay",
                "cors": [{"cat": "preposition", "find": "interested in", "repl": "interested to"}]})
    out.append({"clean": "This approach is similar to the old method.",
                "domain": "professional",
                "cors": [{"cat": "preposition", "find": "similar to", "repl": "similar with"}]})
    out.append({"clean": "The team is capable of delivering on time.",
                "domain": "professional",
                "cors": [{"cat": "preposition", "find": "capable of", "repl": "capable to"}]})
    out.append({"clean": "Wellington is famous for its wind and coffee.",
                "domain": "essay",
                "cors": [{"cat": "preposition", "find": "famous for", "repl": "famous in"}]})
    out.append({"clean": "We are keen on trying new recipes.",
                "domain": "essay",
                "cors": [{"cat": "preposition", "find": "keen on", "repl": "keen of"}]})
    return out

# ---------------------------------------------------------------- redundancy
def build_redundancy():
    out = []
    for good, bad in [("return the call", "return back the call"),
                      ("reply to the message", "reply back the message"),
                      ("reverted to the draft", "reverted back to the draft"),
                      ("discussed the plan", "discussed about the plan"),
                      ("entered the building", "entered into the building"),
                      ("comprises three chapters", "comprises of three chapters"),
                      ("jumped off the wall", "jumped off of the wall"),
                      ("equally good", "equally as good")]:
        frames = ["Please {} before noon.", "The client {} yesterday.",
                  "Our manager {} this morning.", "The report {} in detail."]
        for f in frames:
            try:
                clean = f.format(good)
            except Exception:
                continue
            # build corrupted by inserting bad
            if "return back" in bad:
                pass
            out.append({"clean": clean, "domain": "professional", "cors": []})
    # explicit redundant pairs
    ex = [("Please return the form before Friday.", "return", "return back"),
          ("I will reply to your email shortly.", "reply to", "reply back to"),
          ("She reverted to the earlier draft.", "reverted to", "reverted back to"),
          ("We discussed the budget in depth.", "discussed", "discussed about"),
          ("They entered the building at nine.", "entered", "entered into"),
          ("The guide comprises three sections.", "comprises", "comprises of"),
          ("The cat jumped off the fence.", "off the", "off of the"),
          ("The results were equally good.", "equally", "equally as")]
    for clean, find, repl in ex:
        out.append({"clean": clean, "domain": "professional",
                    "cors": [{"cat": "redundancy", "find": find, "repl": repl}]})
    return out

# ---------------------------------------------------------------- enjoy/avoid +ing
def build_verbform():
    out = []
    ACT2BASE = {"reading": "read", "swimming": "swim", "walking": "walk",
                "cooking": "to cook".split(" ")[1], "writing": "write",
                "singing": "sing", "drawing": "draw", "camping": "camp",
                "fishing": "fish", "dancing": "dance", "tramping": "tramp",
                "gardening": "garden"}
    for verb in ("enjoy", "avoid", "finish", "keep", "practise", "consider"):
        for act in ("reading", "swimming", "walking", "cooking", "writing",
                    "singing", "drawing", "camping", "fishing", "dancing",
                    "tramping", "gardening"):
            for subj, vform in [("I", verb), ("We", verb), ("They", verb),
                                ("She", verb + "s"), ("He", verb + "s")]:
                clean = f"{subj} {vform} {act} every weekend."
                out.append({"clean": clean, "domain": "essay",
                            "cors": [{"cat": "verb_ing", "find": act,
                                      "repl": "to " + ACT2BASE[act]}]})
    return out

# ---------------------------------------------------------------- spelling
def build_misspell():
    out = []
    contexts = ["We {} the parcel on Monday.", "She {} the invitation.",
                 "They {} their tickets online.", "Our team {} the deadline.",
                 "I {} the news last night.", "He {} to the meeting.",
                 "The report {} the new policy.", "Please {} the document.",
                 "We {} the results tomorrow.", "She {} the forms in April."]
    wordmap = [("received", "recieve"), ("separate", "seperate"),
               ("until", "untill"), ("which", "wich"),
               ("because", "becuase"), ("believe", "beleive"),
               ("achieve", "acheive"), ("address", "adress"),
               ("calendar", "calender"), ("grammar", "grammer"),
               ("happened", "occured wrong".split()[0])]
    for good, bad in wordmap[:6]:
        for f in contexts[:3]:
            clean = f.format(good) if "{}" in f else None
            if clean:
                out.append({"clean": clean, "domain": "professional",
                            "cors": [{"cat": "spelling", "find": good,
                                      "repl": bad}]})
    # generic misspell injection into clean sentences
    extras = [
        ("The environment committee met in November.", "environment", "enviroment"),
        ("The government published new guidelines.", "government", "goverment"),
        ("Please confirm the necessary arrangements.", "necessary", "neccessary"),
        ("The occasion called for a formal reply.", "occasion", "occassion"),
        ("Her essay received a high award.", "received", "recieved"),
        ("We must separate the documents by year.", "separate", "seperate"),
        ("I will definitely attend the ceremony.", "definitely", "definately"),
        ("The rehearsal continued until dark.", "until", "untill"),
        ("I'm not sure which option is better.", "which", "wich"),
        ("She couldn't decide because of the noise.", "because", "becuase"),
        ("I believe the figures are correct.", "believe", "beleive"),
        ("They want to achieve a better result.", "achieve", "acheive"),
        ("Please write to our address in Wellington.", "address", "adress"),
        ("The calendar is full this month.", "calendar", "calender"),
        ("Check the grammar before you submit.", "grammar", "grammer"),
        ("The weather changed suddenly.", "weather", "wether"),
        ("Our friends visited in February.", "February", "Febuary"),
        ("He borrowed a book from the library.", "library", "libary"),
        ("The restaurant was excellent.", "restaurant", "restaraunt"),
        ("We are grateful for your support.", "grateful", "greatful"),
        ("She is an independent researcher.", "independent", "independant"),
        ("The committee discussed the proposal.", "committee", "commitee"),
        ("This is a great opportunity.", "opportunity", "opertunity"),
        ("The professor gave a clear explanation.", "explanation", "explantion"),
    ]
    for clean, good, bad in extras:
        out.append({"clean": clean, "domain": "professional",
                    "cors": [{"cat": "spelling", "find": good, "repl": bad}]})
    return out

# ------------------------------------------------------- clean protected pools
def build_clean_protected():
    out = []
    # names
    for name, rest in [("Wiremu", "presented his findings at the hui."),
                       ("Aroha", "organised the fundraiser for the marae."),
                       ("Hōne", "plays rugby for the local club."),
                       ("Priya", "submitted the report before the deadline."),
                       ("Xiaoming", "moved to Auckland last February."),
                       ("Aoife", "recorded the minutes of the meeting."),
                       ("O'Connell", "signed the contract on 14 May 2025."),
                       ("Mr McGregor", "replied to our invoice promptly."),
                       ("Nguyễn", "joined the design team in March."),
                       ("Mereana", "teaches at the kura in Gisborne."),
                       ("Rawiri", "fixed the fence with his father."),
                       ("Kavita", "chaired the review panel on Friday.")]:
        out.append({"clean": f"{name} {rest}", "domain": "professional", "cors": []})
    # numbers / dates / units
    for s in ["The invoice totalled $1,234.50 including GST.",
              "Our office is open from 9:00 a.m. to 5:30 p.m.",
              "The flight departs at 06:45 and lands at 18:10.",
              "She paid $42 for the ticket and $3.90 for coffee.",
              "The population reached 5.12 million in 2019.",
              "We ordered 15 boxes, 240 pens, and 12 staplers.",
              "The survey covered 1,500 respondents aged 18 to 65.",
              "Pi is approximately 3.14159 in this calculation.",
              "The recipe uses 250 g of flour and 300 ml of milk.",
              "The meeting runs from 21 March 2025 to 25 March 2025.",
              "They arrived on 3/04/2025 and left on 12/04/2025.",
              "Chapter 7 covers 34 pages, and Chapter 8 covers 28.",
              "The discount is 20%, so you save $19.80.",
              "Room 12B is on the fourth floor of Building C.",
              "He ran 42.2 km in 3 hours and 51 minutes."]:
        out.append({"clean": s, "domain": "professional", "cors": []})
    # quotes
    for s in ['The reviewer wrote, "a quietly brilliant debut."',
              'Our principal said, "attendance has improved this term."',
              '"Kia ora," she said as she welcomed the visitors.',
              'The notice read: "closed until further notice."',
              'He asked, "did anyone see the missing file?"',
              'The email began, "thank you for your prompt reply."',
              '"We won the debate," the captain announced proudly.',
              'The headline read, "Council approves the new cycleway."']:
        out.append({"clean": s, "domain": "professional", "cors": []})
    # technical
    for s in ["We deployed the service on Kubernetes version 1.29.",
              "The PostgreSQL database runs on port 5432 by default.",
              "Run npm install before you start the dev server.",
              "The API returns JSON over HTTPS with OAuth 2.0.",
              "Configure the nginx reverse proxy in /etc/nginx/nginx.conf.",
              "The function setTimeout schedules tasks in Node.js.",
              "Our CI/CD pipeline uses GitHub Actions and Docker.",
              "The regex ^[a-z]+_[0-9]+$ matches snake_case names.",
              "Redis caching reduced the p99 latency to 87 ms.",
              "The Vue component emits events via props and callbacks.",
              "Enable TLS 1.3 and disable SSLv3 on the gateway.",
              "The GraphQL schema lives in src/graphql/schema.graphql.",
              "Commit the changes with git commit -m 'fix: typo'.",
              "The gRPC service is defined in Protobuf v3 syntax.",
              "Add the ESLint rule to the eslint.config.js file.",
              "The user table has an AUTO_INCREMENT primary key."]:
        out.append({"clean": s, "domain": "technical", "cors": []})
    # UK / NZ / US spelling (correct as-is, never flagged)
    for s in ["We organised the colours for the exhibition. (UK)",
              "She travelled to the centre of London last autumn. (UK)",
              "They practised their programme at the theatre. (UK)",
              "The harbour was full of yachts on Saturday. (UK/NZ)",
              "I realised the aluminium frame had a grey coating. (UK)",
              "My favourite flavour is definitely liquorice. (UK)",
              "We went tramping near Lake Waikaremoana last fortnight. (NZ)",
              "He drove the ute to the bach for the long weekend. (NZ)",
              "Grab some pies from the dairy on the way home. (NZ)",
              "The kids wore togs and jandals at the beach. (NZ)",
              "She sorted the rubbish bin and recycling correctly. (NZ)",
              "Kia ora, welcome to our little slice of paradise. (NZ)",
              "There's heaps of kai at the shared table. (NZ)",
              "The footpath behind the dairy leads to the school. (NZ)",
              "Sweet as, the crew finished the job early. (NZ)",
              "I colorized the catalog with gray-scale images. (US)",
              "The theater organized a labor day special. (US)",
              "analyze the behavior of the optimized model. (US)".capitalize()]:
        out.append({"clean": s, "domain": "essay", "cors": []})
    # clean grammar traps that must NOT be flagged
    for s in ["The team have submitted their report. (UK collective)",
              "Neither of the answers is correct.",
              "Each of the students has a locker.",
              "One of the files was missing.",
              "The data suggest that the trend is real.",
              "There are a pen and two pencils on the desk.",
              "A number of students were absent today.",
              "All of the cake has been eaten.",
              "Some of the water has evaporated overnight.",
              "None of the printers are working.",
              "The sheep grazed quietly in the top paddock.",
              "The police are investigating the burglary.",
              "My hair is getting longer every month.",
              "The news from headquarters was encouraging.",
              "Mathematics is my favourite subject.",
              "Ten kilometres is a long way to walk.",
              "Five dollars seems too much for a coffee.",
              "I could have finished earlier if I'd started sooner.",
              "She may well be right about the schedule.",
              "We had better leave before the rain starts.",
              "Hardly anyone understood the joke.",
              "You had me at hello.",
              "It was I who called the meeting.",
              "That is she at reception.",
              "Between you and me, the cake was burnt.",
              "Whom shall I say is calling?",
              "The well-trained team performed admirably.",
              "A well-written essay deserves a high mark.",
              "She is one of those teachers who always help."]:
        out.append({"clean": s, "domain": "essay", "cors": []})
    return out

# ------------------------------------------------------- multi-domain essays
def build_essay():
    out = []
    essays = [
        "Learning a second language requires patience and daily practice.",
        "Reading widely improves both vocabulary and critical thinking.",
        "Exercise helps students concentrate better during long lessons.",
        "Our school fundraiser was a great success this year.",
        "Volunteering at the food bank taught me a lot about teamwork.",
        "The science fair projects impressed all the judges.",
        "Climate change affects farming communities across the country.",
        "Public libraries offer free access to books and quiet spaces.",
        "Teamwork makes difficult projects much easier to complete.",
        "The debating team won the regional finals in Hamilton.",
        "Every student deserves a safe and supportive classroom.",
        "Music education develops discipline as well as creativity.",
        "The composting scheme reduced our school's waste by half.",
        "Interviewing our grandparents taught us about local history.",
        "A balanced diet and enough sleep improve exam performance.",
        "The new cycleway makes the trip to school safer.",
        "Writing by hand helps some learners remember more effectively.",
        "Our kapa haka group performed at the regional festival.",
        "The robotics club built a small rover from spare parts.",
        "Documentaries bring history to life for young learners.",
    ]
    for e in essays:
        out.append({"clean": e, "domain": "essay", "cors": []})
    return out

BUILDERS = [build_sva, build_past, build_articles, build_plural,
            build_confusables, build_negation, build_adjadv,
            build_comparative, build_contractions, build_capitalization,
            build_period, build_repetition, build_prepositions,
            build_redundancy, build_verbform, build_misspell,
            build_clean_protected, build_essay]

def build_all():
    allrec = []
    for b in BUILDERS:
        allrec.extend(b())
    return allrec

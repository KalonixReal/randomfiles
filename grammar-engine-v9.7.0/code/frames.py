"""Frame-DSL combinatorial corpus engine.
Each family: category + frames with slots and a corruption rule on one slot.
All combos enumerated (capped per slot), hash-partitioned into splits so each
unique (frame, fill-values) combo appears in exactly ONE split.

A frame produces:
  clean sentence (correct English by construction)
  optional corruption: {find, repl} on the filled target slot
Clean-only families (protected classes) have corr=None.
"""

import random, itertools, hashlib

R = random.Random(987654)

from lexicon import (VERBS, NOUNS, ADJ, ADV, SUBJ_SING, SUBJ_PL,
                     MISSPELL, CONFUSABLES, PROPER_LOWER)

V3 = {b: f[0] for b, f in VERBS.items()}
VP = {b: f[1] for b, f in VERBS.items()}
VG = {b: f[2] for b, f in VERBS.items()}
VBASE = list(VERBS.keys())
SING = [n for n in NOUNS["singular"]]
PLUR = [n for n in NOUNS["plural"]]
UNC = NOUNS["uncount"]

SUBJ = ["He", "She", "It", "My brother", "My sister", "Our teacher",
        "The student", "The engineer", "The manager", "The nurse",
        "My friend", "Our neighbour"]
SUBJPL = ["They", "We", "You", "My friends", "The students",
          "Our teachers", "The children", "The players", "My parents",
          "Our neighbours"]
TIMEP = ["yesterday", "last week", "last month", "two days ago",
          "three weeks ago", "last night", "last summer"]
TIMEPL = ["every morning", "every evening", "each week", "twice a week",
          "on Saturdays", "every weekend"]
QUANT = ["two", "three", "four", "five", "six", "seven", "several",
         "many", "ten"]

AN_WORDS = ["apple", "orange", "egg", "umbrella", "hour", "exam",
            "opportunity", "award", "idea", "engineer", "artist", "address",
            "island", "envelope", "onion", "elephant", "instrument",
            "honest answer", "important meeting", "easy question"]
A_WORDS = ["book", "car", "house", "dog", "pen", "chair", "letter", "job",
            "uniform", "European city", "unique chance", "useful tool",
            "square box", "one-way street", "birthday card"]

ADV2 = ADV[:14]
ADJ2 = ADJ[:14]

CONTRAS = [("don't", "dont"), ("can't", "cant"), ("won't", "wont"),
          ("doesn't", "doesnt"), ("didn't", "didnt"), ("isn't", "isnt"),
          ("aren't", "arent"), ("wasn't", "wasnt"), ("weren't", "werent"),
          ("hasn't", "hasnt"), ("haven't", "havent"), ("hadn't", "hadnt"),
          ("couldn't", "couldnt"), ("shouldn't", "shouldnt"),
          ("wouldn't", "wouldnt"), ("I'm", "im"), ("I've", "ive"),
          ("they're", "theyre"), ("you're", "youre"), ("we've", "weve"),
          ("there's", "theres"), ("she's", "shes"), ("he's", "hes"),
          ("let's", "lets")]

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
        "Saturday", "Sunday"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
CITIES = ["Auckland", "Wellington", "Christchurch", "Dunedin", "Hamilton",
          "Queenstown", "Rotorua", "London", "Sydney", "Melbourne", "Tokyo",
          "Paris"]
LANGS = ["English", "French", "German", "Spanish", "Japanese", "Chinese",
         "Māori", "Korean", "Italian"]

NAMES = ["Wiremu", "Aroha", "Hōne", "Priya", "Xiaoming", "Aoife",
         "Mereana", "Rawiri", "Kavita", "Rohan", "Deepa", "Mei", "Yuki",
         "Takashi", "Mateo", "Inés", "Sofia", "Leon", "Amelia", "Oliver",
         "Charlotte", "Henry", "Lucas", "Nguyễn", "McGregor", "O'Connell",
         "Tane", "Manaia", "Jesse", "Rita"]
NAME_ACT = ["presented the findings at the hui",
            "organised the fundraiser for the marae",
            "submitted the report before the deadline",
            "moved to Auckland last February",
            "recorded the minutes of the meeting",
            "signed the contract on 14 May",
            "replied to our invoice promptly",
            "joined the design team in March",
            "teaches at the kura in Gisborne",
            "fixed the fence with his father",
            "chaired the review panel on Friday",
            "answered all the questions clearly",
            "watered the garden this morning",
            "photographed the harbour at sunset",
            "translated the poem into Māori"]

TECH = ["JavaScript", "TypeScript", "Kubernetes", "PostgreSQL", "Redis",
        "Docker", "nginx", "GraphQL", "OAuth 2.0", "Node.js", "Python",
        "the API", "the CI/CD pipeline", "the React app", "the Vue app",
        "the gRPC service", "the SQLite database", "the Git repository",
        "the ESLint config", "the Terraform module", "Prometheus",
        "Grafana", "the WebSocket server", "the REST endpoint"]
TECHACT = ["runs on port 5432 in production",
           "handles retries automatically",
           "needs a manual review before release",
           "supports custom middleware plugins",
           "returns JSON over HTTPS",
           "streams logs to the monitoring stack",
           "caches responses for five minutes",
           "validates every incoming request",
           "rotates its credentials each quarter",
           "backs up the data every night",
           "scales horizontally under load",
           "rejects malformed payloads silently",
           "indexes the queries in the background",
           "forwards traffic to the upstream service",
           "records metrics for the dashboard"]

UKSPELL = [("colour", "color"), ("organised", "organized"),
           ("centre", "center"), ("travelled", "traveled"),
           ("practised", "practiced"), ("programme", "program"),
           ("theatre", "theater"), ("favourite", "favorite"),
           ("realised", "realized"), ("harbour", "harbor"),
           ("licence", "license"), ("defence", "defense"),
           ("aluminium", "aluminum"), ("metre", "meter")]
UKFRAME = ["We {V3} the {U} yesterday.", "She {V3} the {U} last night.",
           "They {V3} a new {U} for the exhibition.",
           "Our team {V3} the {U} before the deadline.",
           "The label on the {U} lists every ingredient."]
USSPELL = [(b, a) for a, b in UKSPELL]  # reversed direction

PREPG = [("different from", "different than"), ("depends on", "depends of"),
         ("consists of", "consists in"), ("good at", "good in"),
         ("interested in", "interested to"), ("afraid of", "afraid from"),
         ("similar to", "similar with"), ("capable of", "capable to"),
         ("responsible for", "responsible of"), ("famous for", "famous in"),
         ("keen on", "keen of")]

IRRPL = [("children", "childs"), ("men", "mans"), ("women", "womans"),
         ("people", "persons"), ("feet", "feets"), ("teeth", "tooths"),
         ("mice", "mouses"), ("geese", "gooses")]

DOUBLE_NEG_FIX = {"anything": "nothing", "anybody": "nobody",
                  "anywhere": "nowhere"}

MISPAIR = [(g, w) for g, w in [("received", "recieved"),
          ("separate", "seperate"), ("until", "untill"),
          ("which", "wich"), ("because", "becuase"),
          ("believe", "beleive"), ("achieve", "acheive"),
          ("address", "adress"), ("calendar", "calender"),
          ("grammar", "grammer"), ("February", "Febuary"),
          ("library", "libary"), ("restaurant", "restaraunt"),
          ("grateful", "greatful"), ("independent", "independant"),
          ("committee", "commitee"), ("opportunity", "opertunity"),
          ("definitely", "definately"), ("environment", "enviroment"),
          ("government", "goverment"), ("necessary", "neccessary"),
          ("occasion", "occassion"), ("weather", "wether")]]

# ------------------------------------------------------------- families
# each frame: (text, slots dict, corr spec or None)
# corr spec: (find_slot, repl_fn) — repl computed from the FILLED find value
def fam(cat, frames): return {"cat": cat, "frames": frames}

FAMILIES = []

# ---- SVA / 3SG / past / verb forms
FAMILIES.append(fam("sva", [
    ("{S} has finished the {N} already.", {"S": SUBJ, "N": SING[:40]}, ("has", lambda v: "have")),
    ("{S} has to submit the {N} before noon.", {"S": SUBJ, "N": SING[:40]}, ("has", lambda v: "have")),
    ("{S} was at the {N} for two hours.", {"S": SUBJ, "N": SING[:40]}, ("was", lambda v: "were")),
    ("{S} does not enjoy the {N}.", {"S": SUBJ, "N": SING[:40]}, ("does not", lambda v: "do not")),
    ("{S} is working on the {N} today.", {"S": SUBJ, "N": SING[:40]}, ("is", lambda v: "are")),
    ("{SP} were happy with the {N}.", {"SP": SUBJPL, "N": SING[:40]}, ("were", lambda v: "was")),
    ("{SP} are meeting the client about the {N} tomorrow.", {"SP": SUBJPL, "N": SING[:40]}, ("are", lambda v: "is")),
    ("{SP} have submitted the {N}.", {"SP": SUBJPL, "N": SING[:40]}, ("have", lambda v: "has")),
    ("I has completed the {N}.", {"N": SING[:40]}, ("has", lambda v: "have")),
    ("You was very helpful during the {N}.", {"N": SING[:40]}, ("was", lambda v: "were")),
]))

TRANS3 = ["watches", "reads", "writes", "opens", "closes", "cleans", "fixes",
          "carries", "washes", "checks", "copies", "finishes", "teaches",
          "touches", "pushes", "wants", "needs", "orders", "reviews",
          "collects", "labels", "paints", "draws", "shares", "packs",
          "wraps", "counts", "measures", "describes", "photographs"]
MOTION3 = ["goes", "walks", "travels", "drives", "runs", "flies", "returns",
           "comes", "moves", "cycles", "hurries", "swims"]
TRANSP = ["watched", "read", "wrote", "opened", "closed", "cleaned", "fixed",
          "carried", "washed", "checked", "copied", "finished", "taught",
          "reviewed", "collected", "photographed", "ordered", "shared",
          "packed", "measured", "described", "painted"]
MOTIONP = ["went", "walked", "travelled", "drove", "ran", "flew", "returned",
           "came", "moved", "cycled", "hurried", "swam"]
VERB2BASE = {"watches":"watch","reads":"read","writes":"write","opens":"open",
             "closes":"close","cleans":"clean","fixes":"fix","carries":"carry",
             "washes":"wash","checks":"check","copies":"copy","finishes":"finish",
             "teaches":"teach","touches":"touch","pushes":"push","wants":"want",
             "needs":"need","orders":"order","reviews":"review","collects":"collect",
             "labels":"label","paints":"paint","draws":"draw","shares":"share",
             "packs":"pack","wraps":"wrap","counts":"count","measures":"measure",
             "describes":"describe","photographs":"photograph",
             "goes":"go","walks":"walk","travels":"travel","drives":"drive",
             "runs":"run","flies":"fly","returns":"return","comes":"come",
             "moves":"move","cycles":"cycle","hurries":"hurry","swims":"swim"}
FAMILIES.append(fam("sva_3sg", [
    ("{S} {V3} the {N} {T}.", {"S": SUBJ, "V3": TRANS3, "N": SING, "T": TIMEPL}, ("{V3}", lambda v: VERB2BASE[v])),
    ("{S} {V3} to the {N} every week.", {"S": SUBJ, "V3": MOTION3, "N": SING}, ("{V3}", lambda v: VERB2BASE[v])),
    ("My sister {V3} the {N} in the {N2}.", {"V3": TRANS3, "N": SING, "N2": SING}, ("{V3}", lambda v: VERB2BASE[v])),
    ("Our teacher {V3} the lesson every {D}.", {"V3": TRANS3, "D": DAYS}, ("{V3}", lambda v: VERB2BASE[v])),
]))

PAST2BASE = {"watched":"watch","read":"read","wrote":"write","opened":"open",
             "closed":"close","cleaned":"clean","fixed":"fix","carried":"carry",
             "washed":"wash","checked":"check","copied":"copy","finished":"finish",
             "taught":"teach","reviewed":"review","collected":"collect",
             "photographed":"photograph","ordered":"order","shared":"share",
             "packed":"pack","measured":"measure","described":"describe",
             "painted":"paint",
             "went":"go","walked":"walk","travelled":"travel","drove":"drive",
             "ran":"run","flew":"fly","returned":"return","came":"come",
             "moved":"move","cycled":"cycle","hurried":"hurry","swam":"swim"}
FAMILIES.append(fam("past", [
    ("{T}, {S} {VP} the {N}.", {"T": TIMEP, "S": ["I", "we", "they", "my friend", "our team"], "VP": TRANSP, "N": SING}, ("{VP}", lambda v: PAST2BASE[v])),
    ("{S} {VP} to the {N} {T}.", {"S": ["I", "We", "They", "She", "He"], "VP": MOTIONP, "N": SING, "T": TIMEP}, ("{VP}", lambda v: PAST2BASE[v])),
    ("Last night we {VP} the {N} together.", {"VP": TRANSP, "N": SING}, ("{VP}", lambda v: PAST2BASE[v])),
]))

FAMILIES.append(fam("verb_form", [
    ("{S} has gone to the {N} twice this week.", {"S": ["I", "She", "He", "Priya", "Wiremu"], "N": SING}, ("gone", lambda v: "went")),
    ("{S} have seen that {N} at least three times.", {"S": ["I", "We", "They"], "N": SING}, ("seen", lambda v: "saw")),
    ("{S} have done all the {PL} in the {N}.", {"S": ["I", "We", "They"], "PL": PLUR, "N": ["chapter", "workbook", "module"]}, ("done", lambda v: "did")),
    ("{S} has written the {N} already.", {"S": ["She", "He", "Aroha"], "N": SING}, ("written", lambda v: "wrote")),
    ("{S} has eaten the {N}.", {"S": ["She", "He", "It"], "N": SING}, ("eaten", lambda v: "ate")),
    ("I seen the {N} yesterday.", {"N": SING[:40]}, ("seen", lambda v: "saw")),
    ("They seen the {N} last week.", {"N": SING[:40]}, ("seen", lambda v: "saw")),
    ("We seen the {N} at the show.", {"N": SING[:40]}, ("seen", lambda v: "saw")),
    ("He done the {N} this morning.", {"N": SING[:40]}, ("done", lambda v: "did")),
    ("She done the {N} before lunch.", {"N": SING[:40]}, ("done", lambda v: "did")),
    ("They done all the {PL} yesterday.", {"PL": PLUR[:40]}, ("done", lambda v: "did")),
    ("I wrote the {N} yesterday.", {"N": SING[:40]}, (None, None)),
    ("She gone to the {N} this morning.", {"N": SING[:40]}, ("gone", lambda v: "went")),
    ("He broke the {N} last night.", {"N": SING[:40]}, (None, None)),
    ("I ate the {N} already.", {"N": SING[:40]}, (None, None)),
]))

# ---- articles
TAD = ["last week", "this morning", "on Friday", "after school",
        "before lunch", "in April", "yesterday"]
TAD = ["last week", "this morning", "on Friday", "after school",
        "before lunch", "in April", "yesterday"]
FAMILIES.append(fam("article", [
    ("She bought an {AN} at the market {T}.", {"AN": AN_WORDS, "T": TAD}, ("an {AN}", lambda v: "a " + v)),
    ("He needs an {AN} for the project {T}.", {"AN": AN_WORDS, "T": TAD}, ("an {AN}", lambda v: "a " + v)),
    ("I saw an {AN} on the table {T}.", {"AN": AN_WORDS, "T": TAD}, ("an {AN}", lambda v: "a " + v)),
    ("We ordered a {A} from the shop {T}.", {"A": A_WORDS, "T": TAD}, ("a {A}", lambda v: "an " + v)),
    ("He wrote a {A} last week about the team.", {"A": A_WORDS}, ("a {A}", lambda v: "an " + v)),
    ("They photographed a {A} at the event.", {"A": A_WORDS}, ("a {A}", lambda v: "an " + v)),
    ("She described an {AN} in her essay about the {N}.", {"AN": AN_WORDS, "N": SING[:30]}, ("an {AN}", lambda v: "a " + v)),
    ("He borrowed a {A} from the library for the {N}.", {"A": A_WORDS, "N": SING[:30]}, ("a {A}", lambda v: "an " + v)),
    ("I photographed an {AN} near the {N}.", {"AN": AN_WORDS, "N": SING[:30]}, ("an {AN}", lambda v: "a " + v)),
    ("We need a {A} for the {N}.", {"A": A_WORDS, "N": SING[:30]}, ("a {A}", lambda v: "an " + v)),
]))

FAMILIES.append(fam("plural", [
    ("My classmates bought {Q} {PL} for the library.", {"Q": QUANT, "PL": PLUR}, ("{PL}", lambda v: [s for s, p in zip(SING, PLUR) if p == v][0])),
    ("She has {Q} {PL} at home.", {"Q": QUANT, "PL": PLUR}, ("{PL}", lambda v: [s for s, p in zip(SING, PLUR) if p == v][0])),
    ("He bought {Q} {PL} at the market.", {"Q": QUANT, "PL": PLUR}, ("{PL}", lambda v: [s for s, p in zip(SING, PLUR) if p == v][0])),
    ("We photographed {Q} {PL} in the garden.", {"Q": QUANT, "PL": PLUR}, ("{PL}", lambda v: [s for s, p in zip(SING, PLUR) if p == v][0])),
    ("I counted {Q} {PL} on the shelf.", {"Q": QUANT, "PL": PLUR}, ("{PL}", lambda v: [s for s, p in zip(SING, PLUR) if p == v][0])),
    ("They own {Q} {PL} near the river.", {"Q": QUANT, "PL": PLUR}, ("{PL}", lambda v: [s for s, p in zip(SING, PLUR) if p == v][0])),
    ("They photographed {Q} {PL} during the trip.", {"Q": QUANT, "PL": PLUR}, ("{PL}", lambda v: [s for s, p in zip(SING, PLUR) if p == v][0])),
    ("I counted {Q} {PL} in the garden.", {"Q": QUANT, "PL": PLUR}, ("{PL}", lambda v: [s for s, p in zip(SING, PLUR) if p == v][0])),
]))

FAMILIES.append(fam("irr_plural", [
    ("We met {Q} {P} at the community centre.", {"Q": QUANT[:6], "P": [p for p, _ in IRRPL]}, ("{P}", lambda v: dict((p, w) for p, w in IRRPL)[v])),
    ("The doctor examined {Q} {P} carefully.", {"Q": QUANT[:6], "P": [p for p, _ in IRRPL]}, ("{P}", lambda v: dict((p, w) for p, w in IRRPL)[v])),
]))

FAMILIES.append(fam("quantifier", [
    ("There are too many {PL} in the {N}.", {"PL": PLUR[:40], "N": ["room", "hall", "building", "garden", "park", "street", "cabinet", "drawer", "crate", "wardrobe"]}, ("many", lambda v: "much")),
    ("She drank much {U} after the {N}.", {"U": UNC, "N": SING[:40]}, ("much", lambda v: "many")),
    ("We have fewer {PL} than last year.", {"PL": PLUR[:40]}, ("fewer", lambda v: "less")),
    ("He needs more {U} for the recipe.", {"U": UNC}, (None, None)),
]))

# ---- confusables (context-controlled)
CONF_FRAMES = [
    ("Their {N} is near the harbour.", {"N": SING}, ("Their", "There")),
    ("Their {N} received first prize.", {"N": SING}, ("Their", "They're")),
    ("There is a {N} near the station.", {"N": SING}, ("There", "Their")),
    ("There are several {PL} on the shelf.", {"PL": PLUR}, ("There", "Their")),
    ("They're going to the {N} tomorrow.", {"N": SING}, ("They're", "Their")),
    ("They're learning {L} this year.", {"L": LANGS}, ("They're", "There")),
    ("Your {N} was the best in the class.", {"N": SING}, ("Your", "You're")),
    ("Your {PL} will love this photograph.", {"PL": PLUR}, ("Your", "You're")),
    ("You're welcome to join the {N}.", {"N": SING}, ("You're", "Your")),
    ("You're doing a great job this {D}.", {"D": DAYS}, ("You're", "Your")),
    ("The cat licked its {N} after dinner.", {"N": SING}, ("its", "it's")),
    ("The company revised its {N}.", {"N": SING}, ("its", "it's")),
    ("It's raining in {C} today.", {"C": CITIES}, ("It's", "Its")),
    ("It's important to check the {N}.", {"N": SING}, ("It's", "Its")),
    ("I want to {VB} the {N} tonight.", {"VB": [b for b in VERBS if b in ("read", "watch", "open", "close", "clean", "fix", "carry", "wash", "check", "photograph", "review", "order", "describe", "measure")], "N": SING}, (" to ", " too ")),
    ("We are going to the {N} on {D}.", {"N": SING, "D": DAYS}, (" to ", " too ")),
    ("The {N} is too {ADJ} to carry.", {"N": SING, "ADJ": ADJ2}, (" too ", " to ")),
    ("This {N} is too {ADJ} for the trip.", {"N": SING, "ADJ": ADJ2}, (" too ", " to ")),
    ("She is {ADJ} than her brother.", {"ADJ": ["taller", "shorter", "stronger", "quieter", "braver", "calmer", "faster", "slower"]}, (" than ", " then ")),
    ("The {N} was harder than the practice test.", {"N": SING}, (" than ", " then ")),
    ("We finished the {N}, then we played chess.", {"N": SING}, (" then ", " than ")),
    ("First we studied, then we walked to the {N}.", {"N": SING}, (" then ", " than ")),
]
FAMILIES.append({"cat": "confusable", "frames": CONF_FRAMES})

# ---- negation (double negatives + clean)
FAMILIES.append(fam("double_neg", [
    ("I didn't see anything unusual at the {N}.", {"N": SING[:40]}, ("anything", lambda v: "nothing")),
    ("I didn't do anything about the {N}.", {"N": SING[:40]}, ("anything", lambda v: "nothing")),
    ("They didn't go anywhere near the {N}.", {"N": SING[:40]}, ("anywhere", lambda v: "nowhere")),
    ("We don't know anything about the {N}.", {"N": SING[:40]}, ("anything", lambda v: "nothing")),
    ("She hasn't told anybody about the {N}.", {"N": SING[:40]}, ("anybody", lambda v: "nobody")),
    ("He can't find anything in the {N}.", {"N": SING[:40]}, ("anything", lambda v: "nothing")),
    ("They couldn't hear anybody near the {N}.", {"N": SING[:40]}, ("anybody", lambda v: "nobody")),
    ("I won't tell anybody about the {N}.", {"N": SING[:40]}, ("anybody", lambda v: "nobody")),
    ("I haven't changed anything in the {N}.", {"N": SING[:40]}, ("anything", lambda v: "nothing")),
    ("We didn't eat anything at the {N}.", {"N": SING[:40]}, ("anything", lambda v: "nothing")),
    ("They never buy anything from the {N}.", {"N": SING[:40]}, ("anything", lambda v: "nothing")),
    ("You shouldn't ignore anything in the {N}.", {"N": SING[:40]}, ("anything", lambda v: "nothing")),
    ("The team hasn't finished anything on the {N}.", {"N": SING[:40]}, ("anything", lambda v: "nothing")),
    ("Our class didn't discuss anything about the {N}.", {"N": SING[:40]}, ("anything", lambda v: "nothing")),
]))

# ---- adj/adv
FAMILIES.append(fam("adjadv", [
    ("Our teacher {V3} {ADV} during the lesson.", {"V3": list(V3.values()), "ADV": ADV2}, ("{ADV}", lambda v: v[:-2] if v.endswith("ly") else v)),
    ("{S} {V3} the {N} {ADV}.", {"S": SUBJ[:8], "V3": TRANS3, "N": SING, "ADV": ADV2}, ("{ADV}", lambda v: v[:-2] if v.endswith("ly") else v)),
    ("The train arrived {ADV} at the station.", {"ADV": ADV2}, ("{ADV}", lambda v: v[:-2] if v.endswith("ly") else v)),
    ("She speaks {ADV} in the interview.", {"ADV": ADV2}, ("{ADV}", lambda v: v[:-2] if v.endswith("ly") else v)),
]))

# ---- comparative
FAMILIES.append(fam("comparative", [
    ("This route is {ADJ} than the old {N}.", {"ADJ": ["better", "easier", "harder", "faster", "cheaper", "stronger", "taller", "cleaner", "simpler", "younger"], "N": SING[:40]}, ("{ADJ}", lambda v: "more " + v)),
    ("That was the {SUP} {N} of the term.", {"SUP": ["easiest", "hardest", "fastest", "cheapest", "strongest", "tallest", "cleanest", "simplest", "youngest", "busiest"], "N": SING[:40]}, ("{SUP}", lambda v: "most " + v)),
]))

# ---- contractions
FAMILIES.append(fam("contraction", [
    ("{S} {C} need any help with the {N} today.", {"S": ["I", "They", "We"], "C": ["don't", "won't", "can't", "couldn't", "shouldn't"], "N": SING[:40]}, ("{C}", lambda v: v.replace("'", ""))),
    ("{S} {C} attend the morning session.", {"S": ["They", "We", "You"], "C": ["can't", "won't", "didn't", "haven't", "shouldn't", "couldn't", "wouldn't"]}, ("{C}", lambda v: v.replace("'", ""))),
    ("{S} {C} finish the {N} before Friday.", {"S": ["They", "We", "You"], "C": ["won't", "can't", "haven't", "didn't"], "N": SING[:40]}, ("{C}", lambda v: v.replace("'", ""))),
    ("{S} {C} live near the {N} anymore.", {"S": ["They", "We"], "C": ["don't", "didn't", "haven't"], "N": SING[:40]}, ("{C}", lambda v: v.replace("'", ""))),
    ("{S} {C} receive the invitation for the {N}.", {"S": ["They", "We"], "C": ["didn't", "haven't", "wouldn't"], "N": SING[:40]}, ("{C}", lambda v: v.replace("'", ""))),
    ("{S} {C} ready for the {N} yet.", {"S": ["They", "We"], "C": ["aren't", "weren't"]}, ("{C}", lambda v: v.replace("'", ""))),
    ("{S} {C} impressed by the {N}.", {"S": ["They", "We"], "C": ["weren't", "aren't", "wouldn't be"]}, ("{C}", lambda v: v.replace("'", ""))),
    ("{S} {C} replied to my email about the {N}.", {"S": ["They", "She", "He"], "C": ["hasn't", "hadn't", "didn't"]}, ("{C}", lambda v: v.replace("'", ""))),
    ("{S} {C} find the {N} anywhere.", {"S": ["They", "We"], "C": ["couldn't", "can't", "didn't"], "N": SING[:40]}, ("{C}", lambda v: v.replace("'", ""))),
    ("{S} {C} booked the venue for the {N}.", {"S": ["They", "We"], "C": ["haven't", "hadn't", "didn't"], "N": SING[:40]}, ("{C}", lambda v: v.replace("'", ""))),
    ("{S} {C} read the appendix of the {N}.", {"S": ["They", "We"], "C": ["hadn't", "haven't"], "N": SING[:40]}, ("{C}", lambda v: v.replace("'", ""))),
    ("{S} {C} ignore the warning about the {N}.", {"S": ["They", "We", "You"], "C": ["shouldn't", "wouldn't"], "N": SING[:40]}, ("{C}", lambda v: v.replace("'", ""))),
    ("{S} {C} change the design of the {N}.", {"S": ["They", "We", "I"], "C": ["wouldn't", "couldn't", "didn't"], "N": SING[:40]}, ("{C}", lambda v: v.replace("'", ""))),
    ("{S} {C} working on the {N} now.", {"S": ["They", "We"], "C": ["aren't", "weren't"], "N": SING[:40]}, ("{C}", lambda v: v.replace("'", ""))),
    ("{S} {C} at the workshop about the {N} yesterday.", {"S": ["They", "We"], "C": ["weren't"]}, ("{C}", lambda v: v.replace("'", ""))),
    ("{S} {C} on the guest list for the {N}.", {"S": ["They", "We"], "C": ["aren't", "weren't"]}, ("{C}", lambda v: v.replace("'", ""))),
    ("{S} {C} writing to confirm the {N}.", {"S": ["I'm"], "C": ["I'm"], "N": SING[:20]}, ("{C}", lambda v: "im")),
    ("{S} {C} attached the latest {N}.", {"S": ["I've"], "C": ["I've"], "N": SING[:20]}, ("{C}", lambda v: "ive")),
    ("{S} {C} moving to Dunedin in March.", {"S": ["They're"], "C": ["They're"]}, ("{C}", lambda v: "theyre")),
    ("{S} {C} eligible for the discount.", {"S": ["You're"], "C": ["You're"]}, ("{C}", lambda v: "youre")),
    ("{S} {C} a new café near the office.", {"S": ["There's"], "C": ["There's"]}, ("{C}", lambda v: "theres")),
    ("{S} {C} leading the design review.", {"S": ["She's"], "C": ["She's"]}, ("{C}", lambda v: "shes")),
    ("{S} {C} review the figures again.", {"S": ["Let's"], "C": ["Let's"]}, ("{C}", lambda v: "lets")),
    ("{S} {C} finished the {N} yet.", {"S": ["She", "He", "Priya"], "C": ["hasn't", "hadn't", "hasn't"], "N": SING[:30]}, ("{C}", lambda v: v.replace("'", ""))),
]))

# ---- capitalization
FAMILIES.append(fam("capitalization", [
    ("The meeting is scheduled for {D} next week.", {"D": DAYS}, ("{D}", lambda v: v.lower())),
    ("The report is due at the end of {M}.", {"M": MONTHS}, ("{M}", lambda v: v.lower())),
    ("Our branch office in {C} is closing early.", {"C": CITIES}, ("{C}", lambda v: v.lower())),
    ("She is fluent in {L}.", {"L": LANGS}, ("{L}", lambda v: v.lower())),
    ("We visited {C} during the {M} holidays.", {"C": CITIES, "M": MONTHS}, ("{C}", lambda v: v.lower())),
    ("The {D} workshop covered {L} grammar.", {"D": DAYS, "L": LANGS}, ("{D}", lambda v: v.lower())),
    ("We travelled to {C} to study {L}.", {"C": CITIES, "L": LANGS}, ("{C}", lambda v: v.lower())),
    ("The {M} report includes the {N} figures.", {"M": MONTHS, "N": SING[:30]}, ("{M}", lambda v: v.lower())),
    ("Our {D} lecture on {L} history was full.", {"D": DAYS, "L": LANGS}, ("{D}", lambda v: v.lower())),
]))

# ---- punctuation
FAMILIES.append(fam("punct_period", [
    ("We finished the {N} and submitted the {N2}.", {"N": SING[:40], "N2": SING[:40]}, (".", lambda v: "")),
    ("Our team completed the {N} on schedule.", {"N": SING[:40]}, (".", lambda v: "")),
    ("She attended all four {PL}.", {"PL": PLUR[:40]}, (".", lambda v: "")),
    ("I have attached the revised {N}.", {"N": SING[:40]}, (".", lambda v: "")),
    ("They photographed the old {N} near the harbour.", {"N": SING[:40]}, (".", lambda v: "")),
    ("Our manager reviewed the {N} in the afternoon.", {"N": SING[:40]}, (".", lambda v: "")),
    ("The students organised the {N} for the fair.", {"N": SING[:40]}, (".", lambda v: "")),
    ("We photographed the {N} near the station.", {"N": SING[:40]}, (".", lambda v: "")),
]))

FAMILIES.append(fam("punct_question", [
    ("Did you finish the {N}?", {"N": SING}, ("?", lambda v: ".")),
    ("Can you send the {N} today?", {"N": SING}, ("?", lambda v: ".")),
    ("Will the office be open on {D}?", {"D": DAYS}, ("?", lambda v: ".")),
    ("Have they signed the {N}?", {"N": SING}, ("?", lambda v: ".")),
]))

# ---- repetition
FAMILIES.append(fam("repetition", [
    ("I filed the {N} in the cabinet yesterday.", {"N": SING}, ("the {N}", lambda v: "the the " + v)),
    ("We photographed the {N} during the tour.", {"N": SING}, ("the {N}", lambda v: "the the " + v)),
    ("She opened the {N} before the meeting.", {"N": SING}, ("the {N}", lambda v: "the the " + v)),
]))

# ---- prepositions
FAMILIES.append(fam("preposition", [
    ("This design is different from the previous {N}.", {"N": SING[:40]}, ("different from", lambda v: "different than")),
    ("The outcome depends on the {N}.", {"N": SING[:40]}, ("depends on", lambda v: "depends of")),
    ("The kit consists of three {PL}.", {"PL": PLUR[:40]}, ("consists of", lambda v: "consists in")),
    ("She is good at solving difficult {PL}.", {"PL": PLUR[:40]}, ("good at", lambda v: "good in")),
    ("They are interested in joining the {N}.", {"N": SING[:40]}, ("interested in", lambda v: "interested to")),
    ("He is afraid of large {PL}.", {"PL": PLUR[:40]}, ("afraid of", lambda v: "afraid from")),
    ("This approach is similar to the old {N}.", {"N": SING[:40]}, ("similar to", lambda v: "similar with")),
    ("The team is capable of delivering the {N}.", {"N": SING[:40]}, ("capable of", lambda v: "capable to")),
    ("The city is famous for its {N}.", {"N": SING[:40]}, ("famous for", lambda v: "famous in")),
    ("We are keen on trying new {PL}.", {"PL": PLUR[:40]}, ("keen on", lambda v: "keen of")),
    ("Priya is married to a nurse from {C}.", {"C": CITIES}, ("married to", lambda v: "married with")),
]))

# ---- redundancy
FAMILIES.append(fam("redundancy", [
    ("Please return the {N} before Friday.", {"N": SING[:40]}, ("return", lambda v: "return back")),
    ("I will reply to your {N} shortly.", {"N": SING[:40]}, ("reply to", lambda v: "reply back to")),
    ("She reverted to the earlier {N}.", {"N": SING[:40]}, ("reverted to", lambda v: "reverted back to")),
    ("We discussed the {N} in depth.", {"N": SING[:40]}, ("discussed", lambda v: "discussed about")),
    ("They entered the {N} at nine.", {"N": SING[:40]}, ("entered", lambda v: "entered into")),
    ("The guide comprises three {PL}.", {"PL": PLUR[:40]}, ("comprises", lambda v: "comprises of")),
    ("The cat jumped off the {N}.", {"N": SING[:40]}, ("off the", lambda v: "off of the")),
    ("The results were equally good for the {N}.", {"N": SING[:40]}, ("equally", lambda v: "equally as")),
]))

# ---- verb+ing
ING_V = [b for b in ("enjoy", "avoid", "finish", "keep", "practise", "consider") if b in VERBS]
ING_ACT = ["reading", "swimming", "walking", "cooking", "writing", "singing",
           "drawing", "camping", "fishing", "dancing", "tramping",
           "gardening", "painting", "baking"]
ING2BASE = {"reading": "read", "swimming": "swim", "walking": "walk",
            "cooking": "cook", "writing": "write", "singing": "sing",
            "drawing": "draw", "camping": "camp", "fishing": "fish",
            "dancing": "dance", "tramping": "tramp", "gardening": "garden",
            "painting": "paint", "baking": "bake", "running": "run"}
FAMILIES.append(fam("verb_ing", [
    ("{S} {V3} {ACT} every weekend.", {"S": SUBJ[:8], "V3": [VERBS[b][0] for b in ING_V], "ACT": ING_ACT}, ("{ACT}", lambda v: "to " + ING2BASE.get(v, v[:-3]))),
    ("We {VB} {ACT} on Saturdays.", {"VB": ING_V, "ACT": ING_ACT}, ("{ACT}", lambda v: "to " + ING2BASE.get(v, v[:-3]))),
    ("She {V3} {ACT} after dinner.", {"V3": [VERBS[b][0] for b in ING_V[:4]], "ACT": ING_ACT}, ("{ACT}", lambda v: "to " + ING2BASE.get(v, v[:-3]))),
]))

# ---- spelling
FAMILIES.append(fam("spelling", [
    ("We received the {N} on Monday.", {"N": SING[:40]}, ("received", lambda v: "recieved")),
    ("She received the invitation for the {N}.", {"N": SING[:40]}, ("received", lambda v: "recieved")),
    ("We must separate the {N} by year.", {"N": SING[:40]}, ("separate", lambda v: "seperate")),
    ("I will definitely attend the {N}.", {"N": SING[:40]}, ("definitely", lambda v: "definately")),
    ("The rehearsal continued until the {N} was ready.", {"N": SING[:40]}, ("until", lambda v: "untill")),
    ("I'm not sure which {N} is better.", {"N": SING[:40]}, ("which", lambda v: "wich")),
    ("She couldn't decide because of the {N}.", {"N": SING[:40]}, ("because", lambda v: "becuase")),
    ("I believe the {N} is correct.", {"N": SING[:40]}, ("believe", lambda v: "beleive")),
    ("They want to achieve a better {N}.", {"N": SING[:40]}, ("achieve", lambda v: "acheive")),
    ("Please write to our address about the {N}.", {"N": SING[:40]}, ("address", lambda v: "adress")),
    ("The calendar is full of {PL} this month.", {"PL": PLUR[:40]}, ("calendar", lambda v: "calender")),
    ("Check the grammar before submitting the {N}.", {"N": SING[:40]}, ("grammar", lambda v: "grammer")),
    ("Our friends visited in February from the {N}.", {"N": SING[:40]}, ("February", lambda v: "Febuary")),
    ("He borrowed a book about the {N}.", {"N": SING[:40]}, ("book", lambda v: "bok")),
    ("The restaurant near the {N} was excellent.", {"N": SING[:40]}, ("restaurant", lambda v: "restaraunt")),
    ("We are grateful for the {N}.", {"N": SING[:40]}, ("grateful", lambda v: "greatful")),
    ("She is an independent reviewer of the {N}.", {"N": SING[:40]}, ("independent", lambda v: "independant")),
    ("The committee discussed the {N}.", {"N": SING[:40]}, ("committee", lambda v: "commitee")),
    ("This is a great opportunity for the {N}.", {"N": SING[:40]}, ("opportunity", lambda v: "opertunity")),
    ("The weather affected the {N}.", {"N": SING[:40]}, ("weather", lambda v: "wether")),
    ("The government published the {N}.", {"N": SING[:40]}, ("government", lambda v: "goverment")),
    ("The environment committee met about the {N}.", {"N": SING[:40]}, ("environment", lambda v: "enviroment")),
    ("Please confirm the necessary {PL}.", {"PL": PLUR[:40]}, ("necessary", lambda v: "neccessary")),
    ("The occasion required a formal {N}.", {"N": SING[:40]}, ("occasion", lambda v: "occassion")),
]))

# ---- corrupted technical family (grammar errors around protected tech terms)
FAMILIES.append({"cat": "sva_3sg", "domain": "technical", "tag": "tech", "frames": [
    ("The {T} service {V3} the {N} in production.", {"T": TECH, "V3": ["runs", "handles", "checks", "verifies"], "N": SING[:12]}, ("{V3}", lambda v: {"runs": "run", "handles": "handle", "checks": "check", "verifies": "verify"}[v])),
    ("The {T} pipeline {V3} every night.", {"T": TECH, "V3": ["runs", "rotates"]}, ("{V3}", lambda v: {"runs": "run", "rotates": "rotate"}[v])),
    ("Our {T} dashboard show the metrics.", {"T": TECH}, ("show", lambda v: "shows")),
    ("The {T} config file was changed yesterday.", {"T": TECH}, ("was", lambda v: "were")),
]})

# ------------------------------------------------- clean-only families
FAMILIES.append({"cat": None, "domain": "technical",
    "tag": "tech",
    "frames": [
    ("The {T} service {V3} the {N} in production.", {"T": TECH, "V3": list(V3.values())[:20], "N": SING[:20]}, None),
    ("Our team deployed {T} on {D}.", {"T": TECH, "D": DAYS}, None),
    ("The {T} configuration {V3} the request payload.", {"T": TECH, "V3": list(V3.values())[:20]}, None),
    ("We reviewed the {T} logs before the meeting.", {"T": TECH}, None),
    ("The {T} dashboard refreshes every {Q} minutes.", {"T": TECH, "Q": QUANT[:6]}, None),
    ("Documentation for {T} is available online.", {"T": TECH}, None),
    ("The {T} {A} the data every night.", {"T": TECH, "A": ["back up", "validate", "archive", "audit"]}, None),
]})

FAMILIES.append({"cat": None, "domain": "professional", "tag": "names",
    "frames": [
    ("{NM} {A2}.", {"NM": NAMES, "A2": NAME_ACT}, None),
    ("{NM} and {NM2} coordinated the event.", {"NM": NAMES, "NM2": NAMES}, None),
    ("We emailed {NM} about the {N}.", {"NM": NAMES, "N": SING[:15]}, None),
    ("{NM} sent the {N} to our office.", {"NM": NAMES, "N": SING[:15]}, None),
]})

NUMB_FRAME = [
    ("The invoice totalled {AM} including GST.", {"AM": ["$1,234.50", "$842.00", "$97.25", "$12,345.90", "$56.10"]}, None),
    ("Our office is open from {T1} to {T2}.", {"T1": ["9:00 a.m.", "8:30 a.m.", "10:00 a.m."], "T2": ["5:30 p.m.", "4:45 p.m.", "6:00 p.m."]}, None),
    ("She paid {AM} for the ticket.", {"AM": ["$42", "$17.50", "$230", "$1,025"]}, None),
    ("The population reached {NUM} in 2019.", {"NUM": ["5.12 million", "4.9 million", "6.2 million"]}, None),
    ("We ordered {CNT} boxes and {CNT2} pens.", {"CNT": ["15", "24", "30"], "CNT2": ["240", "120", "300"]}, None),
    ("The survey covered {N} respondents.", {"N": ["1,500", "2,300", "850"]}, None),
    ("The recipe uses {GR} of flour.", {"GR": ["250 g", "300 g", "180 g"]}, None),
    ("He ran {KM} in {HRS}.", {"KM": ["42.2 km", "21.1 km", "10 km"], "HRS": ["3 hours 51 minutes", "1 hour 45 minutes", "50 minutes"]}, None),
    ("The discount is {PC}, so you save {SAVE}.", {"PC": ["20%", "15%", "25%"], "SAVE": ["$19.80", "$12.75", "$31.20"]}, None),
    ("Room {RM} is on the {F} floor.", {"RM": ["12B", "7A", "3C"], "F": ["fourth", "second", "tenth"]}, None),
    ("Pi is approximately {PI} in this calculation.", {"PI": ["3.14159", "3.14", "2.71828"]}, None),
]
FAMILIES.append({"cat": None, "domain": "professional", "tag": "numbers", "frames": NUMB_FRAME})

DATE_FRAME = [
    ("The meeting runs from {D1} to {D2}.", {"D1": ["21 March 2025", "3 April 2025", "18 June 2024", "30 September 2025"], "D2": ["25 March 2025", "9 April 2025", "2 July 2024", "3 October 2025"]}, None),
    ("They arrived on {D1} and left on {D2}.", {"D1": ["3/04/2025", "12/06/2024", "28/02/2025"], "D2": ["12/04/2025", "25/06/2024", "7/03/2025"]}, None),
    ("The contract was signed on {D1}.", {"D1": ["14 May 2025", "2 August 2024", "27 November 2024", "1 January 2025"]}, None),
    ("O'Connell signed the contract on {D1}.", {"D1": ["14 May 2025", "2 August 2024"]}, None),
    ("The deadline is {D1} at {T}.", {"D1": ["30 June", "15 August", "1 October"], "T": ["5 p.m.", "noon", "9 a.m."]}, None),
    ("Our branch reopened on {D1} after the renovation.", {"D1": ["22 January 2025", "17 March 2024", "8 July 2023"]}, None),
]
FAMILIES.append({"cat": None, "domain": "professional", "tag": "dates", "frames": DATE_FRAME})

QUOTE_FRAME = [
    ("The reviewer wrote, {Q}", {"Q": ['"a quietly brilliant debut."', '"a masterful performance."', '"an ambitious, uneven novel."']}, None),
    ("Our principal said, {Q}", {"Q": ['"attendance has improved this term."', '"the rebuild finishes in July."']}, None),
    ("{Q} she said as she welcomed the visitors.", {"Q": ['"Kia ora,"', '"Nau mai,"', '"Haere mai,"']}, None),
    ("The notice read: {Q}", {"Q": ['"closed until further notice."', '"no entry after 5 p.m."']}, None),
    ("He asked, {Q}", {"Q": ['"did anyone see the missing file?"', '"who updated the roster?"']}, None),
    ("The email began, {Q}", {"Q": ['"thank you for your prompt reply."', '"we regret the delay in responding."']}, None),
    ("{Q} the captain announced proudly.", {"Q": ['"We won the debate,"', '"We topped the group,"']}, None),
    ("The headline read, {Q}", {"Q": ['"Council approves the new cycleway."', '"Rates rise 3.2 percent."']}, None),
]
FAMILIES.append({"cat": None, "domain": "professional", "tag": "quotes", "frames": QUOTE_FRAME})

UKF = [
    ("We {V3} the {U} yesterday.", {"V3": ["organised", "painted", "reviewed", "catalogued"], "U": [u for u, _ in UKSPELL]}, None),
    ("She {V3} the {U} last night.", {"V3": ["chose", "coloured", "measured"], "U": [u for u, _ in UKSPELL]}, None),
    ("The {U} looks perfect in the programme.", {"U": [u for u, _ in UKSPELL]}, None),
    ("I {V2} the {U} to the centre of town.", {"V2": ["walked", "carried"], "U": [u for u, _ in UKSPELL]}, None),
]
FAMILIES.append({"cat": None, "domain": "essay", "tag": "uk", "frames": UKF})

USF = [
    ("We {V3} the {U} yesterday.", {"V3": ["organized", "painted", "reviewed", "catalogued"], "U": [u for _, u in UKSPELL]}, None),
    ("She {V3} the {U} last night.", {"V3": ["chose", "colored", "measured"], "U": [u for _, u in UKSPELL]}, None),
    ("The {U} looks perfect in the program.", {"U": [u for _, u in UKSPELL]}, None),
]
FAMILIES.append({"cat": None, "domain": "essay", "tag": "us", "frames": USF})

NZF = [
    ("We went {ACT} near Lake Waikaremoana last {T}.", {"ACT": ["tramping", "camping", "fishing"], "T": ["fortnight", "January", "summer"]}, None),
    ("He drove the ute to the {T} for the long weekend.", {"T": ["bach", "farm", "marae"]}, None),
    ("Grab some {T} from the dairy on the way home.", {"T": ["pies", "bread", "milk"]}, None),
    ("The kids wore {T} at the beach.", {"T": ["togs", "togs and jandals", "swimming gear"]}, None),
    ("There's {T} of kai at the shared table.", {"T": ["heaps", "plenty", "stacks"]}, None),
    ("The {T} behind the dairy leads to the school.", {"T": ["footpath", "path", "track"]}, None),
    ("{Q}, the crew finished the job early.", {"Q": ["Sweet as", "Choice", "Ka pai"]}, None),
    ("Kia ora, welcome to our {T}.", {"T": ["little slice of paradise", "new classroom", "community hall"]}, None),
    ("{NM} is learning te reo Māori at the kura.", {"NM": NAMES[:12]}, None),
]
FAMILIES.append({"cat": None, "domain": "essay", "tag": "nz", "frames": NZF})

NEGF = [
    ("I didn't see anything unusual at the {N}.", {"N": SING[:15]}, None),
    ("Nobody in the team knew the {N}.", {"N": SING[:15]}, None),
    ("Hardly anyone noticed the {N}.", {"N": SING[:15]}, None),
    ("She never says anything unkind about the {N}.", {"N": SING[:15]}, None),
    ("We couldn't find any {PL} near the venue.", {"PL": PLUR[:15]}, None),
    ("There wasn't anybody at {T} this morning.", {"T": ["reception", "the counter", "the gate"]}, None),
    ("They don't need anything else from the {N}.", {"N": SING[:15]}, None),
    ("Scarcely a {N} passes without a new report.", {"N": ["week", "month", "quarter"]}, None),
]
FAMILIES.append({"cat": None, "domain": "essay", "tag": "negation", "frames": NEGF})

ESSAYF = [
    ("Learning a second language requires {T}.", {"T": ["patience and daily practice", "discipline and curiosity"]}, None),
    ("Reading widely improves both {T}.", {"T": ["vocabulary and critical thinking", "fluency and comprehension"]}, None),
    ("Exercise helps students {T}.", {"T": ["concentrate during long lessons", "sleep better at night"]}, None),
    ("Our school fundraiser was a {T} this year.", {"T": ["great success", "huge achievement"]}, None),
    ("Volunteering at the food bank taught me about {T}.", {"T": ["teamwork", "community service"]}, None),
    ("The science fair projects impressed {T}.", {"T": ["all the judges", "every visitor"]}, None),
    ("Climate change affects {T}.", {"T": ["farming communities", "coastal towns", "the whole region"]}, None),
    ("Public libraries offer free access to {T}.", {"T": ["books and quiet spaces", "learning resources"]}, None),
    ("Teamwork makes difficult {T} easier to complete.", {"T": ["projects", "assignments"]}, None),
    ("The debating team won the {T}.", {"T": ["regional finals", "inter-school title"]}, None),
    ("Every student deserves a safe and supportive {T}.", {"T": ["classroom", "learning environment"]}, None),
    ("Music education develops {T}.", {"T": ["discipline as well as creativity", "confidence and focus"]}, None),
    ("A balanced diet and enough sleep improve {T}.", {"T": ["exam performance", "memory and mood"]}, None),
    ("The new cycleway makes the trip to school {T}.", {"T": ["safer", "quicker and safer"]}, None),
    ("Writing by hand helps some learners {T}.", {"T": ["remember more effectively", "organise their ideas"]}, None),
    ("Our kapa haka group performed at the {T}.", {"T": ["regional festival", "national competition"]}, None),
]
FAMILIES.append({"cat": None, "domain": "essay", "tag": "essay", "frames": ESSAYF})

PROFF = [
    ("Please {V} the attached {N} before Friday.", {"V": ["review", "approve", "sign"], "N": ["contract", "report", "invoice", "proposal"]}, None),
    ("I am writing to {V} our meeting on {D}.", {"V": ["confirm", "reschedule", "follow up on"], "D": DAYS}, None),
    ("Our team {V2} the {N} last quarter.", {"V2": ["completed", "delivered", "audited"], "N": ["migration", "review", "rollout", "assessment"]}, None),
    ("The {N} will be circulated {T}.", {"N": ["minutes", "summary", "budget", "timeline"], "T": ["tomorrow morning", "this afternoon", "on Monday"]}, None),
    ("Thank you for your prompt reply regarding the {N}.", {"N": ["invoice", "booking", "application", "quotation"]}, None),
    ("We appreciate your {N} on this matter.", {"N": ["patience", "feedback", "understanding"]}, None),
    ("The client {V2} the revised proposal.", {"V2": ["accepted", "approved", "reviewed"]}, None),
    ("Kindly {V} the invoice at your earliest convenience.", {"V": ["settle", "process", "verify"]}, None),
]
FAMILIES.append({"cat": None, "domain": "professional", "tag": "professional", "frames": PROFF})

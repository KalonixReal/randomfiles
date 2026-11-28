# -*- coding: utf-8 -*-
"""Expanded word bank + richer template families for the sentence generator.
Goal: word vocab ~8-12k, natural clause variety, subject/verb/number agreement
always controlled."""

PEOPLE_S = ["sister", "brother", "cousin", "friend", "neighbour", "teacher", "manager",
            "colleague", "supervisor", "librarian", "technician", "engineer", "nurse",
            "architect", "clerk", "cashier", "inspector", "plumber", "builder", "farmer",
            "driver", "writer", "editor", "designer", "accountant", "lawyer", "dentist",
            "surgeon", "mechanic", "electrician", "tailor", "baker", "chef", "barista",
            "florist", "gardener", "janitor", "porter", "guide", "sailor", "pilot",
            "student", "tutor", "professor", "mentor", "intern", "trainee", "recruiter",
            "advisor", "analyst", "auditor", "consultant", "director", "secretary",
            "receptionist", "journalist", "photographer", "translator", "interpreter"]
NAMES = ["James", "Priya", "Sione", "Mei", "Aroha", "Tane", "Ava", "Oscar", "Lucy", "Ben",
         "Hemi", "Anahera", "Rewa", "Kofi", "Alvaro", "Nadia", "Sara", "Omar", "Elena",
         "Kenji", "Fatima", "Yusuf", "Amita", "Ivon", "Hana", "Mika", "Leilani", "Rangi",
         "Kauri", "Mere", "Whetu", "Ana", "Sela", "Tama", "Rangi", "Ngaio", "Ihaia",
         "Mrs Taylor", "Mr Hayes", "Dr Ling", "Aunt Hine", "Uncle Pita", "Nana Ria",
         "Grandad Joe", "Gran Lily", "Mr Wu", "Mrs Rao", "Dr Kaneko", "Ms Reid"]
PEOPLE_PL = ["students", "friends", "classmates", "neighbours", "children", "interns",
             "teachers", "engineers", "inspectors", "auditors", "visitors", "volunteers",
             "cousins", "reporters", "editors", "designers", "accountants", "clerks",
             "waiters", "farmers", "builders", "nurses", "drivers", "guides", "pilots",
             "sailors", "chefs", "bakers", "baristas", "florists", "gardeners", "porters"]
NOUNS_SG = ["report", "letter", "parcel", "invoice", "article", "contract", "plugin",
             "driver", "script", "survey", "lecture", "meeting", "concert", "festival",
             "trial", "webinar", "upgrade", "backup", "recipe", "booklet", "brochure",
             "catalogue", "timetable", "receipt", "ticket", "manual", "transcript",
             "licence", "assignment", "essay", "portfolio", "notebook", "checklist",
             "form", "folder", "envelope", "postcard", "voucher", "badge", "banner",
             "poster", "painting", "photograph", "sculpture", "ornament", "lantern",
             "basket", "blanket", "cushion", "curtain", "mirror", "carpet", "cabinet",
             "shelf", "bench", "toolbox", "engine", "battery", "pump", "valve", "gasket",
             "filter", "bracket", "panel", "switch", "socket", "charger", "cable",
             "laptop", "monitor", "printer", "scanner", "camera", "tripod", "ladder",
             "trolley", "barrow", "trailer", "caravan", "kayak", "bicycle", "scooter"]
NOUNS_PL = ["reports", "letters", "parcels", "invoices", "articles", "contracts",
            "plugins", "scripts", "surveys", "lectures", "meetings", "concerts",
            "festivals", "trials", "webinars", "upgrades", "backups", "recipes",
            "booklets", "brochures", "catalogues", "timetables", "receipts", "tickets",
            "manuals", "transcripts", "licences", "assignments", "essays", "portfolios",
            "notebooks", "checklists", "forms", "folders", "envelopes", "postcards",
            "vouchers", "badges", "banners", "posters", "paintings", "photographs",
            "sculptures", "ornaments", "lanterns", "baskets", "blankets", "cushions",
            "curtains", "mirrors", "carpets", "cabinets", "shelves", "benches",
            "toolboxes", "engines", "batteries", "pumps", "valves", "gaskets", "filters",
            "brackets", "panels", "switches", "sockets", "chargers", "cables", "laptops",
            "monitors", "printers", "scanners", "cameras", "tripods", "ladders",
            "trolleys", "barrows", "trailers", "caravans", "kayaks", "bicycles"]
VERB_SG = ["walks", "reads", "writes", "sends", "completes", "reviews", "finishes",
            "drafts", "checks", "files", "signs", "shares", "books", "collects", "prints",
            "returns", "picks", "covers", "uploads", "exports", "installs", "cancels",
            "borrows", "lends", "opens", "closes", "shuts", "starts", "stops", "keeps",
            "drops", "grabs", "moves", "fixes", "mends", "paints", "draws", "sketches",
            "measures", "weighs", "counts", "sorts", "packs", "wraps", "seals", "stacks",
            "washes", "cleans", "rinses", "dries", "irons", "folds", "hangs", "stores",
            "carries", "lifts", "pushes", "pulls", "tows", "parks", "drives", "rides",
            "rowboats", "steers", "paddles", "cycles", "jogs", "walks", "sprints",
            "trains", "practises", "rehearses", "performs", "sings", "plays", "tunes",
            "records", "mixes", "bakes", "grills", "roasts", "chops", "peels", "stirs",
            "pours", "brews", "serves", "orders", "buys", "sells", "trades", "swaps",
            "wins", "loses", "earns", "saves", "spends", "owes", "pays", "quotes",
            "plans", "organises", "arranges", "hosts", "invites", "greets", "welcomes",
            "calls", "phones", "rings", "emails", "texts", "messages", "notifies",
            "reminds", "warns", "tells", "asks", "answers", "replies", "explains",
            "teaches", "guides", "leads", "shows", "points", "marks", "notes", "logs",
            "tracks", "monitors", "watches", "observes", "studies", "learns", "memorises",
            "recalls", "remembers", "forgets", "misses", "finds", "discovers", "uncovers",
            "reveals", "reports", "announces", "declares", "confirms", "verifies",
            "approves", "rejects", "accepts", "declines", "avoids", "delays", "defers",
            "postpones", "reschedules", "updates", "amends", "revises", "edits",
            "corrects", "adjusts", "adapts", "prepares", "cooks", "bakes", "makes",
            "builds", "creates", "designs", "models", "maps", "charts", "plots",
            "graphs", "sketches", "traces", "copies", "duplicates", "photocopies"]
VERB_PL = [v[:-1] if v.endswith("s") and not v.endswith("ss") else v for v in VERB_SG]
PAST_VERBS = ["walked", "read", "wrote", "sent", "completed", "reviewed", "finished",
              "drafted", "checked", "filed", "signed", "shared", "booked", "collected",
              "printed", "returned", "picked", "covered", "uploaded", "exported",
              "installed", "cancelled", "borrowed", "lended", "opened", "closed",
              "shut", "started", "stopped", "kept", "dropped", "grabbed", "moved",
              "fixed", "mended", "painted", "drew", "sketched", "measured", "weighed",
              "counted", "sorted", "packed", "wrapped", "sealed", "stacked", "washed",
              "cleaned", "rinsed", "dried", "ironed", "folded", "hung", "stored",
              "carried", "lifted", "pushed", "pulled", "towed", "parked", "drove",
              "rode", "steered", "paddled", "cycled", "jogged", "sprinted", "trained",
              "practised", "rehearsed", "performed", "sang", "played", "tuned",
              "recorded", "mixed", "baked", "grilled", "roasted", "chopped", "peeled",
              "stirred", "poured", "brewed", "served", "ordered", "bought", "sold",
              "traded", "swapped", "won", "lost", "earned", "saved", "spent", "owed",
              "paid", "quoted", "planned", "organised", "arranged", "hosted",
              "invited", "greeted", "welcomed", "called", "phoned", "rang", "emailed",
              "texted", "messaged", "notified", "reminded", "warned", "told", "asked",
              "answered", "replied", "explained", "taught", "guided", "led", "showed",
              "pointed", "marked", "noted", "logged", "tracked", "monitored",
              "watched", "observed", "studied", "learned", "memorised", "recalled",
              "remembered", "forgot", "missed", "found", "discovered", "uncovered",
              "revealed", "reported", "announced", "declared", "confirmed", "verified",
              "approved", "rejected", "accepted", "declined", "avoided", "delayed",
              "deferred", "postponed", "rescheduled", "updated", "amended", "revised",
              "edited", "corrected", "adjusted", "adapted", "prepared", "cooked",
              "made", "built", "created", "designed", "modelled", "mapped", "charted",
              "plotted", "traced", "copied", "duplicated", "photocopied"]
ADJ = ["detailed", "helpful", "useful", "practical", "thorough", "careful", "honest",
       "reliable", "punctual", "clear", "concise", "complete", "correct", "sensible",
       "thoughtful", "generous", "grateful", "cheerful", "polite", "patient", "calm",
       "quiet", "gentle", "kind", "brave", "bold", "clever", "smart", "wise", "eager",
       "curious", "focused", "steady", "hardworking", "efficient", "productive",
       "creative", "original", "modern", "traditional", "classic", "elegant",
       "spacious", "cosy", "tidy", "neat", "clean", "fresh", "bright", "sunny",
       "windy", "mild", "chilly", "warm", "cool", "dry", "damp", "smooth", "rough",
       "soft", "sturdy", "solid", "heavy", "lightweight", "compact", "portable",
       "affordable", "expensive", "popular", "famous", "well-known", "local", "organic",
       "seasonal", "annual", "weekly", "monthly", "daily", "urgent", "important",
       "essential", "necessary", "optional", "extra", "spare", "suitable", "perfect"]
ADV = ["quickly", "carefully", "immediately", "significantly", "beautifully", "badly",
       "rapidly", "sharply", "efficiently", "successfully", "quietly", "easily",
       "slowly", "gently", "firmly", "politely", "kindly", "calmly", "happily",
       "sadly", "gladly", "proudly", "boldly", "bravely", "cheerfully", "gratefully",
       "patiently", "eagerly", "curiously", "silently", "smoothly", "steadily",
       "regularly", "routinely", "promptly", "early", "later", "soon", "already",
       "finally", "eventually", "recently", "lately", "briefly", "suddenly",
       "constantly", "continuously", "publicly", "privately", "formally", "casually"]
PLACES = ["library", "office", "depot", "clinic", "campus", "counter", "warehouse",
          "studio", "marae", "hall", "workshop", "agency", "bakery", "bookshop",
          "butchery", "cafe", "canteen", "classroom", "courthouse", "dairy", "dormitory",
          "factory", "farmyard", "gallery", "garage", "garden", "gymnasium", "harbour",
          "hospital", "hostel", "kitchen", "laboratory", "laundry", "lecture room",
          "market", "museum", "newsroom", "orchard", "pharmacy", "printery",
          "reception", "restaurant", "retail store", "school hall", "stable",
          "station", "studio", "supermarket", "theatre", "veterinary clinic",
          "waiting room", "wharf"]
TIMEPH = ["every Tuesday", "every morning", "every week", "each afternoon", "each month",
          "before breakfast", "after work", "during the meeting", "on Mondays",
          "before the deadline", "after the inspection", "during the workshop",
          "by the end of the week", "before the audit", "after the briefing",
          "at midday", "at dawn", "by nightfall", "before dusk", "after supper",
          "each evening", "every winter", "each spring", "every autumn",
          "before the rehearsal", "after the tryout", "during the interval"]
PAST_MARKERS = ["Yesterday", "Last week", "Last month", "On Monday", "Last Tuesday",
                "Earlier today", "Last night", "Two days ago", "Last term", "Recently",
                "This morning", "Last Friday", "Last weekend", "Back in April",
                "At the weekend", "In the holidays"]
MODALS = ["can", "will", "should", "must", "might", "would", "could"]
WH = ["Where", "What", "When", "Why", "How"]
CONJ = ["because", "although", "while", "when", "since", "after", "before", "until", "so"]
NEGADV = ["never", "rarely", "seldom", "hardly", "barely"]


def cap_first(s):
    return s[0].upper() + s[1:] if s else s


import random


def gen_simple(rng):
    subj = cap_first(rng.choice(["the " + rng.choice(PEOPLE_S), rng.choice(NAMES)]))
    v = rng.choice(VERB_SG)
    o = "the " + rng.choice(NOUNS_SG if v not in VERB_SG else NOUNS_SG)
    t = rng.choice(TIMEPH)
    return f"{subj} {v} {o} {t}."


def gen_plural_subj(rng):
    subj = cap_first(rng.choice(PEOPLE_PL))
    v = rng.choice(VERB_PL)
    o = "the " + rng.choice(NOUNS_PL)
    t = rng.choice(TIMEPH)
    return f"{subj} {v} {o} {t}."


def gen_past(rng):
    m = rng.choice(PAST_MARKERS)
    subj = rng.choice(NAMES + ["the " + w for w in PEOPLE_S] + PEOPLE_PL)
    v = rng.choice(PAST_VERBS)
    o = "the " + rng.choice(NOUNS_SG + NOUNS_PL)
    return f"{m} {subj} {v} {o} in the {rng.choice(PLACES)}."


def gen_have_perfect(rng):
    if rng.random() < 0.5:
        subj = rng.choice(["the " + w for w in PEOPLE_S] + NAMES)
        v = rng.choice(PAST_VERBS)
        return f"{cap_first(subj)} has {v} the {rng.choice(NOUNS_SG)} already."
    subj = rng.choice(PEOPLE_PL)
    v = rng.choice(PAST_VERBS)
    return f"{cap_first(subj)} have {v} the {rng.choice(NOUNS_PL)} already."


def gen_be_adj(rng):
    if rng.random() < 0.5:
        subj = rng.choice(["the " + w for w in PEOPLE_S] + NAMES)
        adj = rng.choice(ADJ)
        return f"{cap_first(subj)} is {adj} about the {rng.choice(NOUNS_SG)}."
    subj = rng.choice(PEOPLE_PL)
    adj = rng.choice(ADJ)
    return f"{cap_first(subj)} are {adj} about the {rng.choice(NOUNS_PL)}."


def gen_modal(rng):
    subj = rng.choice(["the " + w for w in PEOPLE_S] + NAMES + PEOPLE_PL)
    m = rng.choice(MODALS)
    v = rng.choice(["submit", "review", "confirm", "deliver", "attend", "complete",
                    "verify", "check", "update", "circulate", "print", "collect",
                    "photocopy", "forward", "approve", "sign off", "look into"])
    o = "the " + rng.choice(NOUNS_SG + NOUNS_PL)
    verb = v if subj in PEOPLE_PL else v  # base form after modal for all persons
    return f"{cap_first(subj)} {m} {verb} {o} before Friday."


def gen_question_aux(rng):
    wh = rng.choice(WH)
    aux = rng.choice(["are", "is", "do", "does", "did", "can", "will", "should"])
    if aux == "are":
        return f"{wh} are they going after the {rng.choice(['meeting','class','tour','service','shift','lecture'])}?"
    if aux == "is":
        return f"{wh} is she taking the {rng.choice(NOUNS_SG)}?"
    if aux in ("do", "did"):
        return f"{wh} do they collect the {rng.choice(NOUNS_PL)}?"
    if aux == "does":
        return f"{wh} does the manager sign the {rng.choice(NOUNS_PL)}?"
    if aux == "can":
        return f"{wh} can we find the {rng.choice(NOUNS_SG)}?"
    if aux == "will":
        return f"{wh} will the courier deliver the {rng.choice(NOUNS_PL)}?"
    return f"{wh} should we book the {rng.choice(PLACES)}?"


def gen_conj_clause(rng):
    c = rng.choice(CONJ)
    subj = rng.choice(["the " + w for w in PEOPLE_S] + NAMES + PEOPLE_PL)
    v1 = rng.choice(VERB_PL if subj in PEOPLE_PL else VERB_SG)
    o1 = "the " + rng.choice(NOUNS_SG)
    v2 = rng.choice(PAST_VERBS)
    o2 = "the " + rng.choice(NOUNS_PL)
    if c == "so":
        return f"The {rng.choice(PEOPLE_S)} was {rng.choice(ADJ)}, so {subj} {v2} {o2}."
    if c == "because":
        return f"{cap_first(subj)} {v1} {o1} because the {rng.choice(PEOPLE_S)} asked."
    if c == "although":
        return f"Although the {rng.choice(PEOPLE_S)} was {rng.choice(ADJ)}, {subj} {v2} {o2}."
    if c == "while":
        return f"While the {rng.choice(PEOPLE_S)} rested, {subj} {v2} {o2}."
    if c == "when":
        return f"When the bell rang, {subj} {v2} {o2}."
    if c == "since":
        return f"Since the morning was {rng.choice(ADJ)}, {subj} {v2} {o2}."
    if c == "after":
        return f"After the {rng.choice(NOUNS_SG)} arrived, {subj} {v1} {o1}."
    if c == "before":
        return f"Before the {rng.choice(NOUNS_PL)} were checked, {subj} {v2} {o2}."
    return f"{cap_first(subj)} waited until the {rng.choice(PEOPLE_S)} returned."


def gen_tech_stmt(rng):
    subj = cap_first("the " + rng.choice(["plugin", "driver", "script", "service",
                                          "server", "library", "cluster", "parser",
                                          "compiler", "router", "database", "scheduler",
                                          "middleware", "gateway", "cache", "queue",
                                          "worker", "agent", "daemon", "proxy"]))
    v = rng.choice(["returns", "rejects", "validates", "logs", "processes", "caches",
                    "indexes", "compiles", "uploads", "exports", "installs", "checks",
                    "verifies", "monitors", "handles", "routes", "merges", "reports"])
    obj = rng.choice(["the request", "each entry", "the payload", "the response",
                      "every token", "the config", "the cache", "the queue",
                      "the session", "the schema", "the token", "the header"])
    tail = rng.choice(["on every call.", "after each test.", "before the timeout.",
                       "during startup.", "by default.", "without any delay.",
                       "whenever needed.", "until shutdown."])
    return f"{subj} {v} {obj} {tail}"


def gen_tech_plural(rng):
    subj = cap_first(rng.choice(["the users", "the clients", "the nodes", "the tests",
                                 "the logs", "the workers", "the requests", "the jobs",
                                 "the tasks", "the agents", "the parsers", "the shards"]))
    v = rng.choice(["return", "reject", "validate", "log", "process", "cache",
                    "index", "compile", "upload", "export", "install", "check"])
    obj = rng.choice(["the request", "each entry", "the payload", "the response",
                      "every token", "the config", "the cache", "the queue",
                      "the session"])
    return f"{subj} {v} {obj} on every call."


def gen_negation(rng):
    subj = rng.choice(["the " + w for w in PEOPLE_S] + NAMES + PEOPLE_PL)
    v = rng.choice(VERB_PL if subj in PEOPLE_PL else VERB_SG)
    o = "the " + rng.choice(NOUNS_SG + NOUNS_PL)
    neg = rng.choice(NEGADV)
    if neg == "never":
        return f"{cap_first(subj)} never {v} {o} on Mondays."
    return f"{cap_first(subj)} {neg} {v} {o} in the morning."


def gen_adv(rng):
    subj = rng.choice(["the " + w for w in PEOPLE_S] + NAMES + PEOPLE_PL)
    v = rng.choice(VERB_PL if subj in PEOPLE_PL else VERB_SG)
    o = "the " + rng.choice(NOUNS_SG + NOUNS_PL)
    adv = rng.choice(ADV)
    return f"{cap_first(subj)} {v} {o} {adv}."


def gen_there_be(rng):
    if rng.random() < 0.5:
        n = rng.choice(NOUNS_SG)
        return f"There is a {n} in the {rng.choice(PLACES)}."
    n = rng.choice(NOUNS_PL)
    return f"There are {rng.choice(['two','three','four','five','six','seven','eight','some','many'])} {n} in the {rng.choice(PLACES)}."


def gen_relative(rng):
    head = "the " + rng.choice(PEOPLE_S)
    v1 = rng.choice(VERB_SG)
    o = "the " + rng.choice(NOUNS_SG)
    v2 = rng.choice(PAST_VERBS)
    return f"{cap_first(head)} who {v1} {o} also {v2} the {rng.choice(NOUNS_PL)}."


def gen_notes_future(rng):
    subj = rng.choice(["my aunt", "my uncle", "the plumber", "the builder",
                      "the electrician", "my cousin", "the nurse", "the doctor",
                      "the farmer", "the driver", "the dentist", "the vet"])
    act = rng.choice(["will visit", "will call", "will arrive", "will inspect",
                      "will fix", "will check", "will measure", "will collect"])
    t = rng.choice(["tomorrow", "next week", "on Monday", "in the morning",
                    "on the weekend", "before lunch", "after school", "in the evening"])
    return f"{cap_first(subj)} {act} the {rng.choice(['kitchen','garage','section','roof','garden','site','shed','driveway'])} {t}."


def gen_count(rng):
    num = rng.choice(["two", "three", "four", "five", "six", "seven", "eight",
                      "nine", "ten", "several", "many"])
    thing = rng.choice(NOUNS_PL)
    place = rng.choice(PLACES)
    verb = rng.choice(PAST_VERBS)
    return f"They {verb} {num} {thing} at the {place} this morning."


def gen_everyday_freq(rng):
    subj = rng.choice(["the " + w for w in PEOPLE_S] + NAMES + PEOPLE_PL)
    act = rng.choice(["goes swimming", "goes running", "goes shopping",
                      "go for a walk", "goes tramping", "goes fishing",
                      "goes cycling", "goes dancing", "practises the piano",
                      "waters the garden", "reads the news"])
    if subj in PEOPLE_PL and act.startswith("goes"):
        act = act.replace("goes", "go")
    if subj in PEOPLE_PL and act.startswith("practises"):
        act = act.replace("practises", "practise")
    if subj in PEOPLE_PL and act.startswith("waters"):
        act = act.replace("waters", "water")
    if subj in PEOPLE_PL and act.startswith("reads"):
        act = act.replace("reads", "read")
    return f"{cap_first(subj)} {act} every day."


GENS2 = [
    (gen_simple, 1.4, "essay"), (gen_plural_subj, 1.2, "essay"),
    (gen_past, 1.4, "essay"), (gen_have_perfect, 1.2, "essay"),
    (gen_be_adj, 1.0, "essay"), (gen_modal, 1.0, "essay"),
    (gen_question_aux, 0.8, "essay"), (gen_conj_clause, 1.4, "essay"),
    (gen_tech_stmt, 1.2, "tech"), (gen_tech_plural, 0.8, "tech"),
    (gen_negation, 0.7, "essay"), (gen_adv, 1.0, "essay"),
    (gen_there_be, 0.9, "essay"), (gen_relative, 0.6, "essay"),
    (gen_notes_future, 1.0, "notes"), (gen_count, 0.8, "notes"),
    (gen_everyday_freq, 0.5, "notes"),
]


def generate(n, seed=0):
    rng = random.Random(seed)
    out, seen = [], set()
    while len(out) < n:
        f = rng.choices([x[0] for x in GENS2], weights=[x[1] for x in GENS2], k=1)[0]
        s = f(rng)
        if s in seen:
            continue
        seen.add(s)
        out.append(s)
    return out


if __name__ == "__main__":
    for s in generate(12, seed=3):
        print(" -", s)
    big = generate(50000, seed=4)
    print("unique:", len(set(big)))
    vocab = set()
    for s in big:
        vocab.update(w.lower() for w in s.replace(".", "").split())
    print("distinct words:", len(vocab))

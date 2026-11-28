"""Lexicons for corpus generation. All correct by construction.
Protected tokens are NEVER corrupted and appear frequently so the model
learns to leave them alone (precision on protected classes)."""

PROTECTED = {
    # names (never corrupt, never invented)
    "wiremu", "aroha", "tane", "manaia", "hone", "kepa", "xiaoming", "xiaoyun",
    "priya", "arjun", "sanjay", "aoife", "seamus", "o'connell", "o'connors",
    "mcgregor", "macdonald", "nguyen", "thi", "ha", "eleven", "kauri", "rita",
    "amelia", "charlotte", "oliver", "henrietta", "william", "margaret",
    "hemi", "ana", "tui", "rawiri", "mereana", "atama", "jesse", "kavita",
    "rohan", "deepa", "mei", "chen", "wei", "li", "hao", "yuki", "sora",
    "takashi", "ana", "lucas", "mateo", "santiago", "ines", "sofia", "leon",
    "nz", "uk", "us", "eu", "otago", "canterbury", "waikato", "auckland",
    "wellington", "christchurch", "dunedin", "hamilton", "queenstown",
    "rotorua", "taupo", "gisborne", "napier", "nelson", "timaru", "whanganui",
    "invercargill", "palmerston", "northland", "tasman", "marlborough",
    "london", "manchester", "yorkshire", "belfast", "glasgow", "cardiff",
    "aotea", "hokitika", "masterton", "levin", "te", "kapiti", "whangarei",
}

TECH_TERMS = {
    "javascript", "typescript", "node.js", "python", "postgresql", "mysql",
    "kubernetes", "docker", "nginx", "redis", "graphql", "oauth", "jwt",
    "json", "yaml", "html", "css", "api", "http", "https", "tcp", "udp",
    "git", "github", "gitlab", "ci/cd", "linux", "unix", "bash", "regex",
    "ssl", "tls", "dns", "cdn", "s3", "lambda", "ec2", "pubsub", "grpc",
    "protobuf", "sqlite", "mongodb", "elasticsearch", "kafka", "rabbitmq",
    "rabbitmq", "vue", "react", "angular", "webpack", "vite", "eslint",
    "jest", "vitest", "pytest", "cargo", "rust", "golang", "swift", "kotlin",
    "java", "scala", "clojure", "haskell", "erlang", "elixir", "php", "perl",
    "ruby", "rails", "django", "flask", "spring", "hibernate", "maven",
    "gradle", "terraform", "ansible", "puppet", "chef", "vagrant", "helm",
    "prometheus", "grafana", "datadog", "sentry", "pagerduty", "confluence",
    "jira", "slack", "zoom", "teams", "dropbox", "figma", "sketch",
}

# Verbs for templates. (base, 3sg, past, ing, pastpart)
VERBS = {
    "walk":  ("walks",  "walked",  "walking"),
    "watch": ("watches", "watched", "watching"),
    "finish": ("finishes", "finished", "finishing"),
    "study":  ("studies", "studied", "studying"),
    "carry":  ("carries", "carried", "carrying"),
    "copy":   ("copies", "copied", "copying"),
    "reply":  ("replies", "replied", "replying"),
    "try":    ("tries",  "tried",  "trying"),
    "fix":     ("fixes",  "fixed",  "fixing"),
    "mix":     ("mixes",  "mixed",  "mixing"),
    "wash":   ("washes", "washed", "washing"),
    "brush":  ("brushes", "brushed", "brushing"),
    "push":   ("pushes", "pushed", "pushing"),
    "catch":  ("catches", "caught", "catching"),
    "teach":  ("teaches", "taught", "teaching"),
    "reach":  ("reaches", "reached", "reaching"),
    "touch":  ("touches", "touched", "touching"),
    "watch":  ("watches", "watched", "watching"),
    "fetch":  ("fetches", "fetched", "fetching"),
    "finish": ("finishes", "finished", "finishing"),
    "enjoy":  ("enjoys", "enjoyed", "enjoying"),
    "avoid":  ("avoids", "avoided", "avoiding"),
    "keep":   ("keeps",  "kept",   "keeping"),
    "sleep":  ("sleeps", "slept",  "sleeping"),
    "feel":   ("feels",  "felt",   "feeling"),
    "find":   ("finds",  "found",  "finding"),
    "leave":  ("leaves", "left",   "leaving"),
    "make":   ("makes",  "made",   "making"),
    "take":   ("takes",  "took",   "taking"),
    "write":  ("writes", "wrote",  "writing"),
    "drive":  ("drives", "drove",  "driving"),
    "choose": ("chooses", "chose", "choosing"),
    "break":  ("breaks", "broke",  "breaking"),
    "speak":  ("speaks", "spoke",  "speaking"),
    "drink":  ("drinks", "drank",  "drinking"),
    "swim":   ("swims",  "swam",   "swimming"),
    "sing":   ("sings",  "sang",   "singing"),
    "ring":   ("rings",  "rang",   "ringing"),
    "begin":  ("begins", "began",  "beginning"),
    "eat":    ("eats",   "ate",    "eating"),
    "run":    ("runs",   "ran",    "running"),
    "come":   ("comes",  "came",   "coming"),
    "give":   ("gives",  "gave",   "giving"),
    "go":     ("goes",   "went",   "going"),
    "see":    ("sees",   "saw",    "seeing"),
    "do":     ("does",   "did",    "doing"),
    "have":   ("has",    "had",    "having"),
    "read":   ("reads",  "read",   "reading"),
    "play":   ("plays",  "played", "playing"),
    "open":   ("opens",  "opened", "opening"),
    "close":  ("closes", "closed", "closing"),
    "clean":  ("cleans", "cleaned", "cleaning"),
    "start":  ("starts", "started", "starting"),
    "stop":   ("stops",  "stopped", "stopping"),
    "help":   ("helps",  "helped", "helping"),
    "call":   ("calls",  "called", "calling"),
    "ask":    ("asks",   "asked",  "asking"),
    "tell":   ("tells",  "told",   "telling"),
    "sell":   ("sells",  "sold",   "selling"),
    "win":    ("wins",   "won",    "winning"),
    "meet":   ("meets",  "met",    "meeting"),
    "send":   ("sends",  "sent",   "sending"),
    "build":  ("builds", "built", "building"),
    "spend":  ("spends", "spent", "spending"),
    "lend":   ("lends",  "lent",  "lending"),
    "send":   ("sends",  "sent",  "sending"),
    "bring":  ("brings", "brought", "bringing"),
    "think":  ("thinks", "thought", "thinking"),
    "buy":    ("buys",   "bought", "buying"),
    "fly":    ("flies",  "flew",  "flying"),
    "grow":   ("grows",  "grew",  "growing"),
    "know":   ("knows",  "knew",  "knowing"),
    "throw":  ("throws", "threw", "throwing"),
    "draw":   ("draws",  "drew",  "drawing"),
    "fall":   ("falls",  "fell",  "falling"),
    "hold":   ("holds",  "held",  "holding"),
    "hear":   ("hears",  "heard", "hearing"),
    "wear":   ("wears",  "wore",  "wearing"),
}

NOUNS = {
    "singular": ["book", "car", "house", "door", "window", "table", "chair",
                 "letter", "report", "essay", "project", "meeting", "letter",
                 "package", "picture", "song", "film", "game", "meal", "cake",
                 "river", "bridge", "road", "street", "room", "office",
                 "keyboard", "screen", "laptop", "phone", "bicycle", "guitar",
                 "garden", "tree", "flower", "forest", "mountain", "beach",
                 "market", "shop", "ticket", "story", "chapter", "lesson",
                 "class", "exam", "task", "job", "letter", "mirror", "shelf"],
    "plural":  ["books", "cars", "houses", "doors", "windows", "tables",
                 "chairs", "letters", "reports", "essays", "projects",
                 "meetings", "packages", "pictures", "songs", "films",
                 "games", "meals", "cakes", "rivers", "bridges", "roads",
                 "streets", "rooms", "offices", "keyboards", "screens",
                 "laptops", "phones", "bicycles", "guitars", "gardens",
                 "trees", "flowers", "forests", "mountains", "beaches",
                 "markets", "shops", "tickets", "stories", "chapters",
                 "lessons", "classes", "exams", "tasks", "jobs", "mirrors",
                 "shelves"],
    "uncount": ["water", "milk", "money", "advice", "information", "music",
                "traffic", "work", "homework", "research", "food", "bread",
                "rice", "furniture", "equipment", "software", "hardware",
                "luggage", "energy", "progress", "news", "weather", "fun",
                "knowledge", "experience", "furniture", "stationery"],
    "irr_pl": [("child", "children"), ("man", "men"), ("woman", "women"),
               ("person", "people"), ("foot", "feet"), ("tooth", "teeth"),
               ("mouse", "mice"), ("goose", "geese"), ("fish", "fish")],
}

ADJ = ["big", "small", "old", "young", "new", "long", "short", "bright",
       "quiet", "loud", "strong", "gentle", "happy", "cheerful", "modern",
       "ancient", "simple", "complex", "honest", "loyal", "brave", "calm",
       "careful", "clever", "creative", "diligent", "eager", "efficient",
       "famous", "generous", "gentle", "humble", "kind", "patient",
       "polite", "proud", "reliable", "serious", "talented", "tidy",
       "useful", "warm", "fluent", "quick", "eager", "early", "late"]
ADV = ["quickly", "slowly", "carefully", "loudly", "quietly", "happily",
       "easily", "early", "late", "hard", "well", "badly", "fluently",
       "clearly", "gently", "boldly", "patiently", "politely", "proudly",
       "safely", "slowly", "softly", "swiftly", "wisely", "brightly",
       "bravely", "calmly", "cheerfully", "eagerly", "faithfully"]

SUBJ_SING = ["he", "she", "it", "my brother", "my sister", "my cousin",
             "my friend", "our teacher", "our neighbour", "the student",
             "the engineer", "the manager", "the nurse", "the writer",
             "the driver", "the player", "the singer", "the visitor"]
SUBJ_PL = ["they", "we", "you", "my friends", "my parents", "the students",
           "the engineers", "the managers", "the nurses", "the writers",
           "the players", "the singers", "the visitors", "our teachers",
           "our neighbours", "the children", "the men", "the women"]

INTRO_PHRASE = [
    "after school", "before dinner", "during the holidays", "on Monday",
    "in the morning", "at the weekend", "after the meeting", "before lunch",
    "during the lecture", "after the exam", "in the afternoon", "on Friday",
]

TIME_PAST = ["yesterday", "last week", "last month", "last year", "in 2019",
             "two days ago", "three weeks ago", "last night", "last summer"]
TIME_FUT = ["tomorrow", "next week", "next month", "next year", "tonight",
            "later today", "in two days"]

PLACES = ["the library", "the park", "the museum", "the market",
          "the station", "the office", "the beach", "the bakery",
          "the gym", "the cinema", "the clinic", "the workshop",
          "the harbour", "the playground", "the warehouse", "the studio"]

# Common misspellings -> correct
MISSPELL = {
    "recieve": "receive", "seperate": "separate", "definately": "definitely",
    "occured": "occurred", "untill": "until", "wich": "which",
    "becuase": "because", "thier": "their", "freind": "friend",
    "beleive": "believe", "acheive": "achieve", "buisness": "business",
    "enviroment": "environment", "goverment": "government",
    "tommorow": "tomorrow", "neccessary": "necessary",
    "occassion": "occasion", "adress": "address",
    "accomodate": "accommodate", "embarass": "embarrass",
    "arguement": "argument", "calender": "calendar",
    "catagory": "category", "concious": "conscious",
    "existance": "existence", "foriegn": "foreign", "grammer": "grammar",
    "harrass": "harass", "irresistable": "irresistible",
    "maintenence": "maintenance", "noticable": "noticeable",
    "occurence": "occurrence", "playwrite": "playwright",
    "privelege": "privilege", "publically": "publicly",
    "questionaire": "questionnaire", "recomend": "recommend",
    "refered": "referred", "rythm": "rhythm", "succesful": "successful",
    "tounge": "tongue", "wierd": "weird", "collage": "college",
    "commited": "committed", "dissapoint": "disappoint",
    "gaurd": "guard", "liason": "liaison", "ommission": "omission",
    "perseverence": "perseverance", "persue": "pursue",
    "supress": "suppress", "visable": "visible", "accomplisht": "accomplished",
}

# Word-choice / confusable pairs: wrong -> correct
CONFUSABLES = {
    "their": "they're", "there": "they're", "they're": "their",
    "your": "you're", "you're": "your", "its": "it's", "it's": "its",
    "to": "too", "too": "to", "then": "than", "than": "then",
    "affect": "effect", "effect": "affect", "lose": "loose",
    "loose": "lose", "quite": "quiet", "quiet": "quite",
    "accept": "except", "except": "accept", "advice": "advise",
    "advise": "advice", "breath": "breathe", "breathe": "breath",
    "desert": "dessert", "dessert": "desert", "principal": "principle",
    "principle": "principal", "stationary": "stationery",
    "stationery": "stationary", "complement": "compliment",
    "compliment": "complement", "insure": "ensure", "ensure": "insure",
    "farther": "further", "further": "farther", "allusion": "illusion",
    "capital": "capitol", "cite": "site", "site": "cite",
    "personal": "personnel", "past": "passed", "role": "roll",
    "weather": "whether", "whether": "weather", "who's": "whose",
    "whose": "who's", "led": "lead", "lead": "led",
}

# context-sensitive: only corrupt when template places them in a slot
PREP_FIX = {
    "different than": "different from", "depends of": "depends on",
    "consists in": "consists of", "married with": "married to",
    "arrive to": "arrived at", "good in": "good at", "interested to":
    "interested in", "afraid from": "afraid of", "similar with":
    "similar to", "capable to": "capable of", "responsible of":
    "responsible for", "famous in": "famous for", "keen of": "keen on",
}

REDUNDANT = {
    "return back": "return", "reply back": "reply", "revert back": "revert",
    "discuss about": "discuss", "enter into": "enter",
    "comprises of": "comprises", "off of": "off", "ask to": "ask",
    "repeat again": "repeat", "equally as": "equally",
}

DOUBLE_NEG = {
    "didn't do nothing": "didn't do anything",
    "didn't see nothing": "didn't see anything",
    "didn't go nowhere": "didn't go anywhere",
    "don't know nothing": "don't know anything",
    "haven't told nobody": "haven't told anybody",
    "can't find nothing": "can't find anything",
    "never says nothing": "never says anything",
    "didn't buy nothing": "didn't buy anything",
    "didn't eat nothing": "didn't eat anything",
    "couldn't hear nothing": "couldn't hear anything",
    "wouldn't help nobody": "wouldn't help anybody",
    "won't tell nobody": "won't tell anybody",
    "don't need nothing": "don't need anything",
    "hasn't changed nothing": "hasn't changed anything",
}

CONTRACT_MISS = {
    "dont": "don't", "cant": "can't", "wont": "won't", "doesnt": "doesn't",
    "didnt": "didn't", "isnt": "isn't", "arent": "aren't", "wasnt": "wasn't",
    "werent": "weren't", "hasnt": "hasn't", "havent": "haven't",
    "hadnt": "hadn't", "couldnt": "couldn't", "shouldnt": "shouldn't",
    "wouldnt": "wouldn't", "im": "I'm", "ive": "I've", "id": "I'd",
    "theyre": "they're", "youre": "you're", "weve": "we've",
    "youve": "you've", "theres": "there's", "lets": "let's",
    "shes": "she's", "hes": "he's", "its": "it's", "was": "was",
}

PROPER_LOWER = {
    "monday": "Monday", "tuesday": "Tuesday", "wednesday": "Wednesday",
    "thursday": "Thursday", "friday": "Friday", "saturday": "Saturday",
    "sunday": "Sunday", "january": "January", "february": "February",
    "march": "March", "april": "April", "june": "June", "july": "July",
    "august": "August", "september": "September", "october": "October",
    "november": "November", "december": "December", "english": "English",
    "french": "French", "german": "German", "spanish": "Spanish",
    "japanese": "Japanese", "chinese": "Chinese", "maori": "Māori",
    "nz": "NZ", "uk": "UK", "auckland": "Auckland", "wellington":
    "Wellington", "christchurch": "Christchurch", "dunedin": "Dunedin",
    "hamilton": "Hamilton", "queenstown": "Queenstown", "rotorua":
    "Rotorua", "taupo": "Taupō", "london": "London", "paris": "Paris",
    "tokyo": "Tokyo", "beijing": "Beijing", "sydney": "Sydney",
    "melbourne": "Melbourne", "brisbane": "Brisbane", "perth": "Perth",
    "daniel": "Daniel", "jessica": "Jessica", "katherine": "Katherine",
}

VOCAB_WORDS = set()
for _vs in VERBS.values():
    VOCAB_WORDS.update([_vs[0].split()[0], _vs[1], _vs[2].rstrip("ing") + "e" if False else _vs[2]])
VOCAB_WORDS.update(NOUNS["singular"]); VOCAB_WORDS.update(NOUNS["plural"])
VOCAB_WORDS.update(NOUNS["uncount"]); VOCAB_WORDS.update(ADJ); VOCAB_WORDS.update(ADV)
VOCAB_WORDS.update(MISSPELL.values()); VOCAB_WORDS.update(CONFUSABLES.values())
VOCAB_WORDS.update(CONTRACT_MISS.values()); VOCAB_WORDS.update(PROPER_LOWER.values())
for _w in MISSPELL: VOCAB_WORDS.add(_w)
for _w in CONFUSABLES: VOCAB_WORDS.add(_w)
VOCAB_WORDS.update(["a", "an", "the", "is", "are", "was", "were", "am",
                    "have", "has", "had", "do", "does", "did", "go", "goes",
                    "went", "gone", "will", "would", "can", "could", "should",
                    "many", "much", "fewer", "less", "and", "but", "or",
                    "because", "although", "however", "therefore", "so",
                    "very", "really", "too", "quite", "better", "best",
                    "worse", "worst", "taller", "easiest", "anything",
                    "anybody", "anywhere", "nothing", "nobody", "nowhere",
                    "from", "on", "in", "at", "to", "of", "for", "with",
                    "about", "than", "into", "off", "under", "over",
                    "children", "men", "women", "feet", "teeth", "mice",
                    "geese", "people", "I", "my", "we", "our", "they",
                    "their", "them", "he", "she", "it", "you", "your",
                    "classmates", "teammates", "colleagues", "neighbours",
                    "sincerely", "regards", "however", "moreover", "besides",
                    "meanwhile", "furthermore", "instead", "already",
                    "always", "usually", "often", "sometimes", "never",
                    "probably", "perhaps", "certainly", "clearly", "quickly",
                    "writes", "reads", "walks", "runs", "eats", "drinks",
                    "more", "most", "as", "such", "these", "those", "this",
                    "that", "some", "any", "all", "both", "each", "every",
                    "either", "neither", "other", "another", "same",
                    "different", "similar", "interested", "keen", "afraid",
                    "good", "great", "nice", "fine", "busy", "free",
                    "morning", "afternoon", "evening", "night", "week",
                    "weekend", "month", "year", "today", "tomorrow",
                    "yesterday", "school", "home", "work", "town", "city",
                    "holiday", "holidays", "hobby", "sport", "music",
                    "letter", "email", "message", "note", "essay", "exam",
                    "test", "quiz", "practice", "training", "meeting",
                    "party", "wedding", "birthday", "present", "gift",
                    "trip", "flight", "train", "bus", "walk", "drive",
                    "lunch", "dinner", "breakfast", "supper", "snack"])

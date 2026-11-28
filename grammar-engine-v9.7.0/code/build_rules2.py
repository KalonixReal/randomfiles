# -*- coding: utf-8 -*-
"""Builds rules2.json: rules.json + precision-targeted new rules derived
from the corruption-generator inverse maps and the dev FN analysis (v2).

Engine capabilities required (engine.py + engine94.js):
  apply.kind = "template" | "g_ing" | "del_next" | "period_end"
  guard.prev_re = {re, window} (or plain string) -> must match before span
  guard.prev_not_re = {re, window} -> must NOT match before span
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

HERE = os.path.dirname(os.path.abspath(__file__))
base = json.load(open(os.path.join(HERE, "rules.json")))
rules = list(base["rules"])

# ---------------------------------------------------------------- lexicons
# singular nouns that take singular verbs; collectives EXCLUDED (UK plural use)
NOUN_SINGULAR = (
    "project|lab|laboratory|parcel|aunt|uncle|cousin|brother|sister|mother|father|"
    "parent|child|friend|neighbour|guest|host|manager|owner|captain|coach|judge|"
    "pilot|sailor|soldier|doctor|nurse|dentist|patient|customer|client|visitor|"
    "tourist|engineer|farmer|driver|writer|reader|teacher|student|servant|worker|"
    "officer|librarian|printer|scanner|camera|server|database|network|website|"
    "application|program|function|method|module|feature|release|version|update|"
    "upgrade|patch|ticket|case|issue|bug|error|fault|defect|flaw|wound|injury|"
    "illness|disease|fever|machine|engine|robot|drone|device|appliance|tool|"
    "instrument|clock|watch|screen|keyboard|building|bridge|road|street|wall|"
    "door|window|gate|fence|path|house|home|room|bedroom|kitchen|bathroom|garage|"
    "shed|garden|farm|orchard|paddock|field|park|forest|valley|mountain|hill|"
    "river|stream|creek|lake|island|beach|bay|harbour|port|dock|town|city|"
    "village|country|shop|store|office|factory|mill|foundry|mine|quarry|book|"
    "letter|report|article|chapter|page|question|problem|idea|plan|task|job|"
    "course|subject|topic|lesson|story|poem|essay|song|film|movie|picture|photo|"
    "painting|design|model|experiment|recipe|meal|dish|cup|glass|bottle|plate|"
    "bowl|lamp|candle|towel|bus|train|car|van|ute|truck|boat|ship|plane|ferry|"
    "kayak|canoe|bike|bicycle|meeting|party|concert|festival|game|match|race|"
    "competition|exhibition|seminar|workshop|session|lecture|test|exam|quiz|"
    "assignment|speech|talk|interview|discussion|debate|review|survey|vote|"
    "election|campaign|journey|trip|flight|adventure|walk|drive|ride|holiday|"
    "vacation|weekend|birthday|anniversary|celebration|wedding|funeral|speech|"
    "tradition|habit|routine|schedule|timetable|calendar|agenda|minute|note|"
    "record|file|folder|document|paper|receipt|invoice|statement|account|"
    "budget|forecast|copy|bill|invoice|sum|total|price|fee|rent|fine|penalty|"
    "reward|prize|award|medal|trophy|present|gift|donation|grant|scholarship|"
    "salary|wage|income|pension|allowance|bursary|stipend|honorarium|fee|cost|"
    "expense|outlay|deposit|loan|debt|mortgage|lease|treaty|contract|agreement|"
    "arrangement|deal|pact|bond|law|rule|regulation|policy|decision|choice|"
    "option|opinion|belief|thought|dream|memory|name|word|sentence|phrase|claim|"
    "promise|wish|hope|apology|excuse|reason|cause|effect|result|consequence|"
    "outcome|product|produce|crop|harvest|yield|growth|increase|decrease|"
    "reduction|improvement|development|advance|progress|process|method|"
    "surface|engine|chimney|fireplace|hearth|rug|mat|carpet|curtain|blind|"
    "shutter|awning|pergola|veranda|porch|balcony|deck|patio|terrace|lawn|"
    "hedge|shrub|bush|tree|sapling|seedling|plant|flower|rose|tulip|daffodil|"
    "fern|palm|pine|oak|elm|ash|birch|willow|maple|kauri|rimu|beech|couch|"
    "armchair|stool|bench|desk|table|wardrobe|cupboard|drawer|shelf|cabinet|"
    "chest|box|crate|basket|bag|sack|wallet|purse|backpack|suitcase|trunk|"
    "barrel|bucket|basin|sink|tap|spout|hose|pipe|drain|gutter|spouting|"
    "machine|oven|stove|microwave|dishwasher|vacuum|mop|broom|brush|comb|"
    "bus|cache|endpoint|function|service|module|library|repo|repository|"
    "pipeline|cluster|database|index|query|request|response|token|session|"
    "process|container|image|layer|protocol|route|router|switch|proxy|"
    "gateway|firewall|deploy|migration|backup|commit|crash|outage|"
    "incident|sprint|standup|backlog|milestone|grandad|foal|ewe|lamb|"
    "calf|cow|bull|pig|goat|kid|dog|cat|kitten|puppy|rooster|hen|duck|"
    "gander|turkey|peacock|bird|porch|balcony|deck|patio|terrace|lawn"
    "mirror|soap|shampoo|toothbrush|toothpaste|razor|blanket|quilt|duvet|"
    "pillow|cushion|mattress|torch|heater|boiler|fridge|freezer|cooktop"
)
NOUN_SINGULAR += "|principal|warehouse|mare|stallion|pony|filly|vet|truck|ute"

PLURAL_FORM_SINGULAR_GUARD = [
    "sheep", "deer", "fish", "series", "species", "means", "offspring", "aircraft",
    "hovercraft", "watercraft", "spacecraft", "salmon", "trout", "cod", "reindeer",
    "bison", "moose", "swine", "police", "headquarters", "economics", "physics",
    "mathematics", "politics", "statistics", "gymnastics", "news", "billiards", "darts",
    "measles", "mumps", "rabies", "diabetes", "tennis", "chess", "molasses",
    "billiards", "genetics", "logistics", "obstetrics", "pediatrics",
    "psychiatrics", "tactics", "aerodynamics", "alms",
    "clothes", "glasses", "jeans", "trousers", "pyjamas", "scissors",
    "pliers", "tongs", "tweezers", "binoculars", "spectacles", "shorts",
    "belongings", "congratulations", "earnings", "outskirts", "surroundings",
    "thanks", "wages", "contents", "remains", "savings", "valuables",
    "breadcrumbs", "noodles", "spaghetti", "staples", "stationery",
    "idols", "croissant", "chassis", "analysis", "diagnosis",
    "oasis", "synopsis", "thesis", "crisis", "basis", "ellipsis", "axes",
    "tvs", "pcs", "gps", "ids", "urls", "ios", "sms", "etc", "tv",
    "tues", "thurs", "novs", "admins", "boss", "bus", "gas", "this",
    "miss", "less", "press", "cross", "toss", "loss", "moss", "fuss",
    "plus", "us", "thus", "status", "focus", "bonus", "campus", "virus",
    "radius", "genius", "fungus", "census", "sinus", "esophagus",
    "apparatus", "walrus", "crocus", "ibis", "iris", "lotus", "cactus",
    "octopus", "platypus", "succus", "stylus", "trellis", "wisteria",
    "staff", "team", "committee", "council", "class", "club", "choir", "band",
    "orchestra", "panel", "board", "crew", "crowd", "audience", "public",
    "firm", "branch", "family", "group", "company", "government",
]

PLURAL_NOUNS_FOR_A = (
    "apples|oranges|books|letters|files|notes|reports|items|things|words|pages|questions|"
    "answers|examples|photos|pictures|tickets|forms|pens|pencils|shoes|socks|glasses|coins|"
    "keys|toys|boxes|bags|chips|biscuits|crates|documents|tools|parts|wires|cables|plugs|"
    "screws|bolts|nails|planks|boards|bricks|tiles|plants|seeds|trees|flowers|roses|herbs|"
    "potatoes|tomatoes|carrots|beans|peas|grapes|berries|bananas|sandwiches|cakes|slices|"
    "meals|drinks|cups|bottles|plates|dishes|knives|forks|spoons|chairs|tables|lamps|"
    "batteries|chargers|screens|keyboards|monitors|laptops|tablets|shirts|jackets|coats|"
    "hats|gloves|scarves|towels|sheets|pillows|curtains|carpets|rugs|mats|cushions|shelves|"
    "drawers|mirrors|frames|albums|folders|envelopes|stamps|cards|postcards|parcels|"
    "packages|packets|cans|jars|tins|sacks|bundles|piles|stacks|bunches|pairs|sets|kits"
)

ADJ_TO_ADV = {
    "quick": "quickly", "careful": "carefully", "immediate": "immediately",
    "significant": "significantly", "beautiful": "beautifully", "bad": "badly",
    "rapid": "rapidly", "sharp": "sharply", "efficient": "efficiently",
    "successful": "successfully", "quiet": "quietly", "easy": "easily",
    "terrible": "terribly", "horrible": "horribly", "patient": "patiently",
    "calm": "calmly", "eager": "eagerly", "gentle": "gently", "simple": "simply",
    "brave": "bravely", "honest": "honestly", "hopeful": "hopefully",
    "cheerful": "cheerfully", "wonderful": "wonderfully", "delightful": "delightfully",
    "grateful": "gratefully", "formal": "formally", "perfect": "perfectly",
    "professional": "professionally", "excellent": "excellently",
    "dramatic": "dramatically", "automatic": "automatically",
    "enthusiastic": "enthusiastically", "basic": "basically",
    "economic": "economically", "scientific": "scientifically",
    "specific": "specifically", "whole": "wholly", "true": "truly",
}
ADV_VERBS = (
    "grew|responded|behaved|sang|drove|need|arrived|finished|performed|worked|played|"
    "slept|spoke|wrote|ran|left|moved|danced|smiled|laughed|cried|shouted|whispered|"
    "listened|waited|travelled|walked|talked|ate|rose|fell|climbed|jumped|swam|trained|"
    "studied|learned|taught|practised|explained|asked|answered|returned|sent|built|made|"
    "took|gave|went|came|got|did|said|saw|won|lost|felt|kept|held|met|brought|bought|"
    "caught|found|thought|spent|began|broke|chose|forgot|knew|swam|led|sold|told|"
    "understood|performed|behaved|responded|sang|drove|went|finished|need|leave"
)

PAST_TO_PP = {
    "wrote": "written", "saw": "seen", "ate": "eaten", "took": "taken",
    "gave": "given", "ran": "run", "came": "come", "knew": "known",
    "drove": "driven", "grew": "grown", "began": "begun", "chose": "chosen",
    "broke": "broken", "forgot": "forgotten", "spoke": "spoken", "swam": "swum",
    "sang": "sung", "went": "gone",
}

OVERREG = {
    "goed": "went", "runned": "ran", "buyed": "bought", "bringed": "brought",
    "teached": "taught", "catched": "caught", "sended": "sent", "builded": "built",
    "feeled": "felt", "sleeped": "slept", "eated": "ate", "taked": "took",
    "gaved": "gave", "maked": "made", "camed": "came", "goted": "got",
    "runed": "ran", "writed": "wrote", "speaked": "spoke", "swimmed": "swam",
    "winned": "won", "losed": "lost", "thinked": "thought",
}

REG_VERBS = (
    "return|complete|confirm|deliver|install|attend|start|finish|check|review|"
    "update|upgrade|test|request|report|email|copy|apply|reply|try|carry|study|"
    "plan|stop|drop|ship|book|cancel|collect|connect|create|delete|download|"
    "upload|export|import|insert|print|save|search|select|share|sign|submit|"
    "transfer|travel|watch|work|call|ask|answer|clean|cook|count|cover|cross|"
    "fix|follow|help|join|learn|look|love|move|need|open|order|pass|place|play|"
    "practise|prepare|push|reach|receive|remember|remove|repeat|replace|reply|"
    "require|reserve|rest|return|show|stay|step|support|switch|talk|thank|"
    "train|turn|use|visit|wait|walk|want|wash|water|weigh|wish|wonder|worry|"
    "bother|deliver|consider|explain|gather|listen|offer|point|present|process|"
    "prompt|register|render|respond|trigger|suffer|summon|wander|warm|whisper|"
    "wither|monitor|notify|inform|delay|approve|reject|accept|distribute|"
    "announce|record|track|alert|remind|contact|supply|adopt|schedule|compile|"
    "document|research|target|trace|audit|analyse|analyze|edit|deploy|migrate|"
    "maintain|develop|manage|coordinate|organise|organize|arrange|evaluate|"
    "inspect|investigate|attach|notify|accept|reject|approve|publish|launch|"
    "release|introduce|implement|enforce|repair|replace|store|transfer|welcome|"
    "invite|send|adjust|admit|commit|conduct|consult|consume|contain|convert|"
    "convince|correct|describe|detect|direct|discuss|display|distinguish|"
    "divert|divide|double|draft|emit|enable|enclose|encounter|engage|enhance|"
    "ensure|enter|equip|estimate|examine|exclude|execute|expand|expect|"
    "experience|explore|express|extend|extract|favour|fear|feature|fill|filter|"
    "find|fine|fit|flag|flood|force|form|foster|frame|gain|generate|grant|"
    "greet|group|handle|highlight|host|hurry|identify|illustrate|improve|"
    "include|increase|index|instruct|intend|interest|involve|issue|itemise|"
    "itemize|justify|label|lack|launch|lead|limit|link|list|load|locate|lock|"
    "maintain|mark|market|maximise|maximize|minimise|minimize|model|modify|"
    "mount|name|note|notice|observe|obtain|omit|operate|outline|overcome|"
    "package|paint|pair|partition|paste|pause|permit|poll|port|position|"
    "postpone|praise|predict|prefer|preserve|prescribe|prioritise|prioritize|"
    "produce|program|progress|project|promote|prompt|pronounce|propose|"
    "protect|provide|purchase|pursue|quote|raise|rank|rate|recall|recognise|"
    "recognize|recruit|reduce|refer|reflect|refresh|refuse|regard|relate|"
    "relax|rely|remark|rename|render|rent|rescue|resist|resolve|restore|"
    "restrict|retain|revise|reward|ring|roll|rotate|round|rule|satisfy|"
    "save|scan|scold|score|secure|sell|separate|serve|settle|shade|shape|"
    "shift|ship|shorten|show|signal|simplify|sort|source|spare|specify|"
    "sponsor|spot|spread|stack|staff|stage|stamp|standardise|standardize|"
    "state|stimulate|strengthen|stress|stretch|strike|structure|strengthen|"
    "swap|tailor|target|telephone|thank|thicken|trace|trade|transcribe|"
    "transform|translate|transmit|transport|treat|trust|undertake|update|"
    "upgrade|upload|urge|validate|verify|view|visit|voice|warrant|waste|"
    "welcome|widen|wrap"
).split("|")
REG_PAST_TO_BASE = {}
for v in set(REG_VERBS):
    v = v.strip()
    if not v:
        continue
    if v.endswith("e"):
        p = v + "d"
    elif v.endswith("y") and v[-2] not in "aeiou":
        p = v[:-1] + "ied"
    elif v in ("stop", "drop", "ship", "plan", "commit", "refer", "permit",
               "submit", "admit", "omit", "plot", "spot", "flag", "drag", "jog",
               "pin", "bin", "tan", "hum", "sum", "regret", "travel"):
        p = v + v[-1] + "ed"
    else:
        p = v + "ed"
    REG_PAST_TO_BASE[p] = v

REG_BASE_TO_PAST = {b: p for p, b in REG_PAST_TO_BASE.items()}

# irregular past participles: never let the regular suffix machinery emit
# non-words like "sended" / "receiveed" (be/have + base verb contexts)
REG_BASE_TO_PAST.update({
    "send": "sent", "build": "built", "keep": "kept", "sleep": "slept",
    "feel": "felt", "leave": "left", "meet": "met", "pay": "paid",
    "say": "said", "win": "won", "find": "found", "hold": "held",
    "sell": "sold", "tell": "told", "bring": "brought", "buy": "bought",
    "think": "thought", "teach": "taught", "catch": "caught",
    "go": "gone", "see": "seen", "eat": "eaten", "take": "taken",
    "write": "written", "speak": "spoken", "break": "broken",
    "drive": "driven", "fly": "flown", "know": "known", "grow": "grown",
    "throw": "thrown", "choose": "chosen", "forget": "forgotten",
    "begin": "begun", "drink": "drunk", "swim": "swum", "sing": "sung",
    "give": "given", "get": "got", "make": "made", "feed": "fed",
    "lead": "led", "spend": "spent", "lend": "lent", "stand": "stood",
    "understand": "understood",
})

MISPELL = {
    "recieved": "received", "accomodation": "accommodation", "embarassed": "embarrassed",
    "tomatos": "tomatoes", "adress": "address", "definately": "definitely",
    "seperate": "separate", "occured": "occurred", "untill": "until",
    "begining": "beginning", "writting": "writing", "beleive": "believe",
    "calender": "calendar", "collegue": "colleague", "comming": "coming",
    "commited": "committed", "concious": "conscious", "curiousity": "curiosity",
    "decison": "decision", "dependant": "dependent", "desicion": "decision",
    "effeciency": "efficiency", "embarasment": "embarrassment",
    "enviroment": "environment", "excellant": "excellent", "familar": "familiar",
    "finaly": "finally", "foriegn": "foreign", "fourty": "forty", "freind": "friend",
    "garantee": "guarantee", "goverment": "government", "gaurd": "guard",
    "harrassment": "harassment", "heirarchy": "hierarchy", "immediatly": "immediately",
    "incidently": "incidentally", "independant": "independent", "intrest": "interest",
    "knowlege": "knowledge", "libary": "library", "liason": "liaison",
    "maintenence": "maintenance", "managment": "management", "millenium": "millennium",
    "neccessary": "necessary", "necesary": "necessary", "noticable": "noticeable",
    "occassion": "occasion", "pavillion": "pavilion", "persistant": "persistent",
    "posession": "possession", "potatoe": "potato", "prefered": "preferred",
    "publically": "publicly", "questionaire": "questionnaire", "recomend": "recommend",
    "refered": "referred", "relevent": "relevant", "responsable": "responsible",
    "rythm": "rhythm", "schedual": "schedule", "succesful": "successful",
    "successfull": "successful", "supress": "suppress", "suprise": "surprise",
    "tendancy": "tendency", "threshhold": "threshold", "tommorow": "tomorrow",
    "tounge": "tongue", "truely": "truly", "usualy": "usually", "vaccuum": "vacuum",
    "wich": "which", "wierd": "weird", "writen": "written", "buisness": "business",
    "carefull": "careful", "choosen": "chosen", "disapoint": "disappoint",
    "experiance": "experience", "explaination": "explanation", "florish": "flourish",
    "greatful": "grateful", "hieght": "height", "hygenic": "hygienic",
    "intergrate": "integrate", "labatory": "laboratory", "lengeth": "length",
    "listn": "listen", "maintainance": "maintenance", "marrige": "marriage",
    "mischevious": "mischievous", "mispell": "misspell", "occurance": "occurrence",
    "ocurred": "occurred", "oppurtunity": "opportunity", "perseverence": "perseverance",
    "personel": "personnel", "playwrite": "playwright", "posible": "possible",
    "practicaly": "practically", "prehaps": "perhaps", "propoganda": "propaganda",
    "recomendation": "recommendation", "reguardless": "regardless",
    "religous": "religious", "remeber": "remember", "resturant": "restaurant",
    "ridculous": "ridiculous", "saftey": "safety", "secound": "second",
    "sincerly": "sincerely", "speach": "speech", "strenght": "strength",
    "suggesstion": "suggestion", "superceeded": "superseded", "tranport": "transport",
    "unfortunatly": "unfortunately", "unusal": "unusual", "upgarde": "upgrade",
    "usally": "usually", "vegatarian": "vegetarian", "yeild": "yield", "teh": "the",
    "tehre": "there", "thier": "their", "waht": "what", "whcih": "which",
    "whitch": "which", "wiht": "with", "wnat": "want", "woudl": "would",
    "yuo": "you", "aer": "are", "agian": "again", "awya": "away",
    "becuase": "because", "becasue": "because", "betwen": "between",
    "comeing": "coming", "contraversy": "controversy", "develope": "develop",
    "diffrent": "different", "dilemna": "dilemma", "disatisfied": "dissatisfied",
    "egar": "eager", "embarassing": "embarrassing", "excead": "exceed",
    "excercise": "exercise", "fufill": "fulfill", "graet": "great",
    "happend": "happened", "harrass": "harass", "hardley": "hardly",
    "heros": "heroes", "hopefuly": "hopefully", "idae": "idea",
    "immediatley": "immediately", "irregardless": "regardless", "jist": "gist",
    "knowladge": "knowledge", "lenght": "length", "likly": "likely",
    "morgage": "mortgage", "natrual": "natural", "neccessarily": "necessarily",
    "occassionally": "occasionally", "paralel": "parallel", "peice": "piece",
    "posibly": "possibly", "potencial": "potential", "prety": "pretty",
    "probaly": "probably", "promiss": "promise", "punshment": "punishment",
    "reccommend": "recommend", "recieve": "receive", "referal": "referral",
    "repitition": "repetition", "reqire": "require", "resovle": "resolve",
    "responsability": "responsibility", "restaraunt": "restaurant",
    "revieve": "review", "sandwhich": "sandwich", "scedule": "schedule",
    "sincerley": "sincerely", "strenghten": "strengthen", "strongely": "strongly",
    "sucess": "success", "sucession": "succession", "suposed": "supposed",
    "suprised": "surprised", "theif": "thief", "througout": "throughout",
    "tital": "title", "togeather": "together", "towrad": "toward",
    "tyring": "trying", "unathorized": "unauthorized", "undoubtably": "undoubtedly",
    "useing": "using", "verfy": "verify", "vertually": "virtually",
    "visable": "visible", "writor": "writer", "whith": "with", "yatch": "yacht",
    "youself": "yourself", "summery": "summary",
}
import engine as _E
NZ_STOP = _E.NZ_SUPPRESS_SET | _E.MAORI_DET
MISPELL = {k: v for k, v in MISPELL.items()
           if k.lower() not in NZ_STOP and v.lower() not in NZ_STOP}
# v9.7.0 recall additions: measured X2 misses
MISPELL.update({
    "occurence": "occurrence", "ocurrence": "occurrence", "ocurrance": "occurrence",
    "absolutly": "absolutely", "occured": "occurred", "untill": "until",
    "wich": "which", "alot": "a lot", "aswell": "as well", "eachother": "each other",
    "noone": "no one", "inspite": "in spite", "incase": "in case",
    "infact": "in fact", "ofcourse": "of course", "alright": "all right",
})

def R(id, re_, apply, type_, case="i", guard=None):
    r = {"id": id, "re": re_, "case": case, "apply": apply, "type": type_}
    if guard:
        r["guard"] = guard
    return r

MODALS_CATENATIVE = ["should", "would", "could", "can", "will", "may", "might",
                     "must", "shall", "do", "does", "did", "let", "make", "watch",
                     "see", "hear", "help", "feel", "hear", "leave", "keep"]
PREV_NOT_PREPS = ["about", "of", "with", "for", "from", "in", "on", "at", "by",
                   "to", "near", "under", "over", "without", "within", "into",
                   "onto", "upon", "during", "between", "among", "across",
                   "against", "along", "behind", "beyond", "despite", "except",
                   "inside", "outside", "past", "through", "throughout",
                   "toward", "towards", "until", "up", "down", "off", "aboard",
                   "beneath", "beside", "number", "variety", "total", "range",
                   "majority", "minority", "couple", "pair", "series", "handful",
                   "load", "lot", "percentage", "proportion", "fraction", "part",
                   "portion", "section", "box", "crate", "group", "bunch",
                   "cluster", "batch", "sum", "spate", "string", "run",
                   "and", "or", "nor", "s"]

# words that look plural ([a-z]{3,}s) but are adverbs / singular nouns and must
# never be treated as plural subjects
FAKE_PLURAL_ADVERBS = [
    "sometimes", "always", "perhaps", "nowadays", "anyways", "besides",
    "upwards", "backwards", "forwards", "afterwards", "outwards", "inwards",
    "homewards", "crossroads", "maths", "chassis", "alias", "canvas",
    "atlas", "summons", "chorus",
    # singular -ics / -is academic nouns
    "linguistics", "athletics", "phonetics", "semantics", "optics",
    "informatics", "graphics", "gymnastics", "politics", "economics",
    "hypothesis", "emphasis", "parenthesis", "synthesis", "antithesis",
    "symbiosis", "photosynthesis", "mitosis", "meiosis", "necrosis",
    "thrombosis", "sclerosis", "prognosis", "neurosis", "psychosis",
    "osmosis", "genesis",
]

new_rules = []
new_rules.append(R(
    "sva_noun_sing", r"\b(" + NOUN_SINGULAR + r") (have|are|do|were|don't|dont|aren't|arent|haven't|havent|weren't|werent)\b",
    {"kind": "map", "group": 2, "map": {
        "have": "has", "are": "is", "do": "does", "were": "was",
        "don't": "doesn't", "dont": "doesn't", "aren't": "isn't", "arent": "isn't",
        "haven't": "hasn't", "havent": "hasn't", "weren't": "wasn't", "werent": "wasn't",
        "Have": "Has", "Are": "Is", "Do": "Does", "Were": "Was"}},
    "sva",
    guard={"not_group": 1, "words": [w for w in PLURAL_FORM_SINGULAR_GUARD if w != "bus"],
           "prev_not": PREV_NOT_PREPS},
))
new_rules.append(R(
    "sva_noun_plur_3sg", r"\b([a-z]{3,}s) (seems|wants|needs|likes|knows|thinks|makes|takes|gets|looks|feels|gives|keeps|comes|goes|says|wins|loses|runs|walks|plays|works|lives|moves|sends|holds|finds|buys|brings|calls|helps|asks|tells|turns|uses|visits|shows|answers|attends|starts|finishes|checks|reviews|updates|submits|registers|collects|delivers|installs|monitors|notifies|informs|cancels|transfers|approves|rejects|accepts|publishes|distributes|announces|reminds|contacts|orders|receives|pays|joins|applies|completes|confirms|signs|shares|visits|attends|answers|asks|opens|closes|books)\b",
    {"kind": "map", "group": 2, "map": {
        "seems": "seem", "wants": "want", "needs": "need", "likes": "like",
        "knows": "know", "thinks": "think", "makes": "make", "takes": "take",
        "gets": "get", "looks": "look", "feels": "feel", "gives": "give",
        "keeps": "keep", "comes": "come", "goes": "go", "says": "say",
        "wins": "win", "loses": "lose", "runs": "run", "walks": "walk",
        "plays": "play", "works": "work", "lives": "live", "moves": "move",
        "sends": "send", "holds": "hold", "finds": "find", "buys": "buy",
        "brings": "bring", "calls": "call", "helps": "help", "asks": "ask",
        "tells": "tell", "turns": "turn", "uses": "use", "visits": "visit",
        "shows": "show", "answers": "answer", "attends": "attend",
        "starts": "start", "finishes": "finish", "checks": "check",
        "reviews": "review", "updates": "update", "submits": "submit",
        "registers": "register", "collects": "collect", "delivers": "deliver",
        "installs": "install", "monitors": "monitor", "notifies": "notify",
        "informs": "inform", "cancels": "cancel", "transfers": "transfer",
        "approves": "approve", "rejects": "reject", "accepts": "accept",
        "publishes": "publish", "distributes": "distribute", "announces": "announce",
        "reminds": "remind", "contacts": "contact", "orders": "order",
        "receives": "receive", "pays": "pay", "joins": "join",
        "applies": "apply", "completes": "complete", "confirms": "confirm",
        "signs": "sign", "shares": "share", "opens": "open", "closes": "close",
        "books": "book"}},
    "sva",
    guard={"not_group": 1, "words": PLURAL_FORM_SINGULAR_GUARD + [
        "clothes", "congratulations", "news", "police", "headquarters",
        "economics", "physics", "mathematics", "politics", "statistics",
        "gymnastics", "measles", "mumps", "tennis", "chess", "genetics",
        "logistics", "ethics", "classics", "analysis", "diagnosis", "oasis",
        "synopsis", "thesis", "crisis", "basis", "staples", "stationery",
        "noodles", "spaghetti", "binoculars", "spectacles", "trousers",
        "pyjamas", "scissors", "pliers", "tongs", "tweezers", "shorts",
        "belongings", "earnings", "outskirts", "surroundings", "wages",
        "contents", "remains", "savings", "valuables"] + FAKE_PLURAL_ADVERBS,
        "prev_not": ["ten", "two", "three", "four", "five", "six", "seven",
                     "eight", "nine", "eleven", "twelve", "thirteen",
                     "fourteen", "fifteen", "sixteen", "seventeen", "eighteen",
                     "nineteen", "twenty", "thirty", "forty", "fifty",
                     "sixty", "seventy", "eighty", "ninety", "hundred",
                     "thousand", "million", "dozen", "couple", "few",
                     "several", "many", "some", "both", "half", "quarter",
                     "score", "hundred", "one", "and", "or", "plus", "per"] + PREV_NOT_PREPS,
        "no_camel": 1},
))
new_rules.append(R(
    "sva_irreg_plur", r"\b(children|people|men|women|feet|teeth|mice|geese) (was|is|has|does|seems|says|goes|wants|needs|likes|knows|thinks)\b",
    {"kind": "map", "group": 2, "map": {
        "was": "were", "is": "are", "has": "have", "does": "do",
        "seems": "seem", "says": "say", "goes": "go", "wants": "want",
        "needs": "need", "likes": "like", "knows": "know", "thinks": "think",
        "Was": "Were", "Is": "Are", "Has": "Have", "Does": "Do"}},
    "sva",
))
new_rules.append(R(
    "sva_dont_variants", r"\b(she|he|it|this|that) (don't|dont)\b",
    {"kind": "map", "group": 2, "map": {"don't": "doesn't", "dont": "doesn't",
                                         "Don't": "Doesn't"}},
    "sva",
))
new_rules.append(R(
    "sva_doesnt_variants", r"\b(they|we|you|i) (doesn't|doesnt)\b",
    {"kind": "map", "group": 2, "map": {"doesn't": "don't", "doesnt": "don't",
                                         "Doesn't": "Don't"}},
    "sva",
))
new_rules.append(R(
    "one_of_plur", r"\bone of (?:the |my |our |your |his |her |their |these |those )?([a-z]+s) (are|were|have|do|don't|aren't|haven't|weren't)\b",
    {"kind": "map", "group": 2, "map": {
        "are": "is", "were": "was", "have": "has", "do": "does",
        "don't": "doesn't", "aren't": "isn't", "haven't": "hasn't",
        "weren't": "wasn't", "Are": "Is", "Were": "Was", "Have": "Has"}},
    "sva",
))
new_rules.append(R(
    "verbform_overreg", r"\b(" + "|".join(OVERREG) + r")\b",
    {"kind": "map", "group": 1, "map": dict(OVERREG)},
    "verbform",
))
new_rules.append(R(
    "modal_reg_base", r"\b(?:can|will|should|would|must|might|could|may|shall|cannot|can't|won't|shouldn't|wouldn't|mustn't) (" + "|".join(REG_PAST_TO_BASE) + r")\b",
    {"kind": "map", "group": 1, "map": dict(REG_PAST_TO_BASE)},
    "modal",
))
new_rules.append(R(
    "modal_3sg", r"\b(?:can|will|should|would|must|might|could|may|shall|cannot|can't|won't|shouldn't|wouldn't|mustn't) (plays|customises|wants|needs|likes|knows|thinks|makes|takes|gets|looks|feels|gives|keeps|comes|goes|says|wins|loses|runs|walks|works|lives|moves|sends|holds|finds|buys|brings|calls|helps|asks|tells|turns|uses|visits|shows|answers|attends|starts|finishes|checks|reviews|updates|submits|registers|collects|delivers|installs|monitors|notifies|informs|cancels|transfers|approves|rejects|accepts|publishes|distributes|announces|reminds|contacts|orders|receives|pays|joins|applies|completes|confirms|signs|shares|opens|closes|books)\b",
    {"kind": "map", "group": 1, "map": {
        "plays": "play", "customises": "customise", "wants": "want",
        "needs": "need", "likes": "like", "knows": "know", "thinks": "think",
        "makes": "make", "takes": "take", "gets": "get", "looks": "look",
        "feels": "feel", "gives": "give", "keeps": "keep", "comes": "come",
        "goes": "go", "says": "say", "wins": "win", "loses": "lose",
        "runs": "run", "walks": "walk", "works": "work", "lives": "live",
        "moves": "move", "sends": "send", "holds": "hold", "finds": "find",
        "buys": "buy", "brings": "bring", "calls": "call", "helps": "help",
        "asks": "ask", "tells": "tell", "turns": "turn", "uses": "use",
        "visits": "visit", "shows": "show", "answers": "answer",
        "attends": "attend", "starts": "start", "finishes": "finish",
        "checks": "check", "reviews": "review", "updates": "update",
        "submits": "submit", "registers": "register", "collects": "collect",
        "delivers": "deliver", "installs": "install", "monitors": "monitor",
        "notifies": "notify", "informs": "inform", "cancels": "cancel",
        "transfers": "transfer", "approves": "approve", "rejects": "reject",
        "accepts": "accept", "publishes": "publish", "distributes": "distribute",
        "announces": "announce", "reminds": "remind", "contacts": "contact",
        "orders": "order", "receives": "receive", "pays": "pay", "joins": "join",
        "applies": "apply", "completes": "complete", "confirms": "confirm",
        "signs": "sign", "shares": "share", "opens": "open", "closes": "close",
        "books": "book"}},
    "modal",
))
new_rules.append(R(
    "subj_seen_saw", r"\b(I|we|they|you|he|she|who|people|students|clients|visitors|customers) (seen)\b",
    {"kind": "map", "group": 2, "map": {"seen": "saw", "Seen": "Saw"}},
    "verbform",
    guard={"prev_not_re": {"re": r"\b(have|has|had)\s+[a-z]*\s*$", "window": 25}},
))
new_rules.append(R(
    "be_been_being", r"\b(is|are|was|were|am) (been)\b",
    {"kind": "map", "group": 2, "map": {"been": "being", "Been": "Being"}},
    "verbform",
))
new_rules.append(R(
    "be_base_ing", r"\b(are|is|was|were|am)\s+(?:currently\s+|now\s+|still\s+|already\s+)?(review|monitor|install|deliver|prepare|perform|complete|confirm|collect|investigate|inspect|evaluate|update|upgrade|migrate|deploy|train|study|develop|maintain|support|manage|coordinate|organise|organize|arrange|schedule|process|analyse|analyze|audit|test|plan|compile|edit|document|research|target|track|trace|work|wait|look|listen|talk|speak|walk|run|drive|travel|visit|practise|practice|build|send|check|watch|read|write|learn|teach|play|eat|sleep|sit|stand|stay|move|call|try|use|need|want|think|feel|say|know|take|give|get|turn|leave|arrive|return|apply|ask|answer|bring|buy|choose|decide|find|hold|keep|meet|pay|prefer|remember|require|show|spend|suggest|tell|thank|throw|understand|wear|win|wonder|focus|concentrate|relax|exercise|commute|unpack|pack|settle|retire|graduate)(?=\s+(?:the|a|an|our|their|his|her|its|all|every|some|each|several|new|existing|safety|final|current|latest|previous|whole|entire|on|in|at|for|with|to|from|tomorrow|today|tonight|this|that|next|hard|harder)\b)",
    {"kind": "g_ing", "group": 2},
    "verbform",
))
new_rules.append(R(
    "have_base_past", r"\b(have|has|had) (" + "|".join(sorted(REG_PAST_TO_BASE.values())) + r")\b(?=\s+(?:the|a|an|our|their|his|her|its|my|your|this|that|these|those|all|each|every|some|several|new|the)\b)",
    {"kind": "map", "group": 2, "map": REG_BASE_TO_PAST},
    "verbform",
))
new_rules.append(R(
    "be_past_pp", r"\b(is|are|was|were|am|be|been|being) (" + "|".join(PAST_TO_PP) + r")\b",
    {"kind": "map", "group": 2, "map": dict(PAST_TO_PP)},
    "participle",
))
new_rules.append(R(
    "been_base_pp", r"\b(been|being) (" + "|".join(sorted(REG_BASE_TO_PAST)) + r")\b",
    {"kind": "map", "group": 2, "map": REG_BASE_TO_PAST},
    "participle",
))
new_rules.append(R(
    "be_base_reg_pp", r"\b(is|are|was|were) (" + "|".join(sorted(REG_BASE_TO_PAST)) + r")\b(?=\s+(?:the|a|an|our|their|his|her|its|my|your|this|that|by|about|for|with|to|from|in|on|at|as|before|after|during|under|over|at)\b)",
    {"kind": "map", "group": 2, "map": REG_BASE_TO_PAST},
    "participle",
))
new_rules.append(R(
    "person_ing_adj", r"\b(I|we|you|he|she|they)\s+(?:am|is|are|was|were|feel|feels|felt|have been|has been)\s+(boring|confusing|exciting|surprising|tiring|annoying)\b",
    {"kind": "map", "group": 2, "map": {
        "boring": "bored", "confusing": "confused", "exciting": "excited",
        "surprising": "surprised", "tiring": "tired", "annoying": "annoyed"}},
    "participle",
))
new_rules.append(R(
    "attach_notes", r"\b(attach) (?:notes?|documents?|files?|reports?|letters?|emails?|forms?|minutes|slides|attachments?|details|instructions|updates?|screenshots?|logs?|records?|evidence|receipts?|invoices?)\b",
    {"kind": "map", "group": 1, "map": {"attach": "attached", "Attach": "Attached"}},
    "participle",
))
new_rules.append(R(
    "then_than_broad", r"\b((?:better|worse|easier|harder|cheaper|bigger|smaller|larger|older|younger|nicer|quicker|greater|stronger|weaker|taller|shorter|longer|heavier|lighter|smarter|brighter|darker|warmer|cooler|colder|safer|ruder|stricter|simpler|gentler|friendlier|livelier|happier|angrier|busier|lazier|prettier|uglier|cuter|finer|fuller|richer|poorer|thicker|thinner|wider|narrower|deeper|higher|lower|tighter|looser|faster|slower|cleaner|weirder|more\s+\w+|less\s+\w+|rather|other|no sooner)) (then)\b",
    {"kind": "map", "group": 2, "map": {"then": "than", "Then": "Than"}},
    "homophone",
))
new_rules.append(R(
    "it_s_its_noun", r"\b(it's) (tail|paws?|head|eyes?|ears?|mouth|teeth|fur|feet|body|legs?|own|owner|mother|father|babies|kittens?|puppies?|toys?|food|bowl|collar|lead|bed|house|home|name|colou?r|size|shape|weight|length|height|age|value|price|cost|worth|purpose|role|use|origin|history|future|end|start|beginning|side|top|bottom|front|back|edges?|surface|interior|engine|wheels?|doors?|windows?|roof|seats?|screen|battery|keyboard|software|hardware|design|functions?|features?|era|day|launch|release|sale|finish|flavour|taste|smell|texture|insides?|workings?|creator|maker|author|inventor|builder|designer|planner|winner|loser|victim|hero|heroine|star|lead|theme|title|word|line|sentence|paragraph|chapter|page|cover)\b",
    {"kind": "map", "group": 1, "map": {"it's": "its", "It's": "Its"}},
    "homophone",
))
new_rules.append(R(
    "their_theyre_verb", r"\b(their) (putting|going|coming|doing|being|getting|taking|making|looking|planning|moving|buying|selling|building|working|living|staying|leaving|arriving|running|walking|talking|thinking|trying|hoping|waiting|asking|saying|having|keeping|losing|winning|driving|eating|drinking|reading|writing|playing|watching|listening|learning|teaching|training|studying|travelling|visiting|helping|showing|giving|sending|bringing|finding|feeling|growing|sitting|standing|sleeping|considering|expecting|wanting|aiming|starting|stopping|setting|putting)\b",
    {"kind": "map", "group": 1, "map": {"their": "they're", "Their": "They're"}},
    "homophone",
))
new_rules.append(R(
    "subj_past_passed", r"\b(she|he|we|they|i|you|and) (past)\b",
    {"kind": "map", "group": 2, "map": {"past": "passed", "Past": "Passed"}},
    "homophone",
))
new_rules.append(R(
    "affect_effect_noun", r"\b(?:a|an|the|his|her|their|our|its|my|your|no|noticeable|profound|slight|positive|negative|direct|side|full|overall|main|major|significant|lasting|immediate|little|big|small|serious|adverse|beneficial|harmful|minimal|dramatic|real|visible|clear|strong|weak|added|long-term|short-term|some|any) (affect)\b",
    {"kind": "map", "group": 1, "map": {"affect": "effect", "Affect": "Effect"}},
    "homophone",
))
new_rules.append(R(
    "effect_affect_verb", r"\b(?:will|would|can|could|may|might|must|should|shall|to|not|never|also|possibly|and|or|but|even|still|yet|already) (effect)\b",
    {"kind": "map", "group": 1, "map": {"effect": "affect", "Effect": "Affect"}},
    "homophone",
    guard={"not_group": 1, "words": ["change", "transition", "rescue", "cure",
                                     "repair", "payment", "settlement", "delivery",
                                     "entry", "exit", "insurance", "transfer"]},
))
new_rules.append(R(
    "compliment_complement", r"\b(?:curtains?|colou?rs?|flavou?rs?|styles?|designs?|wines?|dishes|layouts?|furnishings|furniture|artwork|carpet|carpets|paint|paintings?|fabric|fabrics|interiors?|gardens?|photos?|graphics?|shades?|tones?|themes?|textures?|materials?|finishes?|plans?|spaces?|rooms?|bedrooms?|kitchens?|bathrooms?|dresses?|outfits?|hats?|scarves?|shoes?|bags?|jewellery|makeup|hairstyle) (compliment)\b",
    {"kind": "map", "group": 1, "map": {"compliment": "complement",
                                        "Compliment": "Complement"}},
    "homophone",
))
new_rules.append(R(
    "complement_compliment_verb", r"\b(?:paid|pay|give|gave|given|paying|received|receive|got|sent|send|sending|asked|take|took|taking|accept|accepted|accepting|want|wanted|asking|offer|offered) (complement)\b",
    {"kind": "map", "group": 1, "map": {"complement": "compliment",
                                        "Complement": "Compliment"}},
    "homophone",
))
new_rules.append(R(
    "quiet_quite_adj", r"\b(quiet) (a|an|the|very|really|so|too|more|most|different|similar|large|small|big|little|bit|few|number|lot|while|good|nice|hard|easy|difficult|clear|simple|complex|strange|odd|peculiar|remarkable|impressive|unusual|common|rare|cheap|expensive|busy|noisy|heavy|light|smooth|rough|steady|stable|solid|fresh|stale|warm|cold|hot|cool|wet|dry|clean|dirty|old|new|young|brave|strong|weak|tall|short|long|fast|slow)\b",
    {"kind": "map", "group": 1, "map": {"quiet": "quite", "Quiet": "Quite"}},
    "homophone",
))
new_rules.append(R(
    "quite_quiet_noun", r"\b(quite) (quiet|quietly|silence|silent|noisy|loud|loudly|room|library|place|street|neighbourhood|car|engine|motor|fridge|computer|server|fan|machine|crowd|audience|class|children|kids|evening|morning|night|day|hour|moment)\b",
    {"kind": "map", "group": 1, "map": {"quite": "quiet", "Quite": "Quiet"}},
    "homophone",
))
new_rules.append(R(
    "me_and_swap", r"^Me and ([A-Z][a-z]+|my|our|the|his|her|their)\b",
    {"kind": "template", "template": "{1} and I"},
    "pronoun", case="",
))
new_rules.append(R(
    "her_him_them_start", r"^(Her|Him|Them) and\b",
    {"kind": "map", "group": 1, "map": {"Her": "She", "Him": "He", "Them": "They"}},
    "pronoun", case="",
))
new_rules.append(R(
    "prep_and_i_me", r"\b(?:to|for|with|from|between|by|of|at|against|without|across|behind|beyond|near|toward|towards) [a-z]+(?:\s+[a-z]+){0,2}\s+and (I)\b",
    {"kind": "map", "group": 1, "map": {"I": "me", "i": "me"}},
    "pronoun",
))
new_rules.append(R(
    "advform_adj", r"\b(" + "|".join(ADJ_TO_ADV) + r")\b(?=\s[a-z])",
    {"kind": "map", "group": 1, "map": dict(ADJ_TO_ADV)},
    "advform", case="i",
    guard={"prev_re": r"\b(" + ADV_VERBS + r")\s*$", "window": 30},
))
new_rules.append(R(
    "wh_front_missing", r"^\s*(Where|Why|What|When|How|Who|Which)\s+((?:[a-z]+\s+){1,3}?)(is|are|was|were|do|does|did|can|will|would|should|has|have|had)\b(?!\s+(?:you|we|i|they|she|he|it|the|a|an|this|that|these|those|my|our|your|their|his|her|its|all|both|some|any|each|every|most|one|two|three|four|five|who|what|which|there|someone|anyone|everyone|nobody|anybody|everybody)\b)",
    {"kind": "template", "template": "{1} {3} {2}"},
    "inversion", case="i",
))
PARTICIPLE_LOOKAHEAD = (r"(?=\s+(?:[a-z]+ed|[a-z]+en|kept|done|gone|held|sent|paid|"
                        r"lost|found|told|asked|built|sold|shown|drawn|worn|torn|"
                        r"broken|spoken|written|driven|given|eaten|taken|seen|known|"
                        r"grown|thrown|blown|flown|chosen|frozen|stolen|hidden|"
                        r"ridden|beaten|forgotten|situated|located|displayed|stored|"
                        r"collected|paid|done|due|kept)\b)")
new_rules.append(R(
    "wh_embedded", r"\b(where|when|why|what|how|who|which) (is|are|was|were|do|does|did|can|will|would|should|has|have|had) ((?:the|a|an|this|that|these|those|my|our|their|his|her|its|your)\s+(?:[a-z]+\s+){0,2}?[a-z]+?)" + PARTICIPLE_LOOKAHEAD,
    {"kind": "template", "template": "{1} {3} {2}"},
    "inversion", case="i",
    guard={"prev_re": r"\b(wonder|wondered|know|knew|knows|asked|ask|tell|told|remember|sure|think|thought|realise|realize|understand|check|guess|imagine|find out|see|explain|describe)\b[^.!?]{0,40}$",
           "window": 60},
))
new_rules.append(R(
    "i_broad", r"(?<![A-Za-z.-])i(?![A-Za-z.-])",
    {"kind": "map", "group": 0, "map": {"i": "I"}},
    "capit", case="",
))
new_rules.append(R(
    "an_yoo", r"\b(an) (universit\w+|unicor\w+|uniqu\w+|useful|useless|usual\w*|user\w*|uniform\w+|unit\w+|united|universal\w*|europe\w*|european\w*|eucalyptus|ewe|uuid|one|once|utility|utilities|ubiquit\w+)\b",
    {"kind": "map", "group": 1, "map": {"an": "a", "An": "A"}},
    "article",
))
new_rules.append(R(
    "a_silent_h", r"\b(a) (hour|hours|hourly|honest|honestly|honesty|honour|honoured|honourable|honor|honored|honorable|heir|heiress|honouree)\b",
    {"kind": "map", "group": 1, "map": {"a": "an", "A": "An"}},
    "article",
))
new_rules.append(R(
    "a_plural_some", r"\b(a) (" + PLURAL_NOUNS_FOR_A + r")\b",
    {"kind": "map", "group": 1, "map": {"a": "some", "A": "Some"}},
    "article",
))
new_rules.append(R(
    "arrive_in_venue", r"\b(arrive[sd]?|arriving) (in|to) (the|this|that|our)\s+(airport|station|hospital|hotel|motel|office|library|school|gym|cinema|theatre|theater|museum|cafe|restaurant|bank|clinic|factory|warehouse|terminal|depot|campsite|hostel|stadium|marina|wharf|beach|pool|playground|resort|garage|workshop|court|classroom|lab|laboratory|dormitory|ward|dentist|kiosk|counter|desk|reception|gate|platform|stop|yard|mill|foundry|studio|gallery|showroom|store|shop|market|supermarket|mall|salon|spa|arena|track|pitch|rink|cave|mine|bridge|junction|roundabout|corner|crossing|tunnel|mountain|hill|valley|forest|lake|river|stream|creek|waterfall|bay|harbour|harbor|port|pier|jetty|quay|dock|shore|island|reef|summit|peak|bus stop|bus station|train station|airfield|aerodrome)\b",
    {"kind": "map", "group": 2, "map": {"in": "at", "to": "at", "In": "At", "To": "At"}},
    "preposition",
))
new_rules.append(R(
    "keen_in_on", r"\bkeen (in) (?:joining|helping|learning|working|taking|getting|applying|participating|volunteering|starting|beginning|training|studying|reading|writing|playing|coaching|mentoring|teaching|assisting|contributing|supporting|joining)\b",
    {"kind": "map", "group": 1, "map": {"in": "on", "In": "On"}},
    "preposition",
))
new_rules.append(R(
    "working_in_on", r"\b(work|works|worked|working) (in) (the|this|a|an|our|that)\s+(?:new\s+|old\s+|latest\s+|current\s+|existing\s+|updated\s+|revised\s+|final\s+|other\s+|next\s+|previous\s+|first\s+|last\s+|entire\s+|whole\s+|upcoming\s+|planned\s+|proposed\s+)?(product|project|roadmap|plan|idea|issue|bug|feature|release|version|update|upgrade|task|case|ticket|prototype|design|module|component|library|framework|engine|server|cluster|database|pipeline|app|application|website|site|tool|service|platform|system|fix|patch|branch|repo|repository|codebase|backend|frontend|API|SDK|migration|refactor|test|build|deploy|deployment|document|spec|report|brief|manual|guide|tutorial)\b",
    {"kind": "map", "group": 2, "map": {"in": "on", "In": "On"}},
    "preposition",
))
new_rules.append(R(
    "more_compar_broad", r"\b(more) (?=[a-z]{4,12}(?:er|ier)\s+(?:than|of)\b)",
    {"kind": "del_next", "group": 1},
    "compar",
))
new_rules.append(R(
    "the_worse_worst", r"\bthe (worse) (meal|day|night|experience|movie|film|game|match|performance|result|outcome|weather|service|food|hotel|trip|journey|flight|concert|chapter|episode|season|decision|choice|option|place|restaurant|cafe|holiday|week|month|year|time|thing|visit|attempt|effort|version|build|release|cut|patch|draft|birthday|party|exam|test|assignment|error|mistake|accident|injury|storm|flood|fire|drought|crash|outage|breach|leak|scandal|defeat|loss|draw|tie|record|inning|spell|stretch|run|quarter|half|decade|century)\b",
    {"kind": "map", "group": 1, "map": {"worse": "worst", "Worse": "Worst"}},
    "compar",
))
FEWER_NOUNS = ("people|students|teachers|workers|customers|clients|items|files|books|cars|children|kids|men|women|tourists|visitors|teams|groups|families|houses|complaints|errors|bugs|issues|tasks|tickets|places|seats|rooms|options|choices|questions|answers|examples|words|letters|reports|notes|pages|chapters|assignments|projects|meetings|photos|pictures|songs|videos|games|goals|points|runs|wickets|tries|players|spectators|fans|staff|police|officers|patients|cases|deaths|infections|tests|samples|results|records|entries|rows|columns|fields|values|nodes|servers|clusters|machines|devices|screens|keyboards|monitors|laptops|phones|tablets|cables|wires|plugs|sockets|switches|routers|printers|scanners|cameras|batteries|chargers|tools|parts|components|modules|packages|libraries|frameworks|applications|programs|scripts|commands|functions|methods|classes|objects|variables|parameters|arguments|inputs|outputs|directories|folders|documents|logs|backups|copies|versions|releases|builds|deployments|environments|stages|phases|steps|jobs|processes|threads|workers|sessions|connections|requests|responses|messages|emails|calls|meetings|appointments|reservations|bookings|orders|purchases|sales|transactions|payments|invoices|receipts|refunds|returns|deliveries|shipments|parcels|packages|boxes|bags|cartons|crates|pallets|containers|bottles|cans|jars|tins|packets|envelopes|stamps|cards|postcards|texts|notifications|alerts|warnings|reminders|updates|statements|summaries|reviews|comments|posts|articles|stories|products|goods|supplies|materials|resources|assets|buildings|structures|bridges|roads|streets|lanes|paths|tracks|trails|routes|ways|exits|entrances|doors|windows|walls|floors|roofs|stairs|steps|lifts|elevators|platforms|stations|stops|terminals|airports|ports|docks|piers|jetties|quays|wharves|beaches|shores|coasts|cliffs|hills|mountains|valleys|forests|woods|lakes|rivers|streams|creeks|waterfalls|bays|harbours|marinas|islands|reefs")
new_rules.append(R(
    "less_fewer", r"\b(less) (" + FEWER_NOUNS + r")\b",
    {"kind": "map", "group": 1, "map": {"less": "fewer", "Less": "Fewer"}},
    "compar",
))
new_rules.append(R(
    "childs_mens", r"\b(childs|mens|womens)\b",
    {"kind": "map", "group": 1, "map": {"childs": "children's", "mens": "men's",
                                        "womens": "women's", "Childs": "Children's",
                                        "Mens": "Men's", "Womens": "Women's"}},
    "plural",
))
new_rules.append(R(
    "num_advices", r"\b(?:two|three|four|several|some|many) (advices)\b",
    {"kind": "map", "group": 1, "map": {"advices": "pieces of advice",
                                        "Advices": "Pieces of advice"}},
    "plural",
))
new_rules.append(R(
    "subj_been_have", r"\b(we|they|i|you|he|she|it|people|students) (been) (?:trying|waiting|working|living|looking|going|doing|making|thinking|planning|hoping|asking|watching|reading|studying|training|travelling|running|walking|talking|having|getting|taking|putting|calling|emailing|phoning|chasing|following|sorting|fixing|building|testing|shipping|dealing|coping|struggling|battling|campaigning|fundraising|searching|holding|keeping)\b",
    {"kind": "map", "group": 2, "map": {"been": "have been", "Been": "Have been"}},
    "missing",
))
new_rules.append(R(
    "told_that_us", r"\b(told)\b(?=\s+that\b)",
    {"kind": "map", "group": 1, "map": {"told": "told us", "Told": "Told us"}},
    "missing",
    guard={"prev_not_re": {"re": r"\b(was|were|is|are|am|been|being|be)\s*$", "window": 15}},
))
new_rules.append(R(
    "neg_dont_no_any", r"\b(don't|doesn't|didn't|haven't|hasn't|hadn't|can't|couldn't|wouldn't|shouldn't|won't|ain't) have (no)\b",
    {"kind": "map", "group": 2, "map": {"no": "any", "No": "Any"}},
    "negation",
))
new_rules.append(R(
    "neg_prep_no", r"\b(without|not|never|hardly|barely|scarcely|neither|nor) (no)\b",
    {"kind": "del_next", "group": 2},
    "negation",
))
new_rules.append(R(
    "revert_back", r"\b(revert|return|reply|repeat|repay|refund|restore|retreat|relocate|rebuild|reconnect|recount|reiterate|replicate|reproduce|resubmit|retry|revert|reverse|recall|repay) (back|again)\b",
    {"kind": "del_next", "group": 2},
    "dup",
))
new_rules.append({
    "id": "final_period",
    "re": r"^[A-Z][^.!?]*[a-z0-9'\"]$",
    "case": "",
    "apply": {"kind": "period_end"},
    "type": "punct",
    "guard": {"min_words": 4},
})
new_rules.append(R(
    "misspell_map", r"\b(" + "|".join(sorted(MISPELL)) + r")\b",
    {"kind": "map", "group": 1, "map": dict(MISPELL)},
    "spelling", case="i",
))


# ---- wh-question agreement (plural NP + singular aux and vice versa)
WH = r"(Where|Why|What|When|How|Who|Which)"
NP_PL = r"((?:[a-z]+\s+){1,3}?[a-z]+s)"
NP_SG = r"((?:[a-z]+\s+){1,3}?[a-z]+[^s\d])"
new_rules.append(R(
    "wh_pl_np_is", r"^\s*" + WH + r"\s+" + NP_PL + r" (is)\b",
    {"kind": "template", "template": "{1} are {2} "}, "inversion", case="i",
    guard={"no_camel": 2}))
new_rules.append(R(
    "wh_pl_np_was", r"^\s*" + WH + r"\s+" + NP_PL + r" (was)\b",
    {"kind": "template", "template": "{1} were {2} "}, "inversion", case="i",
    guard={"no_camel": 2}))
new_rules.append(R(
    "wh_pl_np_has", r"^\s*" + WH + r"\s+" + NP_PL + r" (has)\b",
    {"kind": "template", "template": "{1} have {2} "}, "inversion", case="i",
    guard={"no_camel": 2}))
new_rules.append(R(
    "wh_pl_np_does", r"^\s*" + WH + r"\s+" + NP_PL + r" (does)\b",
    {"kind": "template", "template": "{1} do {2} "}, "inversion", case="i",
    guard={"no_camel": 2}))
new_rules.append(R(
    "wh_sg_np_are", r"^\s*" + WH + r"\s+" + NP_SG + r" (are)\b",
    {"kind": "template", "template": "{1} is {2} "}, "inversion", case="i",
    guard={"no_camel": 2}))
new_rules.append(R(
    "wh_sg_np_were", r"^\s*" + WH + r"\s+" + NP_SG + r" (were)\b",
    {"kind": "template", "template": "{1} was {2} "}, "inversion", case="i",
    guard={"no_camel": 2}))
new_rules.append(R(
    "wh_sg_np_do", r"^\s*" + WH + r"\s+" + NP_SG + r" (do)\b",
    {"kind": "template", "template": "{1} does {2} "}, "inversion", case="i",
    guard={"no_camel": 2}))
new_rules.append(R(
    "wh_sg_np_have", r"^\s*" + WH + r"\s+" + NP_SG + r" (have)\b",
    {"kind": "template", "template": "{1} has {2} "}, "inversion", case="i",
    guard={"no_camel": 2}))
new_rules.append(R(
    "wh_pl_np_is2", r"\b(where|when|why|what|how) " + NP_PL + r" (is)\b",
    {"kind": "template", "template": "{1} are {2} "}, "inversion", case="i",
    guard={"no_camel": 2}))

# ---- contraction + of -> 'd have (informal register)
new_rules.append(R(
    "contraction_of_have", r"\b((?:hed|id|shed|wed|theyd|youd|ive|weve|theyve|youve|shouldve|couldve|wouldve|mustve|he'd|I'd|she'd|we'd|they'd|you'd|it'd|should've|could've|would've|must've)) (of)\b",
    {"kind": "map", "group": 2, "map": {"of": "have", "Of": "Have"}},
    "homophone", case="i",
))

# ---- singular noun + base verb -> 3sg (tech verbs, unambiguous only)
EXTRA_3SG = ("go|come|make|take|see|watch|look|need|want|like|know|think|say|tell|"
             "work|play|live|move|walk|talk|call|give|keep|win|find|buy|bring|help|"
             "ask|run|eat|sleep|sit|stand|sing|swim|drive|ride|write|speak|feel|"
             "hold|meet|lead|grow|build|teach|learn|study|travel|visit|pass|push|pull|"
             "wash|pay|sign|share|show|seem|stay|wait|wonder|worry|apply|try|carry")
EXTRA_3SG_MAP = {"go":"goes","come":"comes","make":"makes","take":"takes","see":"sees",
    "watch":"watches","look":"looks","need":"needs","want":"wants","like":"likes",
    "know":"knows","think":"thinks","say":"says","tell":"tells","work":"works",
    "play":"plays","live":"lives","move":"moves","walk":"walks","talk":"talks",
    "call":"calls","give":"gives","keep":"keeps","win":"wins","find":"finds",
    "buy":"buys","bring":"brings","help":"helps","ask":"asks","run":"runs",
    "eat":"eats","sleep":"sleeps","sit":"sits","stand":"stands","sing":"sings",
    "swim":"swims","drive":"drives","ride":"rides","write":"writes","speak":"speaks",
    "feel":"feels","hold":"holds","meet":"meets","lead":"leads","grow":"grows",
    "build":"builds","teach":"teaches","learn":"learns","study":"studies",
    "travel":"travels","visit":"visits","pass":"passes","push":"pushes",
    "pull":"pulls","wash":"washes","pay":"pays","sign":"signs","share":"shares",
    "show":"shows","seem":"seems","stay":"stays","wait":"waits","wonder":"wonders",
    "worry":"worries","apply":"applies","try":"tries","carry":"carries"}
new_rules.append(R(
    "sva_noun_base_3sg", r"\b(" + NOUN_SINGULAR + r") (require|use|include|provide|allow|support|offer|contain|accept|receive|deliver|send|return|confirm|specify|perform|execute|process|handle|store|load|save|write|access|validate|verify|check|test|review|approve|reject|trigger|generate|produce|display|render|consume|connect|redirect|route|resolve|parse|encode|decode|encrypt|decrypt|compress|upload|download|install|update|upgrade|delete|remove|create|define|declare|import|export|expect|promise|throw|raise|catch|track|monitor|measure|count|detect|prevent|protect|block|enable|disable|limit|restrict|control|manage|maintain|enforce|implement|authenticate|authorise|authorize|cache|compile|transpile|serialize|deserialise|deserialize|deploy|register|notify|inform|cancel|transfer|launch|publish|distribute|announce|remind|contact|collect)\b",
    {"kind": "map", "group": 2, "map": {
        "require": "requires", "use": "uses", "include": "includes",
        "provide": "provides", "allow": "allows", "support": "supports",
        "offer": "offers", "contain": "contains", "accept": "accepts",
        "receive": "receives", "deliver": "delivers", "send": "sends",
        "return": "returns", "confirm": "confirms", "specify": "specifies",
        "perform": "performs", "execute": "executes", "process": "processes",
        "handle": "handles", "store": "stores", "load": "loads",
        "save": "saves", "write": "writes", "access": "accesses",
        "validate": "validates", "verify": "verifies", "check": "checks",
        "test": "tests", "review": "reviews", "approve": "approves",
        "reject": "rejects", "trigger": "triggers", "generate": "generates",
        "produce": "produces", "display": "displays", "render": "renders",
        "consume": "consumes", "connect": "connects", "redirect": "redirects",
        "route": "routes", "resolve": "resolves", "parse": "parses",
        "encode": "encodes", "decode": "decodes", "encrypt": "encrypts",
        "decrypt": "decrypts", "compress": "compresses", "upload": "uploads",
        "download": "downloads", "install": "installs", "update": "updates",
        "upgrade": "upgrades", "delete": "deletes", "remove": "removes",
        "create": "creates", "define": "defines", "declare": "declares",
        "import": "imports", "export": "exports", "expect": "expects",
        "promise": "promises", "throw": "throws", "raise": "raises",
        "catch": "catches", "record": "records",
        "track": "tracks", "monitor": "monitors", "measure": "measures",
        "count": "counts", "detect": "detects", "prevent": "prevents",
        "protect": "protects", "block": "blocks", "enable": "enables",
        "disable": "disables", "limit": "limits", "restrict": "restricts",
        "control": "controls", "manage": "manages", "maintain": "maintains",
        "enforce": "enforces", "implement": "implements",
        "authenticate": "authenticates", "authorise": "authorises",
        "authorize": "authorizes", "cache": "caches", "compile": "compiles",
        "transpile": "transpiles", "serialize": "serializes",
        "deserialise": "deserialises", "deserialize": "deserializes",
        "deploy": "deploys", "register": "registers", "notify": "notifies",
        "inform": "informs", "cancel": "cancels", "transfer": "transfers",
        "launch": "launches", "publish": "publishes",
        "distribute": "distributes", "announce": "announces",
        "remind": "reminds", "contact": "contacts", "collect": "collects"}},
    "sva",
    guard={"not_group": 1, "words": PLURAL_FORM_SINGULAR_GUARD,
           "prev_not": PREV_NOT_PREPS},
))

# extend sva_noun_base_3sg with common unambiguous verbs
for _r in new_rules:
    if _r["id"] == "sva_noun_base_3sg":
        _r["re"] = _r["re"].replace(r") (require|", ") (" + EXTRA_3SG + r"|require|")
        _r["apply"]["map"].update(EXTRA_3SG_MAP)
        _r.setdefault("guard", {})["prev_not"] = (PREV_NOT_PREPS + MODALS_CATENATIVE)
        break

# ---- patch base rules
for rule in rules:
    if rule.get("id") == "cap_start":
        keep = ["yeah", "nah", "hey", "aye", "gonna", "wanna", "kinda", "dunno",
                "gotta", "lemme", "gimme", "sweet", "choice", "righto", "true",
                "fair", "lol", "omg", "btw", "tbh", "imo", "ngl", "yolo",
                "your", "you", "they", "them", "we", "us", "me",
                "dont", "wont", "didnt", "doesnt", "isnt", "wasnt", "werent",
                "couldnt", "shouldnt", "wouldnt", "havent", "hasnt", "hadnt",
                "aint", "im", "ive", "ill", "id", "hes", "shes", "theyre",
                "youre", "lets", "thats", "whats", "whos", "theyll", "weve",
                "shouldve", "couldve", "wouldve", "youve", "youd", "hed",
                "shed", "wed", "theyd", "itd", "hows", "arent", "aint",
                "sposed", "gonna", "cause", "till", "ok", "okay", "um", "er",
                "hows", "what", "whens", "wheres", "hows", "aint"]
        rule["guard"]["first_in"] = keep
    if rule.get("id") == "looking_fwd":
        rule["re"] = r"\b(?:look|looks|looked|looking) forward to (see|meet|hear|work|visit|join|receive|read|watch|play|talk|speak|learn|start|train|review|discuss|plan)\b"
        rule["apply"] = {"kind": "g_ing", "group": 1}
    if rule.get("id") == "contraction_apos":
        rule["re"] += ""  # unchanged regex; extend map:
        rule["apply"]["map"].update({
            "id": "I'd", "shed": "she'd", "wed": "we'd", "theyd": "they'd",
            "itd": "it'd", "youd": "you'd", "theyve": "they've",
        })
    if rule.get("id") == "plural_subj_be":
        rule.setdefault("guard", {})["prev_not_re"] = {"re": r"\bof\b", "window": 24}
        rule["guard"]["not_group"] = 1
        rule["guard"]["no_camel"] = 1
        rule["guard"]["words"] = sorted(set([
            "harness", "illness", "success", "business", "witness", "address",
            "axis", "genesis", "lens", "glass", "class", "grass", "pass",
            "guess", "kiss", "rush", "brush", "crash", "flash", "wash", "push",
            "wish", "dish", "match", "catch", "watch", "patch", "switch",
            "sketch", "ditch", "pitch", "witch", "stitch", "which", "dash",
            "cash", "trash", "smash", "splash", "finish", "publish", "punish",
            "vanish", "polish", "astonish", "accomplish", "dismiss", "express",
            "impress", "depress", "possess", "access", "assess", "discuss",
            "unless", "excess", "boss", "loss", "toss", "gloss", "cross",
            "across", "chess", "circus", "prospectus", "stimulus", "focus",
            "rebus", "corpus", "genus", "plus", "us", "thus", "status",
            "bonus", "campus", "virus", "sinus", "radius", "genius", "fungus",
            "census", "esophagus", "apparatus", "walrus", "crocus", "ibis",
            "iris", "lotus", "cactus", "octopus", "platypus", "stylus",
            "trellis", "wisteria", "news", "physics", "mathematics", "economics",
            "politics", "statistics", "gymnastics", "measles", "mumps",
            "billiards", "darts", "tennis", "chess", "molasses", "genetics",
            "logistics", "ethics", "classics", "analysis", "diagnosis",
            "oasis", "synopsis", "thesis", "crisis", "basis", "ellipsis",
            "series", "species", "means", "police", "headquarters", "gymnastics",
        ] + FAKE_PLURAL_ADVERBS))
    if rule.get("id") == "sva_sing_base":
        rule["re"] = rule["re"].replace("|read|", "|")
        # base form after do/does/did/modals is correct: "Not only did he finish"
        rule.setdefault("guard", {})["prev_not"] = MODALS_CATENATIVE
    if rule.get("id") == "a_vowel":
        rule.setdefault("guard", {}).setdefault("words", []).extend([
            "unanimous", "universal", "universe", "uranium", "utility",
            "utilities", "unit", "useless", "username", "uuid", "ewe",
            "unicorns", "uniforms", "universities", "euro", "euphonium",
        ])
    if rule.get("id") == "this_plural":
        rule["re"] = (r"\b(this|that) (?:books|files|folders|letters|reports|"
                      r"things|items|words|pages|chapters|notes|ideas|rules|"
                      r"guidelines|tables|figures|examples|questions|answers|"
                      r"gloves|shoes|boots|socks|scissors|trousers|jeans|"
                      r"pyjamas|pliers|tweezers|glasses|chopsticks|headphones|"
                      r"earphones|speakers|batteries|chargers|cables|wires|tools|"
                      r"papers|documents|templates|folders|archives|backups|"
                      r"servers|clusters|machines|devices|laptops|tablets|"
                      r"monitors|keyboards|mice|printers|scanners|cameras|lenses|"
                      r"filters|lamps|bulbs|towels|sheets|blankets|pillows|"
                      r"curtains|carpets|rugs|mats|cushions|shelves|drawers|"
                      r"mirrors|frames|albums|envelopes|stamps|cards|postcards|"
                      r"parcels|packages|packets|cans|jars|tins|sacks|bundles|"
                      r"piles|stacks|bunches|pairs|sets|kits)\b")

# reorder: wh agreement rules must precede the plain wh_front_missing swap
WH_AGREEMENT_IDS = {"wh_pl_np_is", "wh_pl_np_was", "wh_pl_np_has", "wh_pl_np_does",
                    "wh_sg_np_are", "wh_sg_np_were", "wh_sg_np_do", "wh_sg_np_have",
                    "wh_pl_np_is2"}
wh_agree = [r for r in new_rules if r["id"] in WH_AGREEMENT_IDS]
rest = [r for r in new_rules if r["id"] not in WH_AGREEMENT_IDS]
idx = next((i for i, r in enumerate(rest) if r["id"] == "wh_front_missing"), len(rest))
new_rules = rest[:idx] + wh_agree + rest[idx:]

# reorder: participle fixes precede be_base_ing so "was send to the committee"
# -> "sent" (passive, preposition follows) beats "sending"; "was review the
# document" still gets "reviewing" (determiner follows, participle rule silent).
PART_IDS = {"be_past_pp", "be_base_reg_pp", "been_base_pp"}
part_rules = [r for r in new_rules if r["id"] in PART_IDS]
rest2 = [r for r in new_rules if r["id"] not in PART_IDS]
idx2 = next((i for i, r in enumerate(rest2) if r["id"] == "be_base_ing"), len(rest2))
new_rules = rest2[:idx2] + part_rules + rest2[idx2:]

# v9.7.0 latent-FP fixes found by the adversarial probe:
# 1. wh_*_np rules absorbed a following auxiliary into the NP
#    ("What does the machine do" -> "What does does the machine").
WH_AUX_GUARD = r"(?!does\b|do\b|did\b|done\b|doing\b|can\b|could\b|will\b|would\b|"
WH_AUX_GUARD += r"shall\b|should\b|may\b|might\b|must\b|is\b|are\b|was\b|were\b|"
WH_AUX_GUARD += r"am\b|be\b|been\b|being\b|has\b|have\b|had\b)"
for rule in new_rules:
    if rule["id"] in WH_AGREEMENT_IDS:
        old = WH + r"\s+"
        rule["re"] = rule["re"].replace(old, WH + r"\s+" + WH_AUX_GUARD, 1)
# 2. there_is_plural fired on uncountables ("There is some loose change")
for rule in new_rules + rules:
    if rule.get("id") == "there_is_plural":
        rule["re"] = rule["re"].replace("|some|", "|").replace("|lots|", "|")
# 3. wh_front_missing swallowed a mid-sentence auxiliary into its subject NP
#    ("What does the machine do" -> "What do does the machine").
for rule in new_rules + rules:
    if rule.get("id") == "wh_front_missing":
        old = r"((?:[a-z]+\s+){1,3}?)"
        auxfree = r"((?:" + WH_AUX_GUARD + r"[a-z]+\s+){1,3}?)"
        rule["re"] = rule["re"].replace(old, auxfree, 1)
# 4. sva_noun_sing fired under do-support ("What does the machine do").
#    The prev_not DETS-skip (word + determiner before the noun) catches it.
AUX_DO_WORDS = ["do", "does", "did", "done", "doing", "can", "could", "will",
                "would", "shall", "should", "may", "might", "must", "is", "are",
                "was", "were", "am", "be", "been", "being", "has", "have", "had"]
for rule in new_rules + rules:
    if rule.get("id") in ("sva_noun_sing", "sva_noun_base_3sg"):
        pn = rule.get("guard", {}).get("prev_not") or []
        rule.setdefault("guard", {})["prev_not"] = list(pn) + AUX_DO_WORDS
# 5. quiet_quite_adj matched "quiet while" ("be quiet while X" is correct);
#    the real error is "quiet a while" -> "quite a while".
for rule in new_rules + rules:
    if rule.get("id") == "quiet_quite_adj":
        rule["re"] = rule["re"].replace("|while", "")
# 6. v2.7: the wh_pl_np_* family treated any NP ending in 's' as plural, so
#    singular nouns like "process"/"status" slipped through and produced
#    blind "are/were/have" inserts. Block the known fake plurals at the
#    final word of the NP so the plain wh_front_missing reorder takes over.
FAKE_PLUR_WH = (
    r"news|maths|physics|politics|economics|statistics|gymnastics|measles|mumps|"
    r"tennis|chess|genetics|logistics|ethics|classics|analysis|diagnosis|thesis|"
    r"crisis|basis|synopsis|oasis|ellipsis|genesis|status|focus|bonus|campus|"
    r"virus|radius|genius|fungus|census|sinus|apparatus|walrus|crocus|ibis|iris|"
    r"lotus|cactus|octopus|platypus|stylus|trellis|bus|gas|this|his|its|thus|us|"
    r"plus|boss|miss|less|press|cross|toss|loss|moss|fuss|process|series|species|"
    r"means|offspring|aircraft|police|headquarters|chassis|alias|canvas|atlas|"
    r"summons|chorus|crossroads|staff|team|committee|council|class|club|choir|"
    r"band|orchestra|panel|board|crew|crowd|audience|public|firm|branch|family|"
    r"group|company|government"
)
for rule in new_rules:
    if rule["id"] in WH_AGREEMENT_IDS:
        rule["re"] = rule["re"].replace(
            r"[a-z]+s)", r"(?!(?:" + FAKE_PLUR_WH + r")\b)[a-z]+s)")
new_rules.append(R(
    "quiet_a_while",
    r"\b(quiet) (a) (while)\b",
    {"kind": "map", "group": 1, "map": {"quiet": "quite", "Quiet": "Quite"}},
    "homophone",
))

# ============================================================================
# v9.7.0 recall families — classic ESL error families measured as misses on
# the X2 one-shot diagnosis. Every family is precision-guarded so the clean
# corpora (u1_clean/dev-clean/calib-clean/x2_clean) stay at zero findings.
# These rules go FIRST in the list: on overlaps the do-support fix must beat
# the older seen->saw rule ("Did you seen" -> "see", not "saw").
# ============================================================================
recall_rules = []

# -- do-support: "Did you seen" -> "see" (participle used as past under did)
DO_PP_BASE = {
    "seen": "see", "gone": "go", "done": "do", "taken": "take",
    "given": "give", "written": "write", "driven": "drive", "chosen": "choose",
    "broken": "break", "spoken": "speak", "known": "know", "eaten": "eat",
    "fallen": "fall", "forgotten": "forget", "hidden": "hide", "ridden": "ride",
    "risen": "rise", "stolen": "steal", "worn": "wear", "beaten": "beat",
    "bitten": "bite", "blown": "blow", "drawn": "draw", "grown": "grow",
    "thrown": "throw", "shown": "show", "sung": "sing", "swum": "swim",
}
recall_rules.append(R(
    "dosupport_pp_base",
    r"\b(did|didn't|didnt|does|doesn't|doesnt|do|don't|dont) (?:(?!get\b|have\b|has\b|had\b|be\b|been\b)[a-z]+ ){0,2}?(" + "|".join(sorted(DO_PP_BASE)) + r")\b",
    {"kind": "map", "group": 2, "map": DO_PP_BASE},
    "verbform",
))

# -- do-support: "does she knows" -> "know" (adjacent 3sg under does)
V3SG_BASE = {
    "leaves": "leave", "goes": "go", "comes": "come", "arrives": "arrive",
    "starts": "start", "finishes": "finish", "makes": "make", "takes": "take",
    "gets": "get", "gives": "give", "keeps": "keep", "knows": "know",
    "thinks": "think", "says": "say", "wins": "win", "loses": "lose",
    "runs": "run", "walks": "walk", "plays": "play", "works": "work",
    "lives": "live", "moves": "move", "sends": "send", "holds": "hold",
    "finds": "find", "buys": "buy", "brings": "bring", "calls": "call",
    "helps": "help", "asks": "ask", "tells": "tell", "turns": "turn",
    "uses": "use", "visits": "visit", "shows": "show", "answers": "answer",
    "attends": "attend", "opens": "open", "closes": "close", "books": "book",
    "seems": "seem", "wants": "want", "needs": "need", "likes": "like",
    "looks": "look", "feels": "feel", "travels": "travel", "returns": "return",
    "waits": "wait", "watches": "watch", "receives": "receive", "spends": "spend",
    "grows": "grow", "means": "mean", "costs": "cost", "pays": "pay",
}
# -- v2.7 recall additions (X3 pass-2 + dev FN mining): 3sg forms that were
#    missing from the shared map. Only clearly-verbal forms; noun homographs
#    (deals, means, works-as-noun, ends-as-noun in "loose ends") are excluded
#    where FP risk is real, but ends/starts/leaves are kept because the
#    do-support context (aux right before) makes the verbal reading dominant.
V3SG_BASE.update({
    "ends": "end", "trains": "train", "explains": "explain", "complains": "complain",
    "gains": "gain", "obtains": "obtain", "retains": "retain", "contains": "contain",
    "maintains": "maintain", "earns": "earn", "learns": "learn", "replies": "reply",
    "supplies": "supply", "implies": "imply", "worries": "worry", "studies": "study",
    "carries": "carry", "tries": "try", "flies": "fly", "denies": "deny",
    "copies": "copy", "hurries": "hurry", "cries": "cry", "dries": "dry",
    "varies": "vary", "marries": "marry", "catches": "catch", "fetches": "fetch",
    "reaches": "reach", "teaches": "teach", "touches": "touch", "approaches": "approach",
    "launches": "launch", "pushes": "push", "washes": "wash", "brushes": "brush",
    "crushes": "crush", "rushes": "rush", "presses": "press", "misses": "miss",
    "kisses": "kiss", "crosses": "cross", "passes": "pass", "focuses": "focus",
    "notices": "notice", "practises": "practise", "practices": "practice",
    "repeats": "repeat", "competes": "compete", "reports": "report",
    "deletes": "delete", "edits": "edit", "merges": "merge", "commits": "commit",
    "deploys": "deploy", "clones": "clone", "forks": "fork", "emails": "email",
    "messages": "message", "texts": "text",
})
recall_rules.append(R(
    "does_3sg_adjacent",
    r"\b(does|doesn't) (" + "|".join(sorted(V3SG_BASE)) + r")\b",
    {"kind": "map", "group": 2, "map": V3SG_BASE},
    "verbform",
))
# clause-final variant: "What time does the last bus leaves?" -> "leave"
# Intervening words must not be verbs (else the rule jumps into a subordinate
# clause: "What does the machine do when the train leaves?" must stay clean).
recall_rules.append(R(
    "does_3sg_final",
    r"\b(does|doesn't) (?:(?!do\b|does\b|did\b|done\b|doing\b|can\b|could\b|will\b|would\b|shall\b|should\b|may\b|might\b|must\b|is\b|are\b|was\b|were\b|am\b|be\b|been\b|being\b|has\b|have\b|had\b|get\b|got\b|gets\b|go\b|goes\b|went\b|come\b|came\b|makes\b|know\b|knows\b|think\b|thinks\b|say\b|says\b|feel\b|feels\b|look\b|looks\b|want\b|wants\b|need\b|needs\b|like\b|likes\b|believe\b|believes\b|seem\b|seems\b|when\b|while\b|before\b|after\b|because\b|since\b|where\b|who\b|which\b|that\b)[a-z]+ ){0,3}?(" + "|".join(sorted(V3SG_BASE)) + r")(?=\s*[?!])",
    {"kind": "map", "group": 2, "map": V3SG_BASE},
    "verbform",
    guard={"end": "?"},
))
# -- mid-question variant: "What time does the movie starts tonight?" -> "start"
#    (3sg not clause-final). Bounded {0,2} window + aux/subordinator exclusions keep
#    subordinate clauses ("What does the machine do when the train leaves?") clean.
recall_rules.append(R(
    "does_3sg_q",
    r"\b(does|doesn't) (?:(?!do\b|does\b|did\b|done\b|doing\b|can\b|could\b|will\b|would\b|shall\b|should\b|may\b|might\b|must\b|is\b|are\b|was\b|were\b|am\b|be\b|been\b|being\b|has\b|have\b|had\b|get\b|got\b|gets\b|when\b|while\b|before\b|after\b|because\b|since\b|where\b|who\b|which\b|that\b)[a-z]+ ){0,2}?(" + "|".join(sorted(V3SG_BASE)) + r")\b(?=[^?.!]*\?)",
    {"kind": "map", "group": 2, "map": V3SG_BASE},
    "verbform",
    guard={"end": "?"},
))

# -- missing possessive 's on person nouns: "teachers desk" -> "teacher's desk"
POSS_PLURAL_BASE = [
    "teachers", "students", "brothers", "sisters", "friends", "parents",
    "mothers", "fathers", "neighbours", "neighbors", "colleagues",
    "classmates", "teammates", "customers", "clients", "visitors", "guests",
    "players", "workers", "nurses", "doctors", "managers", "engineers",
    "lecturers", "professors", "librarians", "principals", "councillors",
    "relatives", "members", "owners", "drivers", "supervisors", "landlords",
    "tenants", "referees", "coaches", "captains", "solicitors", "witnesses",
    "jurors", "cousins", "aunts", "uncles", "grandparents", "grandchildren",
    "twins", "flatmates", "roommates", "housemates", "partners",
    "apprentices", "interns", "trainees", "mentors", "assistants",
    "receptionists", "secretaries", "clerks", "officers", "paramedics",
    "firefighters", "farmers", "builders", "plumbers", "electricians",
    "carpenters", "mechanics", "pilots", "sailors", "soldiers", "veterans",
    "pupils", "graduates", "undergraduates", "fellows", "scholars",
    "editors", "authors", "reporters", "journalists", "designers",
    "developers", "programmers", "analysts", "advisers", "advisors",
    "consultants", "accountants", "auditors", "bankers", "cashiers",
    "baristas", "chefs", "cooks", "waiters", "waitresses", "bakers",
    "butchers", "grocers", "pharmacists", "opticians", "dentists",
    "surgeons", "patients",
]
POSS_MAP = {w: w[:-1] + "'s" for w in POSS_PLURAL_BASE if w.endswith("s") and not w.endswith("ss")}
POSS_OBJECTS = (
    r"desk|desks|car|cars|office|offices|room|rooms|house|houses|flat|"
    r"apartment|phone|laptop|laptops|computer|computers|bag|bags|backpack|"
    r"briefcase|wallet|purse|keys|key|book|books|notebook|notebooks|chair|"
    r"chairs|table|tables|uniform|uniforms|shirt|jacket|coat|shoes|boots|"
    r"hat|cap|glasses|watch|birthday|wedding|funeral|holiday|holidays|"
    r"party|parties|graduation|retirement|dog|dogs|cat|cats|puppy|kitten|"
    r"horse|horses|bird|fish|garden|gardens|garage|driveway|fence|letter|"
    r"letters|email|emails|mailbox|letterbox|report|reports|essay|"
    r"assignment|assignments|homework|project|projects|exam|exams|results|"
    r"grades|marks|feedback|salary|wages|payslip|timetable|schedule|"
    r"calendar|diary|planner|agenda|minutes|notes|files|documents|papers|"
    r"toolbox|tools|equipment|badge|workstation|cubicle|locker|lockers|"
    r"bicycle|bicycles|motorbike|scooter|van|ute|trailer|boat|kayak|"
    r"surfboard|skis|tent|guitar|piano|violin|camera|headphones|suitcase|"
    r"luggage|passport|licence|license|ticket|tickets|seat|spot|place|cup|"
    r"mug|plate|bowl|umbrella|toothbrush|towel|towels|pillow|pillows|"
    r"blanket|blankets|bed|beds|wardrobe|drawers|mirror|shelves|lamp|pen|"
    r"pens|pencil|folder|folders|stapler|calculator|charger|chargers|"
    r"cable|cables|battery|batteries|screen|monitor|keyboard|mouse|printer|"
    r"bike|bikes|pushbike|tyre|tyres|heater|pump|mower|saddle|bridle|harness"
)
recall_rules.append(R(
    "poss_person_s",
    r"\b(" + "|".join(sorted(POSS_MAP)) + r") (" + POSS_OBJECTS + r")\b",
    {"kind": "map", "group": 1, "map": POSS_MAP},
    "agr",
    guard={"no_camel": 1},
))

# -- "the dogs been outside" -> "the dog's been" (missing auxiliary/possessive)
recall_rules.append(R(
    "noun_been_poss",
    r"\b(dogs|cats|puppies|kittens|horses|kids|boys|girls) (been)\b",
    {"kind": "map", "group": 1, "map": {
        "dogs": "dog's", "cats": "cat's", "puppies": "puppy's",
        "kittens": "kitten's", "horses": "horse's", "kids": "kid's",
        "boys": "boy's", "girls": "girl's"}},
    "verbform",
))

# -- "when its finished" -> "when it's finished" (clause-boundary guard:
#    "its due date" does not match because a noun follows)
ITS_PP = (
    r"finished|done|gone|broken|lost|ready|due|closed|cancelled|canceled|"
    r"sorted|fixed|available|completed|delayed|missing|found|booked|"
    r"confirmed|approved|submitted|received|accepted|rejected|paid|sent|"
    r"delivered|installed|updated|published|released|deployed|merged|"
    r"shipped|rescheduled|denied|granted|postponed|expected|required|"
    r"needed|taken|moved|deleted|removed|renewed|expired|terminated|"
    r"suspended|recalled|cancelled|stolen|damaged|scratched|cracked|"
    r"repaired|cleaned|washed|painted|restored|sold|opened|shipped"
)
recall_rules.append(R(
    "its_pp_clause",
    r"\b(its) (" + ITS_PP + r")\b(?=\s*[,.!?;:]\s|\s*[,.!?;:]*\s*$|\s+(?:we|you|i|they|he|she|it|and|but|or|so|because|if|that|then|before|after|when|while|until|already|still|now)\b)",
    {"kind": "map", "group": 1, "map": {"its": "it's"}},
    "homophone",
))
recall_rules.append(R(
    "its_time_to",
    r"\b(its) time to\b",
    {"kind": "map", "group": 1, "map": {"its": "it's"}},
    "homophone",
))

# -- double comparatives: "more louder" -> "louder"; "most best" -> "best"
COMPAR_ER_LIST = (
    r"bigger|smaller|larger|older|younger|faster|slower|higher|lower|"
    r"longer|shorter|stronger|weaker|louder|quieter|harder|softer|warmer|"
    r"colder|hotter|cooler|brighter|darker|heavier|lighter|cleaner|"
    r"dirtier|easier|funnier|happier|angrier|busier|lazier|luckier|"
    r"prettier|uglier|friendlier|steadier|deeper|wider|narrower|thicker|"
    r"thinner|richer|poorer|cheaper|dearer|nearer|earlier|later|greater|"
    r"taller|smarter|prouder|wilder|milder|gentler|simpler|humbler|"
    r"nobler|riper|ruder|fresher|closer|sadder|braver|cleverer|noisier|"
    r"drier|wetter|smellier|stickier"
)
SUPERL_LIST = (
    r"best|worst|biggest|smallest|largest|oldest|youngest|fastest|slowest|"
    r"highest|lowest|longest|shortest|strongest|weakest|loudest|quietest|"
    r"hardest|warmest|coldest|hottest|coolest|brightest|darkest|heaviest|"
    r"lightest|cleanest|dirtiest|easiest|funniest|happiest|angriest|"
    r"busiest|laziest|luckiest|prettiest|ugliest|friendliest|deepest|"
    r"widest|narrowest|thickest|thinnest|richest|poorest|cheapest|"
    r"dearest|nearest|earliest|latest|greatest|tallest|smartest|"
    r"simplest|freshest|closest|safest|saddest|bravest|rudest"
)
recall_rules.append(R(
    "double_compar_er",
    r"\b(more) (" + COMPAR_ER_LIST + r")\b",
    {"kind": "del_next", "group": 1},
    "compar",
))
recall_rules.append(R(
    "double_compar_superl",
    r"\b(most|more) (" + SUPERL_LIST + r")\b",
    {"kind": "del_next", "group": 1},
    "compar",
))

# -- indefinite singular subjects with intervening PPs:
#    "Everyone in the whanau were" -> "was" (everyone is always singular)
recall_rules.append(R(
    "indef_sg_verb",
    r"\b(everyone|everybody|someone|somebody|anyone|anybody|nobody|"
    r"everything|something|anything|nothing|each) (?:\s?(?:in|of|at|on|from|with|among|amongst|near|around|behind|inside|outside|under|over)\s+(?:the\s+|my\s+|our\s+|your\s+|their\s+|his\s+|her\s+|this\s+|that\s+|these\s+|those\s+|a\s+|an\s+)?[a-z]+ )*?(are|were|have|do|don't|dont|aren't|arent|weren't|haven't|havent)\b",
    {"kind": "map", "group": 2, "map": {
        "are": "is", "were": "was", "have": "has", "do": "does",
        "don't": "doesn't", "dont": "doesn't", "aren't": "isn't",
        "arent": "isn't", "weren't": "wasn't", "haven't": "hasn't",
        "havent": "hasn't"}},
    "sva",
))

# -- head-of-PP agreement: "The list of items are" -> "is"
#    (unambiguous container heads only; quantifier heads excluded on purpose)
recall_rules.append(R(
    "head_pp_sva",
    r"\b(the|this|that|my|our|your|their|his|her|its) (list|box|pile|stack|batch|set|selection|collection|catalogue|catalog|inventory|package|bundle|array|suite|packet|crate|chunk|segment|section|portion|part) of [a-z]+s (are|were|have|do|don't|aren't|weren't)\b",
    {"kind": "map", "group": 3, "map": {
        "are": "is", "were": "was", "have": "has", "do": "does",
        "don't": "doesn't", "aren't": "isn't", "weren't": "wasn't"}},
    "sva",
))

# -- copula + lexical verb: "I am agree" -> "I agree"
#    (base form only: "was agreed that/by/between" and "were agreeing"
#    are valid passives/progressives and stay untouched)
recall_rules.append(R(
    "be_agree",
    r"\b(am|is|are|was|were) (agree|agrees)\b",
    {"kind": "del_next", "group": 1},
    "verbform",
))

# -- "did a mistake" -> "made a mistake"
recall_rules.append(R(
    "do_mistake",
    r"\b(do|did|does|doing) (?:a |an )?(mistake|mistakes)\b",
    {"kind": "map", "group": 1, "map": {
        "do": "make", "did": "made", "does": "makes", "doing": "making"}},
    "verbform",
))

# -- dative alternation: "explained me the problem" -> "explained to me..."
#    (article lookahead keeps "explained them" / "says her name" safe)
recall_rules.append(R(
    "explain_to_io",
    r"\b(explains?|explained) (me|him|us|them)\b(?=\s+(?:the|a|an|this|that|these|those|what|why|how|where|when|my|our|your|their|his|her|its)\b)",
    {"kind": "map", "group": 2, "map": {
        "me": "to me", "him": "to him", "us": "to us", "them": "to them"}},
    "preposition",
))

# -- preposition + next/last time noun: "due on next Monday" -> "due next Monday"
recall_rules.append(R(
    "prep_next_time",
    r"\b(on|in|at) (next|last|this) (monday|tuesday|wednesday|thursday|friday|saturday|sunday|weekend|week|month|year|january|february|march|april|may|june|july|august|september|october|november|december|fortnight)\b(?!['])",
    {"kind": "del_next", "group": 1},
    "preposition",
    guard={"prev_not": ["check", "drop", "stop", "call", "log", "sign",
                        "tune", "put", "hand", "turn", "let", "cut", "fill",
                        "plug", "write", "cash", "punch", "send", "enter",
                        "key", "phase", "roll", "settle", "take", "tuck",
                        "give", "bring", "look", "book", "pencil", "lock"]},
))
recall_rules.append(R(
    "prep_yesterday",
    r"\b(on|in|at) (yesterday|tomorrow|today)\b(?!['])",
    {"kind": "del_next", "group": 1},
    "preposition",
))

# -- "The both teams" -> "Both teams"
recall_rules.append(R(
    "the_both",
    r"\b(the) (both)\b",
    {"kind": "del_next", "group": 1},
    "agr",
))

# -- "Almost people" -> "Almost everyone" (person nouns only)
ALMOST_PERSON = ("people|students|pupils|users|customers|clients|workers|staff|"
                 "teachers|employees|managers|engineers|doctors|nurses|"
                 "residents|citizens|voters|passengers|commuters|visitors|"
                 "tourists|spectators|fans|players|members|guests|teenagers|"
                 "adults|children|kids|families|parents|drivers|riders|"
                 "cyclists|pedestrians|participants|attendees|supporters|"
                 "followers|subscribers|viewers|readers|listeners|"
                 "ratepayers|taxpayers|fishermen|shopkeepers")
recall_rules.append(R(
    "almost_people",
    r"\b(almost) (" + ALMOST_PERSON + r")\b",
    {"kind": "map", "group": 2, "map": {w: "everyone" for w in ALMOST_PERSON.split("|")}},
    "agr",
))

# -- "lose" misspelled as "loose": "Loose the attitude" -> "Lose the attitude"
recall_rules.append(R(
    "loose_lose",
    r"\b(loose|loosing|loosed) (weight|weights|money|time|control|hope|faith|interest|track|touch|contact|appetite|patience|my keys|my wallet|my phone|my job|my temper|my place|the game|the match|the plot|the argument|the attitude|the lead|the election|the vote|the deal|the contract|the client|the customer|the sale|a chance|a game|a match|ground|the will|my mind|his job|her job|their jobs|the data|the file|the thread|the signal|the connection|the thread|our keys|her purse|his temper|"
    r"your place|your job|your keys|your wallet|your phone|your purse|your temper|your mind|your spot|your seat|your way|your grip|your thread|your file|your data|your chance|your hold|your track|your momentum|your balance|your direction|your concentration|your focus|your momentum|"
    r"his place|her place|their place|our place|our keys|our money|our keys|their keys|their money|their temper|their place|their way|their jobs|their minds)\b",
    {"kind": "map", "group": 1, "map": {"loose": "lose", "loosing": "losing", "loosed": "lost", "Loose": "Lose"}},
    "homophone",
))

# -- "be quite during assembly" -> "be quiet" (only before prep/end —
#    "be quite honest" stays untouched)
recall_rules.append(R(
    "be_quite",
    r"\b(be|being|been|keep|keeping|stay|staying) (quite)\b(?=\s+(?:during|while|when|in|at|for|throughout|because|until|before|after|so|and|but|as|watching|reading|working|praying|eating|sleeping|studying)\b|[,.!?;:]\s|\s*$)",
    {"kind": "map", "group": 2, "map": {"quite": "quiet"}},
    "homophone",
))

# -- v9.7.1 generic broadening (post-X3-pass-1; class-level extensions only,
#    informed by universal ESL families, never single test words):
DO_PAST_BASE = {
    "went": "go", "took": "take", "saw": "see", "ate": "eat", "drank": "drink",
    "ran": "run", "swam": "swim", "flew": "fly", "drove": "drive",
    "wrote": "write", "broke": "break", "chose": "choose", "came": "come",
    "gave": "give", "knew": "know", "spoke": "speak", "threw": "throw",
    "wore": "wear", "woke": "wake", "drew": "draw", "fell": "fall",
    "fed": "feed", "led": "lead", "left": "leave", "lost": "lose",
    "made": "make", "met": "meet", "paid": "pay", "read": "read",
    "said": "say", "sold": "sell", "slept": "sleep", "spent": "spend",
    "taught": "teach", "told": "tell", "won": "win", "found": "find",
    "got": "get", "held": "hold", "kept": "keep", "meant": "mean",
    "began": "begin", "brought": "bring", "bought": "buy", "caught": "catch",
    "felt": "feel", "forgot": "forget", "grew": "grow", "knew": "know",
    "sang": "sing", "sent": "send", "sat": "sit", "stood": "stand",
}
recall_rules.append(R(
    "dosupport_past_base",
    r"\b(did|didn't|didnt|does|doesn't|doesnt|do|don't|dont) (?:(?!get\b|have\b|has\b|had\b|be\b|been\b)[a-z]+ ){0,2}?(" + "|".join(sorted(DO_PAST_BASE)) + r")\b",
    {"kind": "map", "group": 2, "map": DO_PAST_BASE},
    "verbform",
))
# -- sentence-initial "Were going" -> "We're going" (missing pronoun)
recall_rules.append(R(
    "were_we_re",
    r"^\s*(Were) (going|coming|doing|being|having|getting|planning|hoping|thinking|trying|looking|working|waiting|leaving|heading|driving|flying|walking|running|travelling|traveling|meeting|seeing|visiting|studying|training|practising|practicing|painting|building|making|taking|bringing|buying|selling|moving|starting|finishing|watching|reading|writing|playing|eating|sleeping|sitting|staying)\b",
    {"kind": "map", "group": 1, "map": {"Were": "We're"}},
    "punct", case="",
))
# -- motion verb + "passed" -> "past" ("We walked passed the statue")
recall_rules.append(R(
    "motion_passed_past",
    r"\b(walked|drove|ran|cycled|jogged|hiked|strolled|marched|hurried|sped|swam|flew|travelled|traveled) (passed)\b",
    {"kind": "map", "group": 2, "map": {"passed": "past"}},
    "preposition",
))
# -- embedded question with pronoun subject: "She asked why was he late"
#    -> "why he was late" (guard: only in embedded clauses, never direct
#    questions at sentence start)
recall_rules.append(R(
    "wh_embedded_pron",
    r"\b(why|how|whether) (was|were|is|are|did|does|do|had|has|have) (he|she|they|we|you|it)\b",
    {"kind": "template", "template": "{1} {3} {2}"},
    "inversion", case="i",
    guard={"prev_re": r"\b(wonder|wondered|know|knew|knows|asked|ask|tell|told|remember|sure|think|thought|realise|realize|understand|check|guess|imagine|find out|see|explain|describe)\b[^.!?]{0,40}$",
           "window": 60},
))

# ==========================================================================
# -- v2.7 additions (X3 pass-2 + dev FN mining): recall families for the
#    remaining miss categories. All precision-guarded; validated against the
#    609-sentence clean corpus + 52 adversarial probe.
# ==========================================================================

# 7. sva_noun_plur_3sg gets the full extended 3sg verb map too ("players trains")
for rule in new_rules:
    if rule["id"] == "sva_noun_plur_3sg":
        rule["re"] = r"\b([a-z]{3,}s) (" + "|".join(sorted(V3SG_BASE)) + r")\b"
        rule["apply"]["map"].update(V3SG_BASE)

# 8. "Almost people in the office were off sick" -> second edit: were -> was
recall_rules.append(R(
    "almost_people_be",
    r"\b(almost) (people|students|pupils|users|customers|clients|workers|guests|players|members|children|kids|teenagers|adults|residents|citizens|voters|passengers|commuters|visitors|tourists|spectators|fans|employees|teachers|managers|engineers)\b[^.!?]{0,40}?\b(were|are|have|do)\b",
    {"kind": "map", "group": 3, "map": {"were": "was", "are": "is", "have": "has",
                                          "do": "does", "Were": "Was", "Are": "Is"}},
    "sva",
))

# 9. modal + past-tense verb: "We should studied" -> "should have studied"
recall_rules.append(R(
    "modal_have_past",
    r"\b(should|could|would|must|might|may|cannot|can't|won't|shouldn't|couldn't|wouldn't|mustn't) (?!\w*eed\b)([a-z]{2,}ed)\b",
    {"kind": "template", "template": "{1} have {2}"},
    "tense",
))

# 10. have/has + base verb + determiner: "The staff have attend the training"
#     -> "attended" (whole-phrase map matches gold exactly)
HAVEBASE_VB = {
    "attend": "attended", "submit": "submitted", "deliver": "delivered",
    "complete": "completed", "finish": "finished", "start": "started",
    "begin": "began", "book": "booked", "order": "ordered", "receive": "received",
    "confirm": "confirmed", "cancel": "cancelled", "update": "updated",
    "install": "installed", "check": "checked", "review": "reviewed",
    "approve": "approved", "reject": "rejected", "accept": "accepted",
    "collect": "collected", "register": "registered", "sign": "signed",
    "share": "shared", "contact": "contacted", "transfer": "transferred",
    "announce": "announced", "publish": "published", "remind": "reminded",
    "join": "joined", "apply": "applied", "open": "opened", "close": "closed",
    "fix": "fixed", "patch": "patched", "merge": "merged", "push": "pushed",
    "build": "built", "test": "tested", "upload": "uploaded",
    "download": "downloaded", "launch": "launched", "visit": "visited",
    "call": "called", "email": "emailed", "pay": "paid", "send": "sent",
    "arrive": "arrived", "train": "trained", "monitor": "monitored",
    "notify": "notified", "inform": "informed", "distribute": "distributed",
}
HAVEBASE_MAP = {}
for _v, _p in HAVEBASE_VB.items():
    HAVEBASE_MAP["have " + _v] = _p
    HAVEBASE_MAP["has " + _v] = _p
    HAVEBASE_MAP["Have " + _v.title()] = _p
    HAVEBASE_MAP["Has " + _v.title()] = _p
recall_rules.append(R(
    "have_base_dobj",
    r"\b(" + "|".join(sorted(HAVEBASE_MAP)) + r")\b(?=\s+(?:the|a|an|my|our|your|their|his|her|its|this|that|these|those|each|every|some|any|no|all|both|us|me|them|him|her|it|last|next|another|several)\b)",
    {"kind": "map", "group": 1, "map": HAVEBASE_MAP},
    "verbform", case="i",
))

# 11. capable/incapable to + verb -> "of + gerund" (engine kind to_of_ing)
recall_rules.append(R(
    "capable_to_ing",
    r"\b(capable|incapable|Capable|Incapable) to ([a-z]+)\b",
    {"kind": "to_of_ing", "group": 2},
    "preposition",
))

# 12. bare wh-question with 3sg verb, no auxiliary: "What time the shop opens?"
#     -> two findings: insert "does" + de-3sg the verb (matches gold's 2 edits)
QWH = r"(what time|where|when|why|what|which|how|who|whose|What time|Where|When|Why|What|Which|How|Who|Whose)"
QAUX = r"(?:does|do|did|is|are|was|were|can|could|will|would|shall|should|may|might|must|has|have|had|don't|doesn't|aren't|isn't|wasn't|weren't|am)\b"
recall_rules.append(R(
    "whq_does_insert",
    r"^\s*" + QWH + r"\s+(?!" + QAUX + r")(?=(?:[a-z]+\s+){0,2}?(?:" + "|".join(sorted(V3SG_BASE)) + r")\b(?=[^?.!]*\?))",
    {"kind": "template", "template": "{1} does "},
    "inversion", case="i",
    guard={"end": "?"},
))
recall_rules.append(R(
    "whq_3sg_base",
    r"^\s*" + QWH + r"\s+(?!" + QAUX + r")(?:[a-z]+\s+){0,2}?" + "(" + "|".join(sorted(V3SG_BASE)) + r")\b(?=[^?.!]*\?)",
    {"kind": "map", "group": 2, "map": V3SG_BASE},
    "sva", case="i",
    guard={"end": "?"},
))

# 13. plural noun + PP + was/is: "The plums in the bowl was bruised" -> were
#     (only with an intervening PP: plain adjacency "items was" never fires,
#      so head-of-PP sentences like "the list of items was" stay untouched)
PLUR_ONLY = {"trousers", "jeans", "pyjamas", "scissors", "pliers", "tongs",
             "tweezers", "binoculars", "spectacles", "shorts", "glasses",
             "clothes", "wages", "thanks", "belongings", "earnings",
             "congratulations", "contents", "remains", "savings", "outskirts",
             "surroundings", "valuables", "noodles", "spaghetti", "staples"}
recall_rules.append(R(
    "noun_plur_pp_was",
    r"\b([a-z]{3,}s)\s+(?:in|on|at|with|from|near|beside|along|under|over|inside|outside|behind|about|around)\s+(?:the|a|an|this|that|my|our|your|their|his|her|its)\s+(?:[a-z]+\s+){0,2}?[a-z]+\s+(was|is)\b",
    {"kind": "map", "group": 2, "map": {"was": "were", "is": "are",
                                          "Was": "Were", "Is": "Are"}},
    "sva",
    guard={"not_group": 1, "words": [w for w in PLURAL_FORM_SINGULAR_GUARD
                                     + FAKE_PLURAL_ADVERBS if w not in PLUR_ONLY],
           "prev_not": PREV_NOT_PREPS + ["two", "three", "four", "five", "six",
            "seven", "eight", "nine", "ten", "hundred", "thousand", "million",
            "several", "many", "few", "both", "half", "quarter", "score"]},
))

# 14. collective + GB-plural verb + US-singular "its" in the same clause
#     (mixed register): "The committee were unanimous in its decision" -> was
recall_rules.append(R(
    "collective_its_mixed",
    r"\b(committee|government|board|company|firm|panel|council|team|staff|family|council|organisation|organization) (were|are|have)\b[^.!?]{0,60}?(?:its|it has|it is)\b",
    {"kind": "map", "group": 2, "map": {"were": "was", "are": "is", "have": "has",
                                          "Were": "Was", "Are": "Is", "Have": "Has"}},
    "sva",
))

out = {"rules": recall_rules + new_rules + rules, "version": "rules-2.7"}
dst = os.path.join(HERE, "rules2.json")
json.dump(out, open(dst, "w"), indent=1)
print(f"rules2.json: {len(recall_rules)} recall + {len(new_rules)} new + {len(rules)} base = {len(recall_rules)+len(new_rules)+len(rules)} rules (recall first)")

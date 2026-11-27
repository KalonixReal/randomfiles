"""Expanded protected-class families (programmatic pools) + extra clean
families. Replaces the small clean-only families from frames.py and adds
volume so every test coverage tag has a full quota of unique instances."""

import random
from lexicon import VERBS, NOUNS, ADJ, ADV
from frames import PROFF

SING = [n for n in NOUNS["singular"]]
PLUR = [n for n in NOUNS["plural"]]
V3 = {b: f[0] for b, f in VERBS.items()}

rr = random.Random(4242)

UK_PLACES2 = ["harbour", "centre", "theatre", "village hall",
              "market square", "old library", "university",
              "gallery", "cricket ground", "community centre",
              "leisure centre", "railway station", "science centre",
              "boating club", "scout hall", "church hall",
              "town square", "ferry terminal"]
US_PLACES2 = ["center", "theater", "mall", "downtown library",
              "stadium", "plaza", "community center",
              "convention hall", "ballpark", "transit hub",
              "courthouse", "chamber of commerce", "airport lounge",
              "youth center", "recreation center"]
NZ_SPOTS = ["bach", "marae", "dairy", "kura", "paddock",
            "woolshed", "campground", "sports ground",
            "community hall", "skate park", "boat ramp",
            "local beach", "netball courts", "sports pavilion",
            "school field", "riverbank", "bush track",
            "holiday park"]


# ---------------------------------------------------------------- numbers
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

MONEY = [f"${d}" for d in (42, 17, 230, 842, 1025, 97, 56, 1234, 58, 76,
                            19, 33, 218, 409, 1550, 66, 91, 305, 88, 47)]
MONEY_C = [f"${d},{c:02d}" for d in (1234, 842, 56, 97, 2345, 1550, 678,
                                      901, 345, 2100) for c in (50, 25, 90, 75, 10)]
TIMES = ["9:00 a.m.", "8:30 a.m.", "10:00 a.m.", "7:45 a.m.", "11:15 a.m.",
         "2:30 p.m.", "4:45 p.m.", "5:30 p.m.", "6:00 p.m.", "8:15 p.m.",
         "7:00 a.m.", "9:45 a.m.", "1:00 p.m.", "3:20 p.m.", "5:05 p.m."]
CNT = [str(x) for x in (12, 15, 18, 24, 30, 36, 42, 48, 60, 100, 120, 240)]
POPN = ["5.12 million", "4.9 million", "6.2 million", "1.8 million",
        "3.4 million", "0.9 million", "2.5 million", "4.1 million"]
RESP = ["1,500", "2,300", "850", "3,200", "1,120", "4,600", "950", "2,750"]
GRAMS = ["250 g", "300 g", "180 g", "500 g", "125 g", "375 g", "550 g", "75 g"]
KMS = ["42.2 km", "21.1 km", "10 km", "5 km", "15 km", "30 km", "8 km"]
HRS = ["3 hours 51 minutes", "1 hour 45 minutes", "50 minutes",
       "2 hours 30 minutes", "1 hour 12 minutes", "46 minutes"]
PCS = ["20%", "15%", "25%", "10%", "30%", "12.5%", "18%"]
SAVES = ["$19.80", "$12.75", "$31.20", "$5.50", "$48.00", "$9.35"]
ROOMS = ["12B", "7A", "3C", "9D", "5E", "14F", "2G", "11H"]
FLOORS = ["fourth", "second", "tenth", "sixth", "eighth", "third", "ninth"]
PIS = ["3.14159", "3.14", "2.71828", "1.61803", "0.57721"]
SPEEDS = ["87 ms", "142 ms", "203 ms", "54 ms", "99 ms", "311 ms"]
VERSIONS = ["1.29", "2.4", "3.1", "5.7", "4.2", "6.0", "8.3", "9.1"]

NUM_FAMILIES = [
    ("numbers", [
        ("The invoice totalled {AM} including GST.", {"AM": MONEY + MONEY_C}, None),
        ("Our office is open from {T1} to {T2}", {"T1": TIMES, "T2": TIMES}, None),
        ("She paid {AM} for the ticket.", {"AM": MONEY}, None),
        ("The population reached {NUM} in 2019.", {"NUM": POPN}, None),
        ("We ordered {CNT} boxes and {CNT2} pens.", {"CNT": CNT, "CNT2": CNT}, None),
        ("The survey covered {N} respondents.", {"N": RESP}, None),
        ("The recipe uses {GR} of flour.", {"GR": GRAMS}, None),
        ("He ran {KM} in {HRS}.", {"KM": KMS, "HRS": HRS}, None),
        ("The discount is {PC}, so you save {SAVE}.", {"PC": PCS, "SAVE": SAVES}, None),
        ("Room {RM} is on the {F} floor.", {"RM": ROOMS, "F": FLOORS}, None),
        ("Pi is approximately {PI} in this calculation.", {"PI": PIS}, None),
        ("The average response time was {S} last quarter.", {"S": SPEEDS}, None),
        ("We upgraded to version {V} of the platform.", {"V": VERSIONS}, None),
        ("The invoice came to {AM} before shipping.", {"AM": MONEY + MONEY_C}, None),
        ("She saved {AM} by booking early.", {"AM": MONEY[:15]}, None),
        ("The project ran {N} days over schedule.", {"N": CNT}, None),
        ("Attendance rose to {N} people this term.", {"N": RESP}, None),
        ("The parcel weighed {GR} exactly.", {"GR": GRAMS}, None),
        ("Our team answered {N} calls that morning.", {"N": RESP}, None),
    ]),
]

# ---------------------------------------------------------------- dates
FULL_DATES = [f"{d} {m} {y}" for d in (1, 3, 5, 8, 14, 17, 21, 25, 28)
              for m in MONTHS for y in (2024, 2025)]
rr2 = random.Random(77)
FULL_DATES = rr2.sample(FULL_DATES, 160)
SLASH_DATES = [f"{d:02d}/{m:02d}/{y}" for d in (3, 7, 12, 18, 22, 28)
               for m in (1, 4, 6, 9, 11) for y in (2024, 2025)]
SLASH_DATES = rr2.sample(SLASH_DATES, 60)
DAY_MONTH = [f"{d} {m}" for d in (30, 15, 1, 12, 22) for m in MONTHS]
DAY_TIMES = ["5 p.m.", "noon", "9 a.m.", "11 a.m.", "2 p.m.", "4 p.m."]

DATE_FAMILIES = [
    ("dates", [
        ("The meeting runs from {D1} to {D2}.", {"D1": FULL_DATES, "D2": FULL_DATES}, None),
        ("They arrived on {D1} and left on {D2}.", {"D1": SLASH_DATES, "D2": SLASH_DATES}, None),
        ("The contract was signed on {D1}.", {"D1": FULL_DATES[:80]}, None),
        ("The deadline is {D1} at {T}", {"D1": DAY_MONTH, "T": DAY_TIMES}, None),
        ("Our branch reopened on {D1} after the renovation.", {"D1": FULL_DATES[80:]}, None),
        ("The warranty expires on {D1}.", {"D1": FULL_DATES[:60]}, None),
        ("We launch the new site on {D1}.", {"D1": FULL_DATES[60:100]}, None),
        ("The audit begins on {D1} and closes on {D2}.", {"D1": FULL_DATES[100:130], "D2": FULL_DATES[130:]}, None),
        ("She joined the team on {D1}.", {"D1": FULL_DATES[:40]}, None),
        ("The term starts on {D1}.", {"D1": FULL_DATES[40:80]}, None),
        ("Payment is due by {D1}.", {"D1": DAY_MONTH}, None),
        ("The order shipped on {D1}.", {"D1": SLASH_DATES[:30]}, None),
        ("They moved house on {D1}.", {"D1": SLASH_DATES[30:]}, None),
    ]),
]

# ---------------------------------------------------------------- quotes
ADJQ = ["quietly", "masterful", "brilliant", "ambitious", "tender", "funny",
        "haunting", "taut", "stylish", "sharp", "sincere", "unmissable",
        "gorgeous", "moving", "gripping"]
NOUNQ = ["debut", "performance", "memoir", "novel", "thriller", "saga",
         "essay", "collection", "portrait", "character study", "ballad",
         "romance", "comedy", "drama", "biography"]
VERBQ = ["improved", "raised", "doubled", "stabilised", "accelerated",
         "surged", "climbed", "rebounded", "widened", "softened"]
NOUN2Q = ["attendance", "membership", "turnover", "readership", "engagement",
          "funding", "readership", "sales", "enrolment"]
QUOTE_TEXTS = {
    "reviewer": [f'"a {a} {n}."' for a in ADJQ for n in NOUNQ] +
                [f'"an ambitious, uneven {n}."' for n in NOUNQ[:5]] +
                [f'"simply unmissable."' , '"quietly subversive."'],
    "principal": [f'"{v} this term."' for v in VERBQ] +
                 [f'"the {n} finishes in July."' for n in ("rebuild", "pool", "gym", "lab")] +
                 ['"every learner deserves support."',
                  '"the gala raised record funds."',
                  '"we will trial new timetables."',
                  '"the new lab opens in August."'],
    "greet": ['"Kia ora,"', '"Nau mai,"', '"Haere mai,"', '"Talofa,"',
              '"Fakaalofa,"', '"Tēnā koe,"'],
    "notice": ['"closed until further notice."', '"no entry after 5 p.m."',
               "'back in ten minutes.'", '"quiet zone — exams in progress."',
               '"the studio is closed."', '"deliveries go to reception."'],
    "asked": [f'"did anyone see the missing {n}?"' for n in ("file", "keys", "folder", "parcel", "report", "invoice", "roster", "timetable")] +
             [f'"has the courier delivered the {n}?"' for n in ("parcel", "envelope", "box", "crate")] +
             [f'"when does the {n} leave?"' for n in ("coach", "ferry", "train", "shuttle", "bus")],
    "email": [f'"thank you for your prompt {n}."' for n in ("reply", "response", "feedback", "update")] +
             [f'"please find the {n} attached."' for n in ("minutes", "report", "invoice", "agenda")] +
             ['"we regret the delay in responding."',
              '"kindly confirm your attendance."'],
    "captain": ['"We won the debate,"', '"We topped the group,"',
                '"We made the final,"', '"We take the series,"'],
    "headline": ['"Council approves the new cycleway."', '"Rates rise 3.2 percent."',
                 '"Ferry timetable extended."', '"New library opens on Saturday."'],
}
QUOTE_PUB = ["the Herald", "the Post", "The Times", "the ODT", "the Gazette",
             "the Standard", "the Chronicle", "the Tribune", "the Guardian",
             "the Journal", "the Weekly", "the Outlook"]
QUOTE_WHEN = ["on Monday", "last week", "in April", "this morning", "in the review",
              "after the launch", "at the opening", "in the autumn issue"]
QUOTE_FAMILIES = [
    ("quotes", [
        ("The reviewer wrote in {P}, {Q}", {"P": QUOTE_PUB, "Q": QUOTE_TEXTS["reviewer"]}, None),
        ("Our principal said at assembly, {Q}", {"Q": QUOTE_TEXTS["principal"]}, None),
        ("{Q} she said as she welcomed the visitors.", {"Q": QUOTE_TEXTS["greet"]}, None),
        ("The notice read: {Q}", {"Q": QUOTE_TEXTS["notice"]}, None),
        ("He asked {W}, {Q}", {"W": ["again", "quietly", "twice", "later"], "Q": QUOTE_TEXTS["asked"]}, None),
        ("The email began, {Q}", {"Q": QUOTE_TEXTS["email"]}, None),
        ("{Q} the captain announced {W}.", {"Q": QUOTE_TEXTS["captain"], "W": ["proudly", "yesterday", "after the final whistle"]}, None),
        ("The headline read, {Q}", {"Q": QUOTE_TEXTS["headline"]}, None),
        ("The letter ended, {Q}", {"Q": QUOTE_TEXTS["email"] + QUOTE_TEXTS["reviewer"][:20]}, None),
        ("She quoted the critic directly: {Q}", {"Q": QUOTE_TEXTS["reviewer"]}, None),
        ("The coach told the team, {Q}", {"Q": ['"focus on the basics."', '"we play as one unit,"', '"leave nothing in the tank."', '"trust the process."']}, None),
        ("The notice on the door said, {Q}", {"Q": QUOTE_TEXTS["notice"]}, None),
        ("In her journal she wrote, {Q}", {"Q": ['"keep going anyway."', '"the light changes everything."'] + QUOTE_TEXTS["reviewer"][:10]}, None),
    ]),
]

# ---------------------------------------------------------------- uk / us
UKSPELL = [("colour", "color"), ("organised", "organized"),
           ("centre", "center"), ("travelled", "traveled"),
           ("practised", "practiced"), ("programme", "program"),
           ("theatre", "theater"), ("favourite", "favorite"),
           ("realised", "realized"), ("harbour", "harbor"),
           ("licence", "license"), ("defence", "defense"),
           ("aluminium", "aluminum"), ("metre", "meter")]
UKW = [u for u, _ in UKSPELL]
USW = [u for _, u in UKSPELL]
UKV = ["organised", "painted", "reviewed", "catalogued", "measured",
       "described", "displayed", "collected", "labelled", "checked"]
UK_PLACES = ["harbour", "centre", "theatre", "village hall",
             "market square", "old library", "university",
             "gallery", "cricket ground", "community centre"]
UK_PLACES_BARE = UK_PLACES

UKW2 = ["colours", "organisers", "centres", "programmes", "theatres",
         "harbours", "licences", "metres", "flavours", "labours"]
UKF = [
    ("uk", [
        ("We {V3} the {U} yesterday.", {"V3": UKV, "U": UKW}, None),
        ("We {V3} the {U} {W}.", {"V3": UKV, "U": UKW2, "W": ["last week", "this term", "in spring", "before the festival", "after the show"]}, None),
        ("She {V3} the {U} last night.", {"V3": UKV[:8], "U": UKW}, None),
        ("The {U} looks perfect in the programme.", {"U": UKW}, None),
        ("I {V2} the {U} to the {P}.", {"V2": ["walked", "carried", "took"], "U": UKW, "P": UK_PLACES2}, None),
        ("They photographed the {U} near the {P}.", {"U": UKW, "P": UK_PLACES2}, None),
        ("The {U} of the hall was repainted in April.", {"U": UKW[:8]}, None),
        ("Our theatre group {V3} a new {U} in May.", {"V3": UKV[:6], "U": UKW}, None),
        ("He described the {U} in the programme notes.", {"U": UKW}, None),
        ("The licence fee covers the {U} inspection.", {"U": UKW[:8]}, None),
        ("She travelled to the {U} by tram.", {"U": UKW}, None),
    ]),
    ("us", [
        ("We {V3} the {U} yesterday.", {"V3": UKV, "U": USW}, None),
        ("She {V3} the {U} last night.", {"V3": UKV[:8], "U": USW}, None),
        ("She {V3} the {U} {W}.", {"V3": UKV[:8], "U": [w + "s" for w in USW if w not in ("color", "honor")][:8], "W": ["last week", "this term", "in spring", "before the festival", "after the show"]}, None),
        ("The {U} looks perfect in the program.", {"U": USW}, None),
        ("The {U} look perfect in the program notes.", {"U": [w + "s" for w in USW if w not in ("color", "honor")][:8]}, None),
        ("I {V2} the {U} to {P}.", {"V2": ["walked", "carried", "took"], "U": USW, "P": ["the center", "the theater", "the mall", "the downtown library", "the stadium", "the plaza"]}, None),
        ("They photographed the {U} near {P}.", {"U": USW, "P": ["the center", "the theater", "the harbor"]}, None),
        ("The {U} of the hall was repainted in April.", {"U": USW[:8]}, None),
        ("He described the {U} in the program notes.", {"U": USW}, None),
        ("She traveled to the {U} by subway.", {"U": USW}, None),
    ]),
]

# ---------------------------------------------------------------- nz
NZF2 = [
    ("nz", [
        ("We went {ACT} near {P} last {T}.", {"ACT": ["tramping", "camping", "fishing", "swimming", "cycling", "hiking", "kayaking", "climbing"],
                                              "P": ["Lake Waikaremoana", "the Remarkables", "Milford Sound",
                                                    "Mount Taranaki", "the Heaphy Track", "Tongariro",
                                                    "the Coromandel", "Kaikoura", "Franz Josef",
                                                    "Lake Taupō", "Wanaka", "Mount Cook", "Stewart Island",
                                                    "the Abel Tasman", "Cape Reinga"],
                                              "T": ["fortnight", "January", "summer", "spring", "July", "September", "the holidays", "the long weekend"]}, None),
        ("He drove the ute to the {T} for the long weekend.", {"T": ["bach", "farm", "marae", "crib", "batch", "holiday home", "campsite", "lodge"]}, None),
        ("Grab some {T} from the dairy on the way home.", {"T": ["pies", "bread", "milk", "eggs", "lollies", "chippies", "ice blocks", "sausage rolls"]}, None),
        ("The kids wore {T} at the beach.", {"T": ["togs", "togs and jandals", "swimming gear", "rash shirts"]}, None),
        ("There's {T} of kai at the shared table.", {"T": ["heaps", "plenty", "stacks", "loads"]}, None),
        ("The {T} behind the dairy leads to the school.", {"T": ["footpath", "path", "track", "walkway", "shortcut"]}, None),
        ("{Q}, the crew finished the job early.", {"Q": ["Sweet as", "Choice", "Ka pai"]}, None),
        ("Kia ora, welcome to our {T}.", {"T": ["little slice of paradise", "new classroom", "community hall", "whare", "school fair"]}, None),
        ("{NM} is learning te reo Māori at the kura.", {"NM": ["Wiremu", "Aroha", "Hōne", "Mereana", "Rawiri", "Tane", "Manaia", "Kavita", "Priya", "Mei"]}, None),
        ("The {T} organised a sausage sizzle for the tamariki.", {"T": ["PTA", "committee", "class", "senior students", "kapa haka group"]}, None),
        ("We'll sort the {T} this arvo.", {"T": ["mowing", "rubbish", "gear", "fencing", "packing"]}, None),
        ("The nz tui sang in the kōwhai outside the {T}.", {"T": ["classroom", "office", "kitchen", "garage"]}, None),
        ("After the hui we shared a hangi at the {T}.", {"T": ["marae", "hall", "campsite", "beach"]}, None),
    ]),
]

# ---------------------------------------------------------------- negation clean + more clean
NEGF2 = [
    ("negation", [
        ("I didn't see anything unusual at the {N}.", {"N": SING[:40]}, None),
        ("Nobody in the team knew the {N}.", {"N": SING[:40]}, None),
        ("Hardly anyone noticed the {N}.", {"N": SING[:40]}, None),
        ("She never says anything unkind about the {N}.", {"N": SING[:40]}, None),
        ("We couldn't find any {PL} near the venue.", {"PL": PLUR[:40]}, None),
        ("There wasn't anybody at {T} this morning.", {"T": ["reception", "the counter", "the gate", "the front desk", "the kiosk"]}, None),
        ("They don't need anything else from the {N}.", {"N": SING[:40]}, None),
        ("Scarcely a {N} passes without a new report.", {"N": ["week", "month", "quarter", "fortnight"]}, None),
        ("I haven't told anybody about the {N} yet.", {"N": SING[:40]}, None),
        ("We haven't changed anything in the {N}.", {"N": SING[:40]}, None),
    ]),
]

CLEAN_EXTRA = [
    ("clean", [
        ("The committee will decide on {D}.", {"D": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]}, None),
        ("Our records show a steady improvement in {T}.", {"T": ["attendance", "readability", "accuracy", "turnover", "engagement"]}, None),
        ("The new policy takes effect next {M}.", {"M": MONTHS}, None),
        ("{NM} coordinates the schedule for the whole {T}.", {"NM": ["Wiremu", "Aroha", "Priya", "Mereana", "Rawiri", "Kavita", "Mei", "Rohan"], "T": ["programme", "season", "term", "project", "tour"]}, None),
        ("Neither of the {T} was available that week.", {"T": ["drivers", "managers", "trainees", "inspectors"]}, None),
        ("Each of the students has a {T}.", {"T": ["locker", "timetable", "mentor", "workbook", "desk"]}, None),
        ("One of the files was missing from the {T}.", {"T": ["archive", "cabinet", "server", "folder"]}, None),
        ("The data suggest that the trend is {T}.", {"T": ["real", "stable", "accelerating", "regional"]}, None),
        ("All of the cake has been {T}.", {"T": ["eaten", "sliced", "shared", "sold"]}, None),
        ("Some of the water has {T} overnight.", {"T": ["evaporated", "frozen", "spilled", "drained"]}, None),
        ("None of the printers are {T}.", {"T": ["working", "connected", "ready", "stocked"]}, None),
        ("The police are investigating the {T}.", {"T": ["burglary", "incident", "report", "outage"]}, None),
        ("Mathematics is my {T} subject.", {"T": ["favourite", "best", "strongest"]}, None),
        ("Ten kilometres is a long way to {T}.", {"T": ["walk", "run", "cycle", "drive"]}, None),
        ("I could have finished earlier if I'd {T}.", {"T": ["started sooner", "asked for help", "skipped lunch"]}, None),
        ("We had better leave before the {T}.", {"T": ["rain", "traffic", "meeting", "storm"]}, None),
        ("Between you and me, the {T} was burnt.", {"T": ["cake", "toast", "roast", "casserole"]}, None),
        ("The well-trained {T} performed admirably.", {"T": ["team", "crew", "choir", "cast"]}, None),
        ("A well-written {T} deserves a high mark.", {"T": ["essay", "report", "summary", "review"]}, None),
        ("She is one of those teachers who always {T}.", {"T": ["help", "listen", "encourage", "prepare"]}, None),
        ("The sheep grazed quietly in the {T}.", {"T": ["top paddock", "back field", "eastern block"]}, None),
        ("My hair is getting longer every {T}.", {"T": ["month", "week", "fortnight"]}, None),
        ("The news from headquarters was {T}.", {"T": ["encouraging", "mixed", "delayed"]}, None),
        ("I have never been anywhere so {T}.", {"T": ["remote", "busy", "beautiful"]}, None),
        ("The team have submitted their {T}.", {"T": ["report", "expenses", "roster", "submission"]}, None),
        ("A number of {T} were absent today.", {"T": ["students", "staff", "delegates", "players"]}, None),
        ("It was I who called the {T}.", {"T": ["meeting", "helpline", "office", "supplier"]}, None),
        ("That is she at {T}.", {"T": ["reception", "the counter", "the front desk"]}, None),
        ("Whom shall I say is {T}?", {"T": ["calling", "waiting", "next"]}, None),
        ("You had me at {T}.", {"T": ["hello", "'brilliant'", "'sure'"]}, None),
    ]),
]

ESSAY_CLEAN = [
    ("Learning a second language requires {T}.", {"T": ["patience and daily practice", "discipline and curiosity", "courage and consistency"]}, None),
    ("Reading widely improves both {T}.", {"T": ["vocabulary and critical thinking", "fluency and comprehension", "focus and imagination"]}, None),
    ("Exercise helps students {T}.", {"T": ["concentrate during long lessons", "sleep better at night", "manage stress during exams"]}, None),
    ("Our school fundraiser was a {T} this year.", {"T": ["great success", "huge achievement", "record-breaking event"]}, None),
    ("Volunteering at the food bank taught me about {T}.", {"T": ["teamwork", "community service", "organising a roster"]}, None),
    ("The science fair projects impressed {T}.", {"T": ["all the judges", "every visitor", "the whole school"]}, None),
    ("Climate change affects {T}.", {"T": ["farming communities", "coastal towns", "the whole region", "our local rivers"]}, None),
    ("Public libraries offer free access to {T}.", {"T": ["books and quiet spaces", "learning resources", "after-school programmes"]}, None),
    ("Teamwork makes difficult {T} easier to complete.", {"T": ["projects", "assignments", "experiments"]}, None),
    ("The debating team won the {T}.", {"T": ["regional finals", "inter-school title", "the annual trophy"]}, None),
    ("Every student deserves a safe and supportive {T}.", {"T": ["classroom", "learning environment", "playground"]}, None),
    ("Music education develops {T}.", {"T": ["discipline as well as creativity", "confidence and focus", "listening skills"]}, None),
    ("A balanced diet and enough sleep improve {T}.", {"T": ["exam performance", "memory and mood", "attendance"]}, None),
    ("The new cycleway makes the trip to school {T}.", {"T": ["safer", "quicker and safer", "more enjoyable"]}, None),
    ("Writing by hand helps some learners {T}.", {"T": ["remember more effectively", "organise their ideas", "slow down and think"]}, None),
    ("Our kapa haka group performed at the {T}.", {"T": ["regional festival", "national competition", "school gala"]}, None),
    ("The composting scheme reduced our school's {T}.", {"T": ["waste by half", "rubbish collections", "landfill fees"]}, None),
    ("Interviewing our grandparents taught us about {T}.", {"T": ["local history", "old trades", "life in the sixties"]}, None),
    ("Documentaries bring {T} to life for young learners.", {"T": ["history", "science", "distant places"]}, None),
    ("The robotics club built a small {T} from spare parts.", {"T": ["rover", "sorting machine", "weather station"]}, None),
]

DAYS2 = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
         "Saturday", "Sunday"]

# corrupted regional families: grammar errors inside UK/US/NZ-flavoured text
REG_CORR = [
    ("uk", [
        ("The {P} {V3} the programme every {D}.", {"P": UK_PLACES2, "V3": ["hosts", "runs", "organises", "sponsors"], "D": DAYS2}, ("{V3}", lambda v: {"hosts": "host", "runs": "run", "organises": "organise", "sponsors": "sponsor"}[v])),
        ("Our team {V2} the colour festival last {T}.", {"V2": ["organised", "catalogued", "reviewed"], "T": ["month", "spring", "autumn", "June"]}, ("{V2}", lambda v: {"organised": "organising", "catalogued": "cataloguing", "reviewed": "reviewing"}[v])),
        ("She travelled to the {P} near the harbour.", {"P": UK_PLACES2}, ("travelled", lambda v: "travel")),
        ("We practised the {U} for the concert.", {"U": ["flute", "violin", "recital", "chorus"]}, ("practised", lambda v: "practise")),
        ("The licence for the {P} was renewed in May.", {"P": UK_PLACES2}, ("was", lambda v: "were")),
        ("They discussed the defence of the {P}.", {"P": UK_PLACES2}, ("discussed", lambda v: "discussed about")),
        ("The metre reading at the {P} has doubled.", {"P": UK_PLACES2}, ("has", lambda v: "have")),
        ("Our theatre group performs at the {P} every {D}.", {"P": UK_PLACES2, "D": DAYS2}, ("performs", lambda v: "perform")),
        ("The defence review listed the {P} last {T}.", {"P": UK_PLACES2, "T": ["month", "fortnight", "quarter"]}, ("listed", lambda v: "list")),
        ("Travellers gathered near the {P} for the parade.", {"P": UK_PLACES2}, ("gathered", lambda v: "gather")),
        ("The centre hosts the colour workshop on {D}.", {"P": UK_PLACES2[:6], "D": DAYS2}, ("hosts", lambda v: "host")),
    ]),
    ("us", [
        ("The {P} {V3} the program every {D}.", {"P": US_PLACES2, "V3": ["hosts", "runs", "organizes", "sponsors"], "D": DAYS2}, ("{V3}", lambda v: {"hosts": "host", "runs": "run", "organizes": "organize", "sponsors": "sponsor"}[v])),
        ("Our team {V2} the color festival last {T}.", {"V2": ["organized", "cataloged", "reviewed"], "T": ["month", "spring", "fall", "June"]}, ("{V2}", lambda v: {"organized": "organizing", "cataloged": "cataloging", "reviewed": "reviewing"}[v])),
        ("She traveled to the {P} downtown.", {"P": US_PLACES2}, ("traveled", lambda v: "travel")),
        ("The meter reading at the {P} has doubled.", {"P": US_PLACES2}, ("has", lambda v: "have")),
        ("We analyzed the labor data from the {P}.", {"P": US_PLACES2}, ("analyzed", lambda v: "analyze")),
        ("They organized the catalog for the {P}.", {"P": US_PLACES2}, ("organized", lambda v: "organize")),
        ("Our theater group performs at the {P} every {D}.", {"P": US_PLACES2, "D": DAYS2}, ("performs", lambda v: "perform")),
        ("The review listed the {P} last {T}.", {"P": US_PLACES2, "T": ["month", "quarter", "week"]}, ("listed", lambda v: "list")),
        ("Travelers gathered near the {P} for the parade.", {"P": US_PLACES2}, ("gathered", lambda v: "gather")),
        ("The center hosts the color workshop on {D}.", {"P": US_PLACES2[:6], "D": DAYS2}, ("hosts", lambda v: "host")),
    ]),
    ("nz", [
        ("The {P} {V3} the kai every {D}.", {"P": NZ_SPOTS, "V3": ["hosts", "runs", "serves", "prepares"], "D": DAYS2}, ("{V3}", lambda v: {"hosts": "host", "runs": "run", "serves": "serve", "prepares": "prepare"}[v])),
        ("Wiremu {V3} the tramping club photos.", {"V3": ["collects", "prints", "shares", "labels"]}, ("{V3}", lambda v: {"collects": "collect", "prints": "print", "shares": "share", "labels": "label"}[v])),
        ("The ute was parked near the {P}.", {"P": NZ_SPOTS}, ("was", lambda v: "were")),
        ("They went tramping near {P} last {T}.", {"P": NZ_SPOTS, "T": ["fortnight", "weekend", "January", "summer"]}, ("went", lambda v: "goes")),
        ("Aroha {V3} kai for the hui.", {"V3": ["prepares", "brings", "cooks", "shares"]}, ("{V3}", lambda v: {"prepares": "prepare", "brings": "bring", "cooks": "cook", "shares": "share"}[v])),
        ("The tamariki {V3} togs to the {P}.", {"V3": ["bring", "wear", "pack"], "P": NZ_SPOTS}, ("{V3}", lambda v: {"bring": "brings", "wear": "wears", "pack": "packs"}[v])),
        ("The kai at the {P} was shared with the manuhiri.", {"P": NZ_SPOTS}, ("was", lambda v: "were")),
        ("Our class {V3} kai for the shared lunch.", {"V3": ["brings", "prepares", "cooks", "packs"]}, ("{V3}", lambda v: {"brings": "bring", "prepares": "prepare", "cooks": "cook", "packs": "pack"}[v])),
        ("They parked the ute beside the {P} on {D}.", {"P": NZ_SPOTS, "D": DAYS2}, ("parked", lambda v: "park")),
        ("The tramping club meets at the {P} every {D}.", {"P": NZ_SPOTS, "D": DAYS2}, ("meets", lambda v: "meet")),
    ]),
]

# expanded clean essay frames (2-slot)
ESSAY_CLEAN2 = [
    ("The {SUBJ} debated {TOP} for weeks.", {"SUBJ": ["class", "council", "team", "committee", "kapa haka group", "robotics club", "student forum"], "TOP": ["the new uniform", "the canteen menu", "the camp venue", "the homework policy", "the recycling plan", "the sports day format"]}, None),
    ("Our {SUBJ} organised a {THING} for charity.", {"SUBJ": ["class", "year group", "student council", "drama club", "choir", "sports council"], "THING": ["bake sale", "book swap", "quiz night", "fun run", "talent show", "mufti day"]}, None),
    ("{WHO} presented {WHAT} at the assembly.", {"WHO": ["The monitors", "The librarians", "The house captains", "The prefects", "The science leaders", "The peer mediators"], "WHAT": ["the new rules", "the fundraiser results", "the reading challenge", "the recycling data", "the sports awards", "the safety plan"]}, None),
    ("The teacher asked us to {TASK} before Friday.", {"TASK": ["draft the essay", "revise the chapter", "practise the speech", "check the references", "complete the worksheet", "design the poster"]}, None),
    ("We measured {WHAT} for the science investigation.", {"WHAT": ["the soil temperature", "the water quality", "the plant growth", "the shadow length", "the reaction time", "the rainfall"], }, None),
    ("The study compared {A} and {B}.", {"A": ["urban schools", "coastal towns", "native birds", "reading habits", "sleep patterns", "bus routes"], "B": ["rural schools", "inland towns", "introduced species", "screen habits", "exam schedules", "cycleways"]}, None),
    ("Our experiment showed that {RESULT}.", {"RESULT": ["the plants grew faster", "the reaction slowed down", "the results were mixed", "the data was reliable", "the pattern repeated", "the trend reversed"]}, None),
    ("Many students find {SUBJ} challenging at first.", {"SUBJ": ["algebra", "essay writing", "chemistry", "new languages", "public speaking", "time management"]}, None),
    ("The principal thanked {WHO} for {WHAT}.", {"WHO": ["the volunteers", "the performers", "the sponsors", "the parents", "the coaches", "the caretakers"], "WHAT": ["their patience", "their generosity", "the long hours", "the kind support", "the steady effort"]}, None),
    ("Our class visited {WHERE} to learn about {WHAT}.", {"WHERE": ["the museum", "the marae", "the observatory", "the wetlands", "the recycling plant", "the art gallery"], "WHAT": ["local history", "star navigation", "native wildlife", "sustainable design", "conservation work", "traditional carving"]}, None),
]

# expanded professional clean frames (2-slot)
PROFF2 = [
    ("Please {V} the attached {N} before {D}.", {"V": ["review", "approve", "sign", "confirm", "circulate"], "N": ["contract", "report", "invoice", "proposal", "summary", "agenda"], "D": ["Friday", "Monday", "the meeting", "noon", "the deadline"]}, None),
    ("I am writing to {V} our meeting on {D}.", {"V": ["confirm", "reschedule", "follow up on", "prepare for"], "D": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]}, None),
    ("Our team {V2} the {N} last quarter.", {"V2": ["completed", "delivered", "audited", "reviewed", "finalised", "expanded"], "N": ["migration", "review", "rollout", "assessment", "survey", "training"]}, None),
    ("The {N} will be circulated {T}.", {"N": ["minutes", "summary", "budget", "timeline", "agenda", "handbook"], "T": ["tomorrow morning", "this afternoon", "on Monday", "by Friday", "after the meeting"]}, None),
    ("Thank you for your {N} regarding the {N2}.", {"N": ["patience", "feedback", "understanding", "prompt reply", "detailed response"], "N2": ["invoice", "booking", "application", "quotation", "shipment", "appointment"]}, None),
    ("The client {V2} the revised {N}.", {"V2": ["accepted", "approved", "reviewed", "signed", "queried", "endorsed"], "N": ["proposal", "budget", "timeline", "design", "contract", "scope"]}, None),
    ("Kindly {V} the {N} at your earliest convenience.", {"V": ["settle", "process", "verify", "forward", "archive"], "N": ["invoice", "payment", "order", "request", "claim", "refund"]}, None),
    ("Our records show a steady improvement in {T}.", {"T": ["attendance", "readability", "accuracy", "turnover", "engagement", "satisfaction"]}, None),
]

def extended_families():
    """Return list of (tag, frames) family tuples in fam-dict form."""
    out = []
    for tag, frames in (NUM_FAMILIES + DATE_FAMILIES + QUOTE_FAMILIES +
                        UKF + NZF2 + NEGF2 + CLEAN_EXTRA):
        out.append({"cat": None, "domain": "essay" if tag in ("uk", "nz", "us", "essay", "negation", "clean") else "professional",
                    "tag": tag, "frames": frames})
    # clean essay sentences, no family tag (domain-quota eligible)
    out.append({"cat": None, "domain": "essay", "tag": None, "frames": ESSAY_CLEAN + ESSAY_CLEAN2})
    # professional clean family, tag None so the professional quota can use it
    out.append({"cat": None, "domain": "professional", "tag": None, "frames": PROFF + PROFF2})
    # corrupted regional families (fill their own quotas)
    for tag, frames in REG_CORR:
        cat = frames[0][2][1](frames[0][2][0].format(**{k: v[0] for k, v in frames[0][1].items()})) and None
        out.append({"cat": "sva_3sg", "domain": "essay", "tag": tag, "frames": frames})
    return out

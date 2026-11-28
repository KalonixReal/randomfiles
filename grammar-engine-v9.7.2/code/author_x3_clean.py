#!/usr/bin/env python3
"""Author X3 clean rows: fresh natural NZ/UK register sentences.

All grammatically correct; GB spelling where natural; Māori loanwords as in
everyday NZ usage. One-shot: never checked against the engine before scoring.

Output: scripts/data_built/x3_clean.jsonl
"""
import json

CLEAN = [
    "We will arrange the marquee before the guests arrive.",
    "The queue at the bakery stretched past the door this morning.",
    "Her grey mare was shod by the farrier on Thursday.",
    "The tui called from the kōwhai outside the kitchen window.",
    "He practised the guitar until the neighbours complained.",
    "Our flight from Wellington was delayed by fog.",
    "The accountant filed the returns before the deadline.",
    "She colour-coded the spreadsheet by department.",
    "They bottled the plum sauce in the garage last summer.",
    "The wharf was busy with cray boats at dawn.",
    "Our teacher has taught at the kura for fifteen years.",
    "The mower left stripes across the front lawn.",
    "Both candidates spoke at the community meeting.",
    "We caught the ferry to Waiheke on the nine o'clock sailing.",
    "The dog barked at the postie and then went back to sleep.",
    "Her mother travelled through the centre of Dunedin on the bus.",
    "The committee has reached a unanimous decision on the plan.",
    "Everyone in the team has signed the card for Matiu.",
    "The chassis was badly rusted under the wheel arches.",
    "Linguistics is a demanding but rewarding field.",
    "Maths was my favourite subject in the sixth form.",
    "Seldom have we seen such a close final at the basin.",
    "It is I who am to blame for the mix-up.",
    "She sometimes seems distracted during the afternoon sessions.",
    "The police have cordoned off the area near the slip.",
    "What time does the last train leave for Picton?",
    "Which candidate did you vote for in the by-election?",
    "A couple of the boxes were damaged in transit.",
    "The set of keys was found in the letterbox.",
    "The number of applicants has doubled since last year.",
    "The majority of voters were under forty at the last census.",
    "The group of tourists was waiting at the gate.",
    "There is some loose change in the drawer by the door.",
    "The bolt came loose after the long vibration test.",
    "She was quite honest about the risks involved.",
    "I'll be quite candid: the margins are thin this quarter.",
    "The manager explained the process to us in plain language.",
    "Can you explain them in simple words for the class?",
    "The teacher explained the rule twice before we understood.",
    "It was agreed that the merger would proceed in stages.",
    "It was agreed by both parties at the mediation.",
    "The terms were agreed between the union and the council.",
    "Almost all the passengers were on board by six.",
    "Almost nobody was injured in the collision.",
    "Let's check in next week once the scaffolding is down.",
    "The results are due on this coming Friday.",
    "She was born in the last week of March.",
    "The loose change in the tin added up to forty dollars.",
    "Both essays argued the same point about the treaty text.",
    "Everyone in the village who was evacuated has returned home.",
    "Everything in the boxes was labelled and dated.",
    "Something in the engine was making a strange noise.",
    "The project kept its due date despite the outage.",
    "The committee published its findings last month.",
    "The cat licked its paws and went back to sleep.",
    "What does the machine do when the train leaves?",
    "How does the panel decide which option works best?",
    "The teachers in the senior syndicate met after school.",
    "The team have won every match this season so far.",
    "Her flight arrives at midnight on the red-eye service.",
    "We did the mistake analysis after the outage last year.",
    "She made a note of every fault the inspectors found.",
    "The revised budget was sent to the committee yesterday.",
    "I look forward to receiving your reply before Friday.",
    "The accommodation was basic but warm enough for the night.",
    "They received the forms on Friday and signed them Monday.",
    "Try not to lose your place in the queue at the counter.",
    "Please be quiet while the notices are being read.",
    "She asked why he was late again this morning.",
    "Tama and I are running the sausage sizzle on Saturday.",
    "The bus arrives at the depot at six sharp.",
    "It depends on the funding round in April.",
    "She is interested in the nursing course at the polytech.",
    "She ate an apple before the game on Saturday.",
    "We waited an hour outside the town hall.",
    "The storm had a big effect on the roof of the shed.",
    "You're welcome to stay for dinner if you like.",
    "We walked past the statue in the square.",
    "They're arriving on the late ferry tonight.",
    "Don't leave the gate open at dusk.",
    "We're going to the pools after school tomorrow.",
    "The dog's been outside for hours without a bark.",
    "It's a pity about the weather for the picnic.",
    "I am studying at the polytech this year.",
    "I think the kōrero went well today.",
    "Everyone in the choir was given a hymn book.",
    "Nobody on the committee has read the brief yet.",
    "He explained the problem to me twice before I understood.",
    "The box of parts was left in the shed overnight.",
    "This route is shorter than the highway in the mornings.",
    "That was the worst decision of the season, we all agreed.",
    "The player's boots were caked in mud after the game.",
    "My cousin's bike needs new tyres before the rail trail.",
    "Where does the trail end at the Kaitoke car park?",
    "What time does the movie start tonight at the Regent?",
    "Did you go to the open day in Hamilton last week?",
    "Did she take the minutes at the hui on Tuesday?",
    "He had eaten all the kai before we arrived.",
    "She has written a letter to the board about the uniforms.",
    "The principal has approved the new timetable for term three.",
    "The players train every Tuesday morning before work.",
    "The children were collected at the gate by the teacher aides.",
    "There are several stalls at the market this weekend.",
    "The warehouse was locked over the holidays.",
]

rows = []
seen = set()
for t in CLEAN:
    if t in seen:
        continue
    seen.add(t)
    rows.append({"text": t, "edits": [], "cats": ["clean"],
                 "origin": "authored-natural-holdout", "group": "X3"})

out = "/home/z/my-project/scripts/data_built/x3_clean.jsonl"
with open(out, "w") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"x3_clean.jsonl: {len(rows)} clean rows")

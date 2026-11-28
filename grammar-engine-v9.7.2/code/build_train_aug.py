#!/usr/bin/env python3
"""Build training augmentations for tagger v3:

1. glm_errors.jsonl (bad, good)  -> training rows via corrupt.diff_edits
2. glm_clean_valid.jsonl          -> hard-negative rows (edits=[])
3. authored U2 clean sentences    -> hard-negative rows (edits=[])
Output: scripts/data_built/train_aug.jsonl
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corrupt as C

HERE = os.path.dirname(os.path.abspath(__file__))
DISTILL = "/home/z/my-project/work/distill"

U2 = [
    # fresh authored natural clean (training hard negatives; NOT eval sets)
    "The batch job runs overnight and emails the report at six.",
    "Their team are heading up the new rollout next month.",
    "A number of tickets have been raised about the login page.",
    "The number of outages has fallen since the last release.",
    "We could hardly believe how quickly the tide turned.",
    "Never before had the region seen such a wet July.",
    "The data are reassuring, on the whole, for the sector.",
    "Physics was my worst subject at school, sadly.",
    "Each of the reports is signed off by the auditor.",
    "Either of the venues would suit the celebration.",
    "Neither of the drafts is ready for the client yet.",
    "The kōwhai trees along the fence were buzzing with bees.",
    "Grab your togs and goggles; the pool is open till eight.",
    "The boat ramp at Tutukākā was packed by dawn.",
    "Mum dropped us at the marae before the powhiri started.",
    "He reckons the snapper were biting off the rocks.",
    "The bach needs a new coat of paint before Labour Weekend.",
    "We will organise the colours with the printer this week.",
    "The centre of town was shut for the parade.",
    "Ask at the i-SITE about the track to the falls.",
    "The variable kPoints stores the node indices.",
    "The config maps each route to a handler function.",
    "Their CI pipeline deploys to staging on every merge.",
    "The cache invalidates whenever an order is placed.",
    "The renderer batches the draw calls per frame.",
    "Wi-Fi drops out in the far corner of the office.",
    "The README explains how to run the container.",
    "Set the user agent to Mozilla/5.0 before retrying.",
    "Version 3.2.1 fixed a tokenizer regression.",
    "The proxy rewrites the Location header before forwarding.",
    "Kind regards, and thanks again for the quick turnaround.",
    "Please find the revised draft attached for your review.",
    "The committee have asked for a costing before June.",
    "Our suppliers have moved to a larger facility.",
    "It was agreed that the works would finish before winter.",
    "The auditor recommended that the ledger be reconciled monthly.",
    "Seldom does a first novel win both prizes in one year.",
    "Rarely have the volunteers asked for anything in return.",
    "Not only did the crew finish early, but they also stayed within budget.",
    "Scarcely had the gates opened when the queue formed.",
    "It is she who signs off the roster each Friday.",
    "It was they who raised the alarm that night.",
    "Which candidate did the panel interview last week?",
    "What time does the last ferry leave on Sundays?",
    "Where does the shuttle stop at the airport?",
    "How does the scheduler handle overlapping jobs?",
    "Who did the referee speak to after the final whistle?",
    "A unanimous decision was reached after an hour.",
    "A unique opportunity arose during the merger talks.",
    "The hypothesis was tested across three independent trials.",
    "Linguistics attracts students from every faculty.",
    "The status bar shows the current build status.",
    "The chassis was inspected after the rally.",
    "The bus is late again this morning.",
    "The minutes from the last meeting have been circulated.",
    "Sometimes the simplest fix works best.",
    "The stairs to the loft are steep and narrow.",
    "These scissors are too blunt for the silk.",
    "Your trousers are ready for collection after five.",
    "The news from the coast is better today.",
    "Measles is making a comeback in several regions.",
    "Maths is taught in mixed-ability classes this year.",
    "Two thirds of the crop was lost to the frost.",
    "The invoice totals $1,234.56 including GST.",
    "Sales rose by 14.5% over the previous quarter.",
    "The workshop runs from 21 February to 4 March 2026.",
    "Her birthday is on the 1st of December, same as her brother.",
    "He called it \"a triumph of style over substance\" in his review.",
    "\"Hand me the spanner,\" he muttered from under the car.",
    "The referee shouted, \"Play on!\", and the crowd roared.",
    "Whanganui is famous for its river and its Victorian streets.",
    "Anahera and Tāmati were married at Ōhope Beach last summer.",
    "Tāmaki Makaurau has grown faster than any other city.",
    "Prime Minister Jacinda Ardern spoke at the memorial.",
    "Te Wharekura o Rotorua hosted the regional festival.",
    "The pohutukawa along the coast were ablaze with blossom.",
    "The kaimoana gathered at low tide fed the whole marae.",
    "Our neighbours have just built a lovely new veranda.",
    "She practises the piano every evening after training.",
    "I'll be back in a fortnight, after the programme wraps.",
    "Whilst the weather holds, we might walk the track.",
    "We had a brilliant feed of kai after the service.",
    "Kia ora, welcome along to tonight's session.",
    "The tui were singing in the gums at first light.",
    "He caught a fat kahawai off the rocks near Raglan.",
    "After tramping the crossing, our feet were wrecked.",
    "Aroha brings her famous pavlova to every shared lunch.",
    "The working group have circulated their recommendations.",
    "Our staff have raised concerns about the new roster.",
    "The board has approved the capital expenditure.",
    "Both parties have accepted the terms of the settlement.",
    "The panel were divided on the final ranking.",
    "My colleagues and I will attend the Wellington conference.",
    "Neither answer is entirely satisfactory.",
    "Either the plumber or the electrician is free on Thursday.",
    "She is one of those managers who listen carefully.",
    "Who did you give the tickets to, in the end?",
    "To whom should we address the complaint?",
    "The team that wins tonight goes straight to the final.",
    "All being well, the shipment leaves on the morning tide.",
    "Having finished the report, she left early.",
    "We would rather walk than wait for the next bus.",
    "If I were you, I would take the earlier train.",
    "Were it not for the storm, we would have sailed at noon.",
    "Should you have any questions, please contact the office.",
    "Under no circumstances are the keys to be left in the ute.",
    "On the hill stood a small chapel built by the settlers.",
    "The parcel weighs more than the scales allow.",
    "That is the most beautiful sunrise I have ever seen.",
    "The more we practise, the easier the routine becomes.",
    "This model is by far the most reliable of the three.",
    "The old ferry is being converted into a restaurant.",
    "Where are my reading glasses when I need them?",
    "The entrées arrived before the drinks, oddly.",
    "The proceeds go to the mountain rescue trust.",
    "Gymnastics was dropped from the programme for lack of numbers.",
]

rows = []

# 1. GLM error pairs -> training rows
n_err = 0
with open(os.path.join(DISTILL, "glm_errors.jsonl")) as f:
    for line in f:
        if not line.strip():
            continue
        r = json.loads(line)
        try:
            edits = C.diff_edits(r["bad"], r["good"])
        except Exception:
            continue
        if not edits:
            continue
        dicts = [{"start": s, "end": e, "orig": r["bad"][s:e], "rep": rep, "type": "glm"}
                 for (s, e, rep) in edits]
        rows.append({"text": r["bad"], "clean": r["good"], "edits": dicts,
                     "origin": "glm-error", "group": "G", "domain": r.get("domain")})
        n_err += 1

# 2. GLM clean -> hard negatives
n_clean = 0
with open(os.path.join(DISTILL, "glm_clean_valid.jsonl")) as f:
    for line in f:
        if not line.strip():
            continue
        r = json.loads(line)
        rows.append({"text": r["text"], "clean": r["text"], "edits": [],
                     "origin": "glm-clean-neg", "group": "G", "domain": r.get("domain")})
        n_clean += 1

# 3. authored U2 clean -> hard negatives
for s in U2:
    rows.append({"text": s, "clean": s, "edits": [],
                 "origin": "authored-neg", "group": "U2"})

out = os.path.join(HERE, "data_built", "train_aug.jsonl")
with open(out, "w") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"train_aug.jsonl: {len(rows)} rows (glm-errors={n_err}, glm-clean={n_clean}, u2={len(U2)})")

# 4. gold maintenance: the 'Ive' row in test.jsonl is a genuine gold error
#    ("Ive had in ages" -> "I've"): the engine was right, the label was wrong.
for p in [os.path.join(HERE, "data_built", "test.jsonl"),
          "/home/z/my-project/download/model/data/test.jsonl"]:
    if not os.path.exists(p):
        continue
    lines = open(p).read().split("\n")
    fixed = 0
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        r = json.loads(line)
        if r["text"] == "them sausages were the best Ive had in ages." and not r["edits"]:
            start = r["text"].find("Ive")
            r["edits"] = [{"start": start, "end": start + 3, "orig": "Ive", "rep": "I've",
                           "type": "contraction"}]
            lines[i] = json.dumps(r, ensure_ascii=False)
            fixed += 1
    if fixed:
        open(p, "w").write("\n".join(lines))
        print(f"gold fixed in {p}: {fixed} row(s)")

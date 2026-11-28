#!/usr/bin/env python3
"""Author X3 error rows (fresh one-shot set for the v9.7.0 measurement).

Protocol identical to X2: (wrong, right, tag) tuples converted to gold edits
with corrupt.diff_edits. Sentences are NEW surface forms; no rule in the
engine was written against these specific sentences (lexicons were built from
the X2 diagnosis only). This file is executed ONCE for the final report —
X3 is not used for any tuning.

Output: scripts/data_built/x3_errors.jsonl
"""
import json
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corrupt as C

E = [
    # subject-verb agreement
    ("The principal have approved the new timetable.", "The principal has approved the new timetable.", "have/has"),
    ("The players trains every Tuesday morning.", "The players train every Tuesday morning.", "trains/train"),
    ("The children was collected at the gate by the aides.", "The children were collected at the gate by the aides.", "was/were"),
    ("There is several stalls at the market this weekend.", "There are several stalls at the market this weekend.", "is/are"),
    ("The warehouse were locked over the holidays.", "The warehouse was locked over the holidays.", "were/was"),
    # verb forms / participles
    ("She has wrote a letter to the board.", "She has written a letter to the board.", "wrote/written"),
    ("The parcel was send to the old address.", "The parcel was sent to the old address.", "send/sent"),
    ("Did you went to the open day in Hamilton?", "Did you go to the open day in Hamilton?", "went/go"),
    ("Did she took the minutes at the hui?", "Did she take the minutes at the hui?", "took/take"),
    ("He had ate all the kai before we arrived.", "He had eaten all the kai before we arrived.", "ate/eaten"),
    # do-support 3sg
    ("Where does the trail ends?", "Where does the trail end?", "ends/end"),
    ("What time does the movie starts tonight?", "What time does the movie start tonight?", "starts/start"),
    # possessive apostrophe
    ("My cousins bike needs new tyres.", "My cousin's bike needs new tyres.", "cousins/cousin's"),
    ("The dentists chair reclined fully.", "The dentist's chair reclined fully.", "dentists/dentist's"),
    ("The cats been indoors since lunch.", "The cat's been indoors since lunch.", "cats/cat's"),
    # its / it's
    ("The team will call when its finished.", "The team will call when it's finished.", "its/it's"),
    ("Its a pity about the weather.", "It's a pity about the weather.", "Its/It's"),
    # double comparatives
    ("This route is more shorter than the highway.", "This route is shorter than the highway.", "more shorter"),
    ("That was the most worst decision of the season.", "That was the worst decision of the season.", "most worst"),
    # indefinite singular subjects
    ("Everyone in the choir were given a hymn book.", "Everyone in the choir was given a hymn book.", "were/was"),
    ("Nobody on the committee have read the brief.", "Nobody on the committee has read the brief.", "have/has"),
    # head-of-PP agreement
    ("The box of parts were left in the shed.", "The box of parts was left in the shed.", "were/was"),
    # copula + agree
    ("I am agree with the recommendation.", "I agree with the recommendation.", "am agree"),
    # collocations
    ("We did a mistake with the catering order.", "We made a mistake with the catering order.", "did/made"),
    ("The manager explained us the new rostering process.", "The manager explained to us the new rostering process.", "explained us"),
    # preposition + next/last
    ("The inspector will visit on next Tuesday.", "The inspector will visit next Tuesday.", "on next"),
    ("Are you free on tomorrow for the site walk?", "Are you free tomorrow for the site walk?", "on tomorrow"),
    # the both / almost people
    ("The both essays argued the same point.", "Both essays argued the same point.", "The both"),
    ("Almost students failed the first quiz.", "Almost everyone failed the first quiz.", "almost people"),
    # loose / lose
    ("Try not to loose your place in the queue.", "Try not to lose your place in the queue.", "loose/lose"),
    # quite / quiet
    ("Please be quite while the notices are read.", "Please be quiet while the notices are read.", "quite/quiet"),
    # indirect question word order
    ("She asked why was he late this morning.", "She asked why he was late this morning.", "inversion"),
    # pronoun subject
    ("Me and Tama are running the sausage sizzle.", "Tama and I are running the sausage sizzle.", "Me and"),
    # prepositions
    ("The bus arrives to the depot at six.", "The bus arrives at the depot at six.", "to/at"),
    ("It depends of the funding round.", "It depends on the funding round.", "of/on"),
    ("She is interested about the nursing course.", "She is interested in the nursing course.", "about/in"),
    # articles
    ("She ate a apple before the game.", "She ate an apple before the game.", "a/an"),
    ("We waited for a hour outside the hall.", "We waited for an hour outside the hall.", "a/an"),
    # homophones / confusables
    ("The storm had a big affect on the roof.", "The storm had a big effect on the roof.", "affect/effect"),
    ("Your welcome to stay for dinner.", "You're welcome to stay for dinner.", "Your/You're"),
    ("We walked passed the statue in the square.", "We walked past the statue in the square.", "passed/past"),
    ("Their arriving on the red-eye flight.", "They're arriving on the red-eye flight.", "Their/They're"),
    # contractions
    ("Dont leave the gate open at dusk.", "Don't leave the gate open at dusk.", "Dont/Don't"),
    ("Were going to the pools after school.", "We're going to the pools after school.", "Were/We're"),
    # spelling
    ("The accomodation was basic but warm.", "The accommodation was basic but warm.", "accomodation"),
    ("They recieved the forms on Friday.", "They received the forms on Friday.", "recieved"),
    ("He gave me several advices about the wiring.", "He gave me several pieces of advice about the wiring.", "advices"),
    # modal + of
    ("You should of booked earlier for the ferry.", "You should have booked earlier for the ferry.", "should of"),
    # progressive
    ("I am study at the polytech this year.", "I am studying at the polytech this year.", "study/studying"),
    # capital i
    ("i think the kōrero went well today.", "I think the kōrero went well today.", "i/I"),
    # wh questions missing auxiliary
    ("What time the shop opens on Saturdays?", "What time does the shop open on Saturdays?", "missing do"),
]

rows = []
skipped = 0
for bad, good, cat in E:
    if good is None:
        skipped += 1
        continue
    edits = C.diff_edits(bad, good)
    dicts = [{"start": s, "end": e, "orig": bad[s:e], "rep": r, "type": "authored"}
             for (s, e, r) in edits]
    rows.append({"text": bad, "clean": good, "edits": dicts, "cats": ["error"],
                 "origin": "authored-error", "group": "X3"})

out = "/home/z/my-project/scripts/data_built/x3_errors.jsonl"
with open(out, "w") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"x3_errors.jsonl: {len(rows)} error rows ({skipped} skipped)")

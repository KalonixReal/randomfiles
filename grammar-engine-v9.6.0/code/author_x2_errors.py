#!/usr/bin/env python3
"""Author X2 error rows (with exact gold edits) for the final one-shot test.

Paired with x2_clean.jsonl (96 clean). Same register breadth: NZ/UK,
workplace, tech, school, names, numbers, quotes. Errors are the kind both
our engine and GLM plausibly fix: SVA, verb forms, apostrophes, spelling,
articles, prepositions, confusables, word order, punctuation.

Output: scripts/data_built/x2_errors.jsonl
"""
import json

E = [
    # subject-verb agreement
    ("The list of items are on the desk.", "The list of items is on the desk.", "is/are"),
    ("She don't know about the meeting tomorrow.", "She doesn't know about the meeting tomorrow.", "dont/doesnt"),
    ("The children was excited about the trip.", "The children were excited about the trip.", "was/were"),
    ("Our team have won every match this season.", "Our team has won every match this season.", "have/has"),
    ("The students is arriving at eight sharp.", "The students are arriving at eight sharp.", "is/are"),
    ("One of the boys have forgotten his boots.", "One of the boys has forgotten his boots.", "have/has"),
    ("Everyone in the whanau were at the marae.", "Everyone in the whanau was at the marae.", "were/was"),
    ("The womens team is training tonight.", "The women's team is training tonight.", "womens"),
    ("There is three options on the table.", "There are three options on the table.", "is/are"),
    # verb forms
    ("I seen the results yesterday afternoon.", "I saw the results yesterday afternoon.", "seen/saw"),
    ("She had went home before the rain started.", "She had gone home before the rain started.", "went/gone"),
    ("They was driving to Taupo when the tyre blew.", "They were driving to Taupo when the tyre blew.", "was/were"),
    ("He should of checked the schedule first.", "He should have checked the schedule first.", "of/have"),
    ("We was told that the trip might be cancelled.", "We were told that the trip might be cancelled.", "was/were"),
    ("The budget was send to the committee.", "The budget was sent to the committee.", "send/sent"),
    ("I am work on the caching layer this week.", "I am working on the caching layer this week.", "work/working"),
    ("She have finished her homework already.", "She has finished her homework already.", "have/has"),
    ("Did you seen the size of that kahawai?", "Did you see the size of that kahawai?", "seen/see"),
    # apostrophes / contractions
    ("The teachers desk was covered in marking.", "The teacher's desk was covered in marking.", "teachers"),
    ("Ive had better coffee, to be honest.", "I've had better coffee, to be honest.", "Ive"),
    ("Theyre arriving on the night ferry.", "They're arriving on the night ferry.", "Theyre"),
    ("Dont forget the sunblock for the beach.", "Don't forget the sunblock for the beach.", "Dont"),
    ("My brothers car is in the garage.", "My brother's car is in the garage.", "brothers"),
    ("It's raining and the dogs been outside for hours.", "It's raining and the dog's been outside for hours.", "dogs"),
    ("We could of won that game, honestly.", "We could have won that game, honestly.", "of/have"),
    # spelling
    ("I recieved the invoice on Tuesday.", "I received the invoice on Tuesday.", "recieved"),
    ("Please seperate the recycling from the rubbish.", "Please separate the recycling from the rubbish.", "seperate"),
    ("That was definately the best pie in town.", "That was definitely the best pie in town.", "definately"),
    ("The occurence was reported to the office.", "The occurrence was reported to the office.", "occurence"),
    ("We waited untill the tide turned.", "We waited until the tide turned.", "untill"),
    ("She grabbed teh keys and left.", "She grabbed the keys and left.", "teh"),
    ("Their going to the beach tomorrow.", "They're going to the beach tomorrow.", "Their/Theyre"),
    # articles / determiners
    ("He wants a orange juice with his breakfast.", "He wants an orange juice with his breakfast.", "a/an"),
    ("We booked an hotel near the stadium.", "We booked a hotel near the stadium.", "an/a"),
    ("She is an university student in Dunedin.", "She is a university student in Dunedin.", "an/a"),
    ("That was a hour well spent.", "That was an hour well spent.", "a/an"),
    # prepositions
    ("They arrived in the airport two hours early.", "They arrived at the airport two hours early.", "in/at"),
    ("She is keen in joining the netball club.", "She is keen on joining the netball club.", "in/on"),
    ("The success depends of the weather.", "The success depends on the weather.", "of/on"),
    ("He is married with a nurse from Gisborne.", "He is married to a nurse from Gisborne.", "with/to"),
    ("We arrived to the marae before dawn.", "We arrived at the marae before dawn.", "to/at"),
    # confusables
    ("Her notes are more tidy then mine.", "Her notes are more tidy than mine.", "then/than"),
    ("Its going to be a long winter.", "It's going to be a long winter.", "Its/It's"),
    ("The dog wagged its tail; its been a good day.", "The dog wagged its tail; it's been a good day.", "its/it's2"),
    ("Loose the attitude and listen up.", "Lose the attitude and listen up.", "Loose/Lose"),
    ("The medicine will affect your driving, be careful.", "The medicine will affect your driving, be careful.", None),
    ("The weather had a big affect on attendance.", "The weather had a big effect on attendance.", "affect/effect"),
    ("I could of sworn it was Friday.", "I could have sworn it was Friday.", "of/have2"),
    ("Your late again this morning.", "You're late again this morning.", "Your/You're"),
    ("Their is a problem with the heater.", "There is a problem with the heater.", "Their/There"),
    ("The principal asked everyone to be quite during assembly.", "The principal asked everyone to be quiet during assembly.", "quite/quiet"),
    # word order / questions
    ("Where the students is going after the trip?", "Where are the students going after the trip?", "wh-order"),
    ("Why was the shipment delayed again?", None, None),  # correct - skip
    ("I am not sure why was the meeting cancelled.", "I am not sure why the meeting was cancelled.", "embedded"),
    ("What time does the last bus leaves?", "What time does the last bus leave?", "leaves/leave"),
    # comparatives / quantity
    ("There were less people at the game this week.", "There were fewer people at the game this week.", "less/fewer"),
    ("This is the most best option we have.", "This is the best option we have.", "most best"),
    ("The more louder the crowd got, the worse they played.", "The louder the crowd got, the worse they played.", "more louder"),
    # pronouns
    ("Me and Dave are painting the fence on Saturday.", "Dave and I are painting the fence on Saturday.", "Me and Dave"),
    ("Her and her sister are arriving on Friday.", "She and her sister are arriving on Friday.", "Her and her"),
    ("The tickets are for you and I.", "The tickets are for you and me.", "you and I"),
    ("Between you and I, the plan needs work.", "Between you and me, the plan needs work.", "you and I2"),
    # punctuation / capitalisation
    ("she dont know about the surprise party yet.", "She doesn't know about the surprise party yet.", "cap+dont"),
    ("i will send the report when its finished", "I will send the report when it's finished", "cap+its"),
    ("The bus leaves at 6:45 sharp.", None, None),  # correct - skip
    # plural / mass nouns
    ("We bought new furnitures for the lounge.", "We bought new furniture for the lounge.", "furnitures"),
    ("She gave me some good advices.", "She gave me some good advice.", "advices"),
    ("The team needs more informations.", "The team needs more information.", "informations"),
    # misc grammar
    ("He is more taller than his brother.", "He is taller than his brother.", "more taller"),
    ("The both teams played well in the wet.", "Both teams played well in the wet.", "the both"),
    ("I am agree with the proposal.", "I agree with the proposal.", "am agree"),
    ("She explained me the problem twice.", "She explained the problem to me twice.", "explained me"),
    ("We discussed about the budget for an hour.", "We discussed the budget for an hour.", "discussed about"),
    ("The report is due on next Monday.", "The report is due next Monday.", "on next"),
    ("He did a mistake in the calculation.", "He made a mistake in the calculation.", "did/made"),
    ("Almost people in the office were off sick.", "Almost everyone in the office was off sick.", None),
]

rows = []
skipped = 0
for bad, good, cat in E:
    if good is None:
        skipped += 1
        continue
    # compute gold edits via token diff (same tooling as training data)
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import corrupt as C
    edits = C.diff_edits(bad, good)
    dicts = [{"start": s, "end": e, "orig": bad[s:e], "rep": r, "type": "authored"}
             for (s, e, r) in edits]
    rows.append({"text": bad, "clean": good, "edits": dicts, "cats": ["error"],
                 "origin": "authored-error", "group": "X2"})

out = "/home/z/my-project/scripts/data_built/x2_errors.jsonl"
with open(out, "w") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"x2_errors.jsonl: {len(rows)} error rows ({skipped} skipped as duplicates/correct)")

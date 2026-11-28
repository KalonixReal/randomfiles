# -*- coding: utf-8 -*-
"""Author the FRESH comparison set (v9.7.1 vs v9.7.0 vs GLM).
Held-out reporting set: emails + essays with real errors, and clean NZ/UK
prose (including wh-subject clauses, GB collectives, NZ spellings, Māori
loanwords). NOT used for any gate or rule tuning.
Gold edits are derived from (wrong, correct) pairs and verified.
Output: data_built/fresh.jsonl — {"text", "edits":[{start,end,rep}], "genre"}
"""

def diff_edit(wrong, correct):
    """single-edit diff via common prefix/suffix; returns (start, end, rep)"""
    # strip common prefix
    p = 0
    while p < len(wrong) and p < len(correct) and wrong[p] == correct[p]:
        p += 1
    # strip common suffix (after prefix)
    s = 0
    while (s < len(wrong) - p and s < len(correct) - p
           and wrong[len(wrong) - 1 - s] == correct[len(correct) - 1 - s]):
        s += 1
    start, end = p, len(wrong) - s
    rep = correct[p:len(correct) - s]
    # verify single application reproduces the correct sentence
    applied = wrong[:start] + rep + wrong[end:]
    assert applied == correct, (wrong, correct, applied)
    return {"start": start, "end": end, "rep": rep}

EMAILS = [
    ("Please find the report attach to this email.", "Please find the report attached to this email."),
    ("The meeting was cancelled because the manager were sick.", "The meeting was cancelled because the manager was sick."),
    ("I look forward to hear from you soon.", "I look forward to hearing from you soon."),
    ("We have discuss the proposal with the team.", "We have discussed the proposal with the team."),
    ("The client want us to finish the project by June.", "The client wants us to finish the project by June."),
    ("Thank you for your patients during the outage.", "Thank you for your patience during the outage."),
    ("Please revert back to me if you have any questions.", "Please reply to me if you have any questions."),
    ("The attachments is the signed contract.", "The attachments are the signed contract."),
    ("We regret to inform you that your application has been decline.", "We regret to inform you that your application has been declined."),
    ("Kindly confirm if you have receive the parcel.", "Kindly confirm if you have received the parcel."),
    ("Both proposal were rejected by the board.", "Both proposals were rejected by the board."),
    ("He dont have access to the shared drive.", "He doesn't have access to the shared drive."),
    ("The invoice need to be paid before the end of the month.", "The invoice needs to be paid before the end of the month."),
    ("We are currently experience some issues with the payment gateway.", "We are currently experiencing some issues with the payment gateway."),
    ("Please note that the office will be close on Monday.", "Please note that the office will be closed on Monday."),
    ("Their has been a delay in shipping your order.", "There has been a delay in shipping your order."),
    ("I am interesting in the junior developer role.", "I am interested in the junior developer role."),
    ("The report which was submitted yesterday have several errors.", "The report which was submitted yesterday has several errors."),
    ("She is responsible of managing the accounts.", "She is responsible for managing the accounts."),
    ("The training session will be hold in the boardroom.", "The training session will be held in the boardroom."),
    ("We apologies for the inconvenience caused.", "We apologise for the inconvenience caused."),
    ("As per our conversation, I have send the revised drawings.", "As per our conversation, I have sent the revised drawings."),
    ("This is to inform you that the warranty on your machine expire next month.", "This is to inform you that the warranty on your machine expires next month."),
    ("Could you check the data and let me know if their accurate?", "Could you check the data and let me know if they're accurate?"),
    ("The supplier have confirm the delivery date.", "The supplier has confirmed the delivery date."),
]

ESSAYS = [
    ("The main reason of the failure was poor planning.", "The main reason for the failure was poor planning."),
    ("In conclusion, the evidence suggest that the policy works.", "In conclusion, the evidence suggests that the policy works."),
    ("Students which study regularly perform better in exams.", "Students who study regularly perform better in exams."),
    ("Each of the students have submitted their essay.", "Each of the students has submitted their essay."),
    ("The number of participants were higher than expected.", "The number of participants was higher than expected."),
    ("Pollution effects the health of local residents.", "Pollution affects the health of local residents."),
    ("The novel was wrote by a young author from Dunedin.", "The novel was written by a young author from Dunedin."),
    ("There is many factors that contribute to climate change.", "There are many factors that contribute to climate change."),
    ("The experiment resulted in a significant improving in results.", "The experiment resulted in a significant improvement in results."),
    ("Childrens spend too much time on screens.", "Children spend too much time on screens."),
    ("She explained me the problem in detail.", "She explained the problem to me in detail."),
    ("Compared from last year, sales have doubled.", "Compared with last year, sales have doubled."),
    ("It is more better to prevent illness than to cure it.", "It is better to prevent illness than to cure it."),
    ("The books was borrowed from the library.", "The books were borrowed from the library."),
    ("He did not went to university because of the cost.", "He did not go to university because of the cost."),
    ("The results of the survey was surprising.", "The results of the survey were surprising."),
    ("The information were not available at the time.", "The information was not available at the time."),
    ("The students was given a second chance to submit.", "The students were given a second chance to submit."),
    ("Each of the players were given a medal.", "Each of the players was given a medal."),
    ("She could of finished the essay earlier.", "She could have finished the essay earlier."),
    ("The weather in Auckland are unpredictable.", "The weather in Auckland is unpredictable."),
    ("My favourite subject are history.", "My favourite subject is history."),
    ("The essay discuss two main causes of the war.", "The essay discusses two main causes of the war."),
    ("Everyone in the class have finished the assignment.", "Everyone in the class has finished the assignment."),
    ("People is living longer than ever before.", "People are living longer than ever before."),
]

CLEAN = [
    # wh-subject clause family (the reported FP family)
    "Why the process was redesigned remains commercially sensitive.",
    "What the committee recommended surprised the entire board.",
    "How the team qualified for the finals still puzzles the commentators.",
    "Whether the treaty applies remains unsettled.",
    "Where the kōrero took place is now a heritage site.",
    "What remains unclear is who signed the form.",
    "Why she resigned remains a matter of speculation.",
    "How it works is explained in the user manual.",
    "Why the ferry was cancelled is still unclear.",
    "How much the ticket costs depends on the season.",
    "What she said made sense to everyone in the room.",
    "When the gallery closes depends on staffing.",
    # GB collectives (legitimately plural in NZ/UK prose)
    "The committee were divided over the proposal.",
    "The government are considering changes to the law.",
    "The staff have raised concerns about the roster.",
    "Our team is focused on delivering the release on time.",
    # NZ/UK spellings
    "We organise the annual fundraiser in the community hall.",
    "The colour scheme was chosen by the students.",
    "She travelled around the South Island last summer.",
    "They realised the project was over budget.",
    "The programme starts in February.",
    "The centre is open on weekends.",
    "The neighbours organised a working bee at the marae.",
    "He enrolled in a maths course at the polytechnic.",
    "The theatre was full on opening night.",
    "She practises the piano every evening.",
    # Māori loanwords in running prose
    "The whānau gathered at the marae for the tangi.",
    "The tamariki performed a haka for the visitors.",
    "He gave a speech about manaakitanga at the graduation.",
    "Our rūnanga meets on the first Monday of each month.",
    "The tōtara trees along the boundary were protected.",
    "It's been raining since Tuesday in Ōhope.",
    "Everyone who attended the hui enjoyed the kai.",
    # correct direct questions and embedded questions
    "Why is the process failing so often this quarter?",
    "Could you tell me where the station is?",
    "I don't know why the process keeps failing.",
    "Do you know when the results are announced?",
    "What time does the ferry depart on Sundays?",
    # passives, agreement traps that must stay quiet
    "The contract was reviewed by our solicitors last week.",
    "Data from the sensors were collected every hour.",
    "None of the equipment was damaged in the storm.",
    "A number of residents have complained about the noise.",
    "The bus leaves at seven every morning.",
    "Maths is my favourite subject.",
    "The news from Christchurch was encouraging.",
    "The status of the application is still unknown.",
    "The process is working as expected.",
    "We walked past the statue on our way to school.",
    "He passed the exam despite the disruption.",
    "Its handle was broken, so we replaced it.",
    "The dog licked its paws and settled down for the night.",
    "That was quite a performance from the All Blacks.",
    "Be quiet while the karakia is being said.",
    "She is quite good at netball.",
    "He explained the problem to us clearly.",
    "The committee has published its findings.",
    "Each student has submitted their essay on time.",
    "The evidence suggests that the policy works.",
    "A series of workshops was held in Ōtepoti.",
    "Please find the report attached to this email.",
    "I look forward to hearing from you.",
    "Thank you for your patience during the outage.",
    "We will be in touch once the audit is finished.",
    "The children were excited about the trip to the museum.",
    "The plays of Shakespeare are still performed worldwide.",
]

rows = []
for wrong, correct in EMAILS:
    rows.append({"text": wrong, "edits": [diff_edit(wrong, correct)], "genre": "email"})
for wrong, correct in ESSAYS:
    rows.append({"text": wrong, "edits": [diff_edit(wrong, correct)], "genre": "essay"})
for t in CLEAN:
    rows.append({"text": t, "edits": [], "genre": "clean-prose"})

import json, os
dst = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_built", "fresh.jsonl")
with open(dst, "w") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
errs = sum(1 for r in rows if r["edits"])
print(f"fresh.jsonl written: {len(rows)} rows ({errs} error: {len(EMAILS)} email + {len(ESSAYS)} essay; {len(rows)-errs} clean)")
for r in rows[:3] + rows[26:29]:
    print(" ", json.dumps(r, ensure_ascii=False)[:110])

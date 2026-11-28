// Adversarial FP stress round 2: correct sentences sitting exactly in the
// v9.7.2 rule families' strike zones. None of these may be flagged.
const fs = require('fs');
const path = require('path');
const data = fs.readFileSync(path.join(__dirname, 'export_out/engine94_data.json'), 'utf8');
const rules = fs.readFileSync(path.join(__dirname, 'export_out/engine94_rules.json'), 'utf8');
const weights = fs.readFileSync(path.join(__dirname, 'export_out/engine94_weights.b64'), 'utf8').trim();
let code = fs.readFileSync(path.join(__dirname, 'engine94.js'), 'utf8');
const dataObj = JSON.parse(data);
dataObj.threshold = 1.0;
code = 'const W94_DATA=' + JSON.stringify(dataObj) + ';\nconst W94_RULES=' + rules + ';\nconst W94_WEIGHTS_B64=' + JSON.stringify(weights) + ';\n' + code;
code = code.replace(/self\.onmessage[\s\S]*$/m, '');
code += "\n;globalThis.W94=W94;";
globalThis.atob = s => Buffer.from(s, 'base64').toString('binary');
eval(code);

const T = [
  // sva_sing_lex: noun compounds and correct 3sg verbs
  "The essay discusses two main causes of the war.",
  "The report describes the incident in detail.",
  "The machine expires next month.",
  "The warranty covers accidental damage.",
  "The evidence suggests that the policy works.",
  "The theory explains the observed data.",
  "The file upload failed this morning.",
  "The image upload was interrupted.",
  "The data upload finished overnight.",
  "The study involved thirty participants over six months.",
  "The traffic report was worrying.",
  "The safety review documents every incident.",
  "The process covers both cases.",
  "The review process starts on Monday.",
  "The essay question section was hard.",
  "The machine learning model was retrained.",
  "The policy covers pre-existing conditions.",
  "The teacher recommends rest and fluids.",
  "The manager recommends that we proceed.",
  // both_sg_plur_verb
  "Both proposals were rejected by the board.",
  "Both children were excited about the trip.",
  "Both police officers were praised for their response.",
  "Both staff members were rostered for the weekend.",
  "Both matches were postponed due to the weather.",
  "Both fish were returned to the stream.",
  // mass_noun_sva
  "The weather in Auckland is unpredictable.",
  "The information was not available at the time.",
  "Her feedback was positive and constructive.",
  "The traffic on the bridge was heavier than usual.",
  "The equipment in the lab was recalibrated.",
  // modal_be_pp (adjective/other readings)
  "The margin will be close this time.",
  "The race will be close until the final lap.",
  "The venue will be closed during the renovations.",
  "The results will be out on Friday.",
  "The office will be open on Saturday.",
  "The session will be held in the boardroom.",
  // be + adverb + verb (already correct -ing)
  "We are currently experiencing some issues with the payment gateway.",
  "She is now managing the Auckland branch.",
  "They were still hoping for a miracle.",
  "He was always making us laugh.",
  // their / they're
  "Their has been" == "x" ? "" : "There has been a delay in shipping.",
  "They're accurate and well sourced.",
  "Their late father was a respected kaumatua.",
  "Their late arrival caused a short delay.",
  "Their ready meals sell well in the suburbs.",
  "Their missing keys were found under the stairs.",
  "Their correct answers earned full marks.",
  "Their broken screen was replaced under warranty.",
  // reason of (protected idioms)
  "He pleaded not guilty by reason of insanity.",
  "For reasons of safety, the climb was abandoned.",
  "The main reason for the failure was poor planning.",
  // person + which (correct who)
  "Students who study regularly perform better in exams.",
  "The players who trained hardest were selected.",
  // relative head agreement (correct)
  "The report which was submitted yesterday has several errors.",
  "The report that was filed last week has been reviewed twice.",
  "The plan that was approved last month is now on track.",
  "The invoice which was paid yesterday covers the March order.",
  // effects as noun (relative clauses, determined nouns)
  "The side effects the drug causes are usually mild.",
  "The effects the treatment produced were temporary.",
  "The effects on the health of residents were measured.",
  "Several effects of the outage were still emerging.",
  "The long-term effects of the spill remain unclear.",
  // adjective + gerund (correct compounds / valid uses)
  "A growing concern for policymakers was the cost of living.",
  "The rising cost of fuel was the main issue.",
  "The declining balance covered the payment.",
  "A significant improvement in results was observed.",
  "The increasing cost of materials forced a rethink.",
  // childrens correct forms
  "The children's toys were scattered across the floor.",
  // compared from/with
  "Compared with last year, sales have doubled.",
  "Compared to the old model, this one is faster.",
  // apologies correct
  "We apologise for the inconvenience caused.",
  "Please accept our apologies for the delay.",
  "Our apologies go out to the affected families.",
  // interesting
  "The documentary was interesting in many ways.",
  "I am interested in the junior developer role.",
  "The topic is interesting to most readers.",
  // noun + attached
  "Please find the report attached to this email.",
  "The photo attached to the message was blurry.",
  "Please attach the file to the email.",
  // thank you + patience/patients
  "Thank you for your patience during the outage.",
  "The nurses checked on their patients during the night shift.",
  "Thanks for your patience while we investigated.",
  // head of PP
  "The number of participants was higher than expected.",
  "A number of students were absent today.",
  "The number of applications has doubled since May.",
  // plural + of-PP + singular be (correct singular heads)
  "The list of items was on the desk.",
  "The total of the invoices was settled on Friday.",
  "The group of tourists was waiting at the gate.",
  "What did the weather do in July?",
  "To whom should the report go?",
  // noun/verb homograph compound traps (v9.7.2 split rules)
  "The book cover tears easily.",
  "The job offer expires tomorrow.",
  "The train track bends near the river.",
  "The water supply fails during the drought.",
  "The birthday surprise arrives tonight.",
  "The subject matter was dry.",
  "The door handle breaks.",
  "The insurance lapse costs the claim.",
  "The storm damage worsens each week.",
  "The question mark denotes the end.",
  "The security check takes an hour.",
  "The product launch succeeds.",
  "The meeting delay annoys everyone.",
  "The policy influence grows each year.",
  "The farm produce arrives weekly.",
  "The game highlight airs tonight.",
  "The island shape changes over time.",
  "The equipment hire includes insurance.",
  "The meeting call starts at three.",
  "The student interest grows each term.",
  "The insurance benefit expires next year.",
  "The visitor welcome includes a powhiri.",
  "The module import fails silently.",
  "The file transfer completes overnight.",
  "The server load spikes at noon.",
  "The quality control catches defects early.",
  "The word limit exceeds the target.",
  // wh-subject clauses (regression)
  "Why the process is failing remains unclear.",
  "What he said was true.",
  "How the machine works is explained in the manual.",
  // misc regression
  "The centre is open on weekends.",
  "I don't know why the process keeps failing.",
  "The bus leaves at seven every morning.",
  "Maths is my favourite subject.",
];
let fp = 0;
for (const t of T) {
  if (!t) continue;
  const lints = W94.lint(t);
  if (lints.length) {
    fp++;
    console.log('FP: "' + t + '"');
    for (const l of lints) console.log('    ' + JSON.stringify(t.slice(l.start, l.end)) + ' -> ' + JSON.stringify(l.suggestions[0]) + ' [' + l.rule + ']');
  }
}
console.log('adversarial2: ' + (T.filter(Boolean).length - fp) + '/' + T.filter(Boolean).length + ' clean');

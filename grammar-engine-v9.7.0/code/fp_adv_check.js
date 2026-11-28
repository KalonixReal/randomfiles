// Adversarial FP stress: correct sentences that sit exactly in the new rule
// families' strike zones. None of these may be flagged.
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
  // possessive strike zone (plural person noun + owned noun, legit compounds/labels)
  "The teachers lounge was repainted over the holidays.",
  "All passengers luggage was scanned at the gate.",
  // do-support zone (participles in valid environments)
  "Did you get seen by the triage nurse?",
  "We did have known issues with the build.",
  "What did the manager say about the delay?",
  "Did they have finished before the deadline?",
  // does + 3sg-looking words in valid structures
  "What does the machine do when the train leaves?",
  "How does the panel decide which option works best?",
  "What time does the ferry depart for the island?",
  // double comparatives zone
  "This approach is more practical than the old one.",
  "She is the most careful driver in the family.",
  "The most interesting part was the ending.",
  // indefinite subjects
  "Everyone in the village who was evacuated has returned home.",
  "Everyone of us was given a uniform.", // 'everyone of us' awkward but not flagged zone
  "Everything in the boxes was labelled and dated.",
  "Something in the engine was making a strange noise.",
  // head-of-PP
  "A number of students were absent today.",
  "The majority of voters were under thirty.",
  "The group of tourists were waiting at the gate.",
  // its/it's zone
  "The project kept its due date despite the outage.",
  "Its due date is next Friday.",
  "The committee published its findings last month.",
  "The cat licked its paws and went to sleep.",
  // preposition + time
  "Let's check in next week once the build is green.",
  "We will drop in next Tuesday to inspect the site.",
  "The results are due on this coming Friday.",
  "She was born in the last week of March.",
  "They arrived on Monday morning.",
  // be_quite zone
  "I'll be quite honest with you about the margins.",
  "The review was quite thorough in the end.",
  "Quite frankly, the design is quite elegant.",
  // explain zone
  "She explained the problem twice before we understood.",
  "The teacher explained the rule to us carefully.",
  "Can you explain them in plain language?", // them = inanimate DO
  // almost zone
  "Almost all the passengers were on board by six.",
  "Almost nobody was injured in the collision.",
  // loose zone
  "There is some loose change in the drawer.",
  "The bolt came loose after the vibration test.",
  "They set the hounds loose on the scent.",
  // the both / be+agree
  "Both teams played well in the wet.",
  "We are agreed on the final wording.",
  "It was agreed that the merger would proceed.",
  "It was agreed by both parties.",
  "The terms were agreed between the unions and the council.",
  // misc strike zones
  "The list of items was on the desk.",
  "She made a mistake in the calculation.",
  "He did the mistake analysis after the outage.", // 'did the mistake analysis' valid
  "The team have won every match this season.",   // GB collective
  "Our team has been training on Tuesdays.",
  "Where did you go after the trip?",
  "The settings panel shows more options than before.",
  "I look forward to receiving your reply.",
];
let fp = 0;
for (const t of T) {
  const lints = W94.lint(t);
  if (lints.length) {
    fp++;
    console.log('FP: "' + t + '"');
    for (const l of lints) console.log('    ' + JSON.stringify(t.slice(l.start, l.end)) + ' -> ' + JSON.stringify(l.suggestions[0]) + ' [' + l.rule + ']');
  }
}
console.log('adversarial: ' + (T.length - fp) + '/' + T.length + ' clean');

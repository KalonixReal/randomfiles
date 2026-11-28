// Probe: run shipped engine on the 7 U1 FP sentences, print each finding with rule id.
const fs = require('fs');
const path = require('path');
const data = fs.readFileSync(path.join(__dirname, 'export_out/engine94_data.json'), 'utf8');
const rules = fs.readFileSync(path.join(__dirname, 'export_out/engine94_rules.json'), 'utf8');
const weights = fs.readFileSync(path.join(__dirname, 'export_out/engine94_weights.b64'), 'utf8').trim();
let code = fs.readFileSync(path.join(__dirname, 'engine94.js'), 'utf8');
code = 'const W94_DATA=' + data + ';\nconst W94_RULES=' + rules + ';\nconst W94_WEIGHTS_B64=' + JSON.stringify(weights) + ';\n' + code;
code = code.replace(/self\.onmessage[\s\S]*$/m, '');
code += "\n;globalThis.W94=W94;";
eval(code);

const PROBE = [
  "The variable kPoints holds the k-d tree nodes for the search.",
  "Ask at the i-SITE for current track conditions before you set out.",
  "Which candidate did you vote for in the last election?",
  "Seldom have we seen such a close final at this ground.",
  "The police have cordoned off the area near the wharf.",
  "It is I who am to blame for the delay.",
  "Maths is my favourite subject this year.",
  "The committee have not yet reached agreement on the budget forecast.",
  "Our neighbours have just built a lovely new veranda.",
  "She sometimes seems distracted in the afternoon.",
  "The bus is late again this morning.",
  "We was told that the trip might be cancelled.",
  "The revised budget was send to the committee yesterday.",
  "I look forward to receive your feedback on the draft.",
];
for (const t of PROBE) {
  const lints = W94.lint(t);
  console.log('"' + t.slice(0, 60) + '"');
  if (!lints.length) { console.log('   (clean)'); continue; }
  for (const l of lints) {
    console.log(`   [${l.rule}] "${t.slice(l.start, l.end)}" -> "${l.suggestions[0]}" | ${l.message.slice(0, 50)} | type=${l.type94}`);
  }
}

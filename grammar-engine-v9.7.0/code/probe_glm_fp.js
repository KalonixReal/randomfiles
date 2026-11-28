// Probe the GLM-flagged FP sentences with full rule attribution.
const fs = require('fs');
const path = require('path');
const data = fs.readFileSync(path.join(__dirname, 'export_out/engine94_data.json'), 'utf8');
const rules = fs.readFileSync(path.join(__dirname, 'export_out/engine94_rules.json'), 'utf8');
let code = fs.readFileSync(path.join(__dirname, 'engine94.js'), 'utf8');
code = 'const W94_DATA=' + data + ';\nconst W94_RULES=' + rules + ';\nconst W94_WEIGHTS_B64=' + JSON.stringify('') + ';\n' + code;
code = code.replace(/self\.onmessage[\s\S]*$/m, '');
code += "\n;globalThis.W94=W94;";
globalThis.atob = s => Buffer.from(s, 'base64').toString('binary');
eval(code);

const flagged = JSON.parse(fs.readFileSync('/home/z/my-project/work/distill/glm_flagged.json', 'utf8'));
for (const f of flagged) {
  console.log('"' + f.text + '"');
  for (const l of W94.rulesFindings(f.text)) {
    console.log(`   [${l.src}] "${f.text.slice(l.start, l.end)}" -> "${l.rep}"`);
  }
}
console.log('\n=== targeted follow-ups ===');
const EXTRA = [
  "The minutes from yesterday's meeting have been distributed.",
  "Neither of the options seems particularly appealing.",
  "Not only did he finish the race, but he also broke the record.",
  "What time does the train depart for London?",
  "Linguistics is a complex field with many sub-disciplines.",
  "The committee have reached a unanimous agreement.",
  "A unanimous decision was reached within an hour.",
  "She gave a unique perspective on the proposal.",
  "Physics is taught by Mr Harris this year.",
  "The scissors are in the top drawer.",
  "One of the students is late every morning.",
  "Each of the players receives a medal.",
  "Either of the dates suits me fine.",
  "What time does the bus leave?",
  "Where does the ferry dock at Picton?",
  "Why does the engine stall when cold?",
  "How does the parser handle nested lists?",
];
for (const t of EXTRA) {
  const lints = W94.rulesFindings(t);
  console.log('"' + t.slice(0, 62) + '"  -> ' + (lints.length ? lints.map(l => `[${l.src}] "${t.slice(l.start, l.end)}"=>"${l.rep}"`).join(' ; ') : 'CLEAN'));
}

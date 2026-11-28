// Probe: embedded wh-subject clauses must NOT be turned into direct questions.
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

const CASES = [
  // ---- reported FP and its family: wh-clause as SUBJECT (must stay clean)
  ["Why the process is failing remains unclear.", 0],
  ["What he said was true.", 0],
  ["Why she left remains a mystery.", 0],
  ["How the machine works is explained in the manual.", 0],
  ["When the ferry departs depends on the weather.", 0],
  ["Where they hid the key is still unknown.", 0],
  ["What the committee decided surprised everyone.", 0],
  ["Why the process was delayed remains unclear to the board.", 0],
  ["How the team performs matters to the sponsors.", 0],
  ["What remains unclear is why the process is failing.", 0],
  ["Whether the plan works remains to be seen.", 0],
  // ---- real errors: direct question missing inversion (must be flagged)
  ["Why you are always late for the stand-up?", 1],
  ["Why the meeting is cancelled?", 1],
  ["Where the station is?", 1],
  ["How much the ticket costs?", 1],
  ["What time the ferry departs?", 1],
  ["When the results are announced?", 1],
  // ---- embedded wh after cognition verbs (clean; tagger zone)
  ["I wonder why the process is failing.", 0],
  ["Nobody knows where the spare keys are kept.", 0],
  ["We asked why the shipment was delayed.", 0],
  // ---- singular -s nouns before is/was (plural_subj_be must stay quiet)
  ["The process is working as expected.", 0],
  ["The status is still unknown.", 0],
  ["The bus is coming in five minutes.", 0],
  ["What remains unclear is why the process is failing.", 0],
  ["The students is arriving at eight sharp.", 1], // genuine plural subj
];
let bad = 0;
for (const [t, wantErr] of CASES) {
  const lints = W94.lint(t);
  const flagged = lints.length > 0;
  const ok = flagged === !!wantErr;
  if (!ok) bad++;
  console.log((ok ? 'ok  ' : 'FAIL') + ' want=' + wantErr + ' n=' + lints.length + ' | ' + t);
  for (const l of lints) console.log('       ' + JSON.stringify(t.slice(l.start, l.end)) + ' -> ' + JSON.stringify(l.suggestions[0]) + ' [' + l.rule + ']');
}
console.log(bad === 0 ? 'ALL OK' : 'FAILURES: ' + bad);

// Debug specific sentences through the shipped engine
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

const cases = [
  'Me and Dave are painting the fence on Saturday.',
  'I am not sure why was the meeting cancelled.',
  'The occurence was reported to the office.',
  'The teachers desk was covered in marking.',
  "It's raining and the dogs been outside for hours.",
  'Did you seen the size of that kahawai?',
  'What time does the last bus leaves?',
  'I am work on the caching layer this week.',
];
for (const t of cases) {
  const lints = W94.lint(t);
  console.log('TEXT: ' + t);
  for (const l of lints) console.log('   -> ' + JSON.stringify(t.slice(l.start, l.end)) + ' => ' + JSON.stringify(l.suggestions && l.suggestions[0]) + ' [' + l.rule + ']');
  if (!lints.length) console.log('   (no findings)');
}

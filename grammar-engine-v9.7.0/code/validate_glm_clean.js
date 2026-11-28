// Validate GLM clean corpus against current rules engine (tagger off).
// usage: node validate_glm_clean.js
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

const items = fs.readFileSync('/home/z/my-project/work/distill/glm_clean.jsonl', 'utf8')
  .split('\n').filter(Boolean).map(JSON.parse);
console.log('validating', items.length, 'sentences (rules-only)');

const cleanOut = [];
const flagged = [];
for (const it of items) {
  const lints = W94.rulesFindings(it.text);
  if (lints.length) flagged.push({ text: it.text, domain: it.domain, lints });
  else cleanOut.push(it);
}
fs.writeFileSync('/home/z/my-project/work/distill/glm_clean_valid.jsonl',
  cleanOut.map(x => JSON.stringify(x)).join('\n') + '\n');
console.log(`clean=${cleanOut.length} flagged=${flagged.length}`);
fs.writeFileSync('/home/z/my-project/work/distill/glm_flagged.json', JSON.stringify(flagged, null, 1));
for (const f of flagged) {
  console.log(`  [${f.domain}] ${f.text.slice(0, 72)}`);
  for (const l of f.lints) {
    console.log(`    ${f.text.slice(l.start, l.end)} -> ${l.rep} (${l.type})`);
  }
}

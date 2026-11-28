// FP diagnosis: run the shipped Engine94 over clean sentences and list every finding.
// usage: node diag_engine.js <split.jsonl> <label> [max]
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

const SPLIT = process.argv[2];
const LABEL = process.argv[3] || 'split';
const items = fs.readFileSync(SPLIT, 'utf8').split('\n').filter(x => x.trim()).map(JSON.parse);
const clean = items.filter(it => !it.edits.length);
console.log(`split=${LABEL} total=${items.length} clean=${clean.length} with_errors=${items.length - clean.length}`);

const byRule = {};
const byType = {};
let flagged = 0;
const examples = [];
for (const it of clean) {
  const lints = W94.lint(it.text);
  if (lints.length) flagged++;
  for (const l of lints) {
    const key = (l.src || l.type) + '|' + (l.type || '');
    byRule[key] = (byRule[key] || 0) + 1;
    byType[l.type] = (byType[l.type] || 0) + 1;
    if (examples.length < 400) {
      examples.push({ text: it.text, cat: it.cats, origin: it.origin,
        span: it.text.slice(l.start, l.end), rep: l.suggestions ? l.suggestions[0] : l.rep,
        key, start: l.start, end: l.end, msg: l.message });
    }
  }
}
console.log(`CLEAN FALSE ALERTS: ${flagged}/${clean.length} sentences flagged (${(100 * flagged / clean.length).toFixed(1)}%)`);
console.log('by rule:', JSON.stringify(byRule, null, 0));
console.log('by type:', JSON.stringify(byType, null, 0));
fs.writeFileSync(`export_out/diag_${LABEL}_examples.json`, JSON.stringify(examples, null, 1));
console.log(`examples -> export_out/diag_${LABEL}_examples.json`);

// also: erroneous-row FP breakdown (which rules fire wrongly on error rows)
let tp = 0, fp = 0;
const byRuleErr = {};
const NORM = x => x.replace(/\s+/g, ' ').trim().toLowerCase();
const apply = (t, s, e, r) => t.slice(0, s) + r + t.slice(e);
for (const it of items.filter(x => x.edits.length)) {
  const lints = W94.lint(it.text);
  const goldEff = new Set(it.edits.map(g => NORM(apply(it.text, g.start, g.end, g.rep))));
  for (const l of lints) {
    const eff = NORM(apply(it.text, l.start, l.end, l.suggestions ? l.suggestions[0] : l.rep));
    if (goldEff.has(eff)) tp++;
    else { fp++; const key = (l.src || l.type) + '|' + (l.type || ''); byRuleErr[key] = (byRuleErr[key] || 0) + 1; }
  }
}
console.log(`error rows: tp=${tp} fp=${fp}`);
console.log('fp by rule (error rows):', JSON.stringify(byRuleErr, null, 0));
fs.writeFileSync(`export_out/diag_${LABEL}_errfp.json`, JSON.stringify(byRuleErr, null, 1));

// List recall misses (FNs) of the shipped engine config on a split.
// usage: node list_misses.js <split.jsonl> [threshold]
const fs = require('fs');
const path = require('path');

const SPLIT = process.argv[2] || 'data_built/x2.jsonl';
const THRESH = process.argv[3] ? parseFloat(process.argv[3]) : 1.0;

const data = fs.readFileSync(path.join(__dirname, 'export_out/engine94_data.json'), 'utf8');
const rules = fs.readFileSync(path.join(__dirname, 'export_out/engine94_rules.json'), 'utf8');
const weights = fs.readFileSync(path.join(__dirname, 'export_out/engine94_weights.b64'), 'utf8').trim();
let code = fs.readFileSync(path.join(__dirname, 'engine94.js'), 'utf8');
const dataObj = JSON.parse(data);
dataObj.threshold = THRESH;
code = 'const W94_DATA=' + JSON.stringify(dataObj) + ';\nconst W94_RULES=' + rules + ';\nconst W94_WEIGHTS_B64=' + JSON.stringify(weights) + ';\n' + code;
code = code.replace(/self\.onmessage[\s\S]*$/m, '');
code += "\n;globalThis.W94=W94;";
globalThis.atob = s => Buffer.from(s, 'base64').toString('binary');
eval(code);

const items = fs.readFileSync(path.join(__dirname, SPLIT), 'utf8').split('\n').filter(x => x.trim()).map(JSON.parse);
const NORM = x => x.replace(/\s+/g, ' ').trim().toLowerCase();
const apply = (t, s, e, r) => t.slice(0, s) + r + t.slice(e);
let missed = [], hit = 0, total = 0;
for (const it of items) {
  if (!it.edits.length) continue;
  const lints = W94.lint(it.text);
  const props = lints.map(l => ({ start: l.start, end: l.end, rep: l.suggestions ? l.suggestions[0] : '' }));
  for (const g of it.edits) {
    total++;
    const geff = NORM(apply(it.text, g.start, g.end, g.rep));
    const found = props.some(f => NORM(apply(it.text, f.start, f.end, f.rep)) === geff);
    if (found) hit++;
    else missed.push({ text: it.text, orig: it.text.slice(g.start, g.end), rep: g.rep });
  }
}
console.log('GOLD edits:', total, 'hit:', hit, 'MISSED:', missed.length);
for (const m of missed) console.log('  MISS | ' + m.text.slice(0, 90) + '  ||  ' + JSON.stringify(m.orig) + ' -> ' + JSON.stringify(m.rep));

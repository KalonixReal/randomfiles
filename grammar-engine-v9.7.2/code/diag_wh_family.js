// Diagnostic: which rules fire on X2/X3 error sentences; how many wh-family
// true positives live in sentences ending with "?" (to size an end="?" guard).
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

const WH_FAMILY = ['wh_front_missing', 'wh_pl_np_is', 'wh_pl_np_was', 'wh_pl_np_has',
  'wh_pl_np_does', 'wh_sg_np_are', 'wh_sg_np_were', 'wh_sg_np_do', 'wh_sg_np_have',
  'wh_pl_np_is2', 'wh_embedded', 'whq_does_insert', 'whq_3sg_base',
  'does_3sg_final', 'does_3sg_q', 'wh_embedded_pron'];

const NORM = x => x.replace(/\s+/g, ' ').trim().toLowerCase();
const apply = (t, s, e, r) => t.slice(0, s) + r + t.slice(e);

for (const SPLIT of ['data_built/x2.jsonl', 'data_built/x3.jsonl']) {
  const items = fs.readFileSync(path.join(__dirname, SPLIT), 'utf8').split('\n').filter(Boolean).map(JSON.parse);
  const stat = {}; const examples = {};
  for (const it of items) {
    if (!it.edits.length) continue;
    const lints = W94.lint(it.text);
    const endsQ = /\?\s*$/.test(it.text);
    for (const l of lints) {
      const id = (l.rule || '').replace('Engine94:rule:', '');
      const p = { start: l.start, end: l.end, rep: l.suggestions ? l.suggestions[0] : '' };
      const goldEff = new Set(it.edits.map(g => NORM(apply(it.text, g.start, g.end, g.rep))));
      const isTP = goldEff.has(NORM(apply(it.text, p.start, p.end, p.rep)));
      const key = id + (isTP ? ':TP' : ':FP');
      stat[key] = (stat[key] || 0) + 1;
      if (WH_FAMILY.includes(id)) {
        examples[key] = examples[key] || [];
        if (examples[key].length < 6) examples[key].push((endsQ ? '[?]' : '[.]') + ' ' + it.text.slice(0, 70));
      }
    }
  }
  console.log('==== ' + SPLIT);
  for (const k of Object.keys(stat).sort()) console.log('  ' + k + ' x' + stat[k]);
  for (const k of Object.keys(examples)) {
    console.log('  -- ' + k);
    for (const e of examples[k]) console.log('     ' + e);
  }
}

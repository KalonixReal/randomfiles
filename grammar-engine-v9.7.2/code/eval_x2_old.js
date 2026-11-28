// One-shot X2 eval for the OLD v9.5.0 shipped engine (intact files in download/model).
// usage: node eval_x2_old.js <split.jsonl>
const fs = require('fs');
const path = require('path');

const SPLIT = process.argv[2] || 'data_built/x2.jsonl';
const M = '/home/z/my-project/download/model';
const data = fs.readFileSync(path.join(M, 'engine94_data.json'), 'utf8');
const rules = fs.readFileSync(path.join(M, 'engine94_rules.json'), 'utf8');
const weights = fs.readFileSync(path.join(M, 'engine94_weights.b64'), 'utf8').trim();
let code = fs.readFileSync(path.join(M, 'engine94.js'), 'utf8');
code = 'const W94_DATA=' + data + ';\nconst W94_RULES=' + rules + ';\nconst W94_WEIGHTS_B64=' + JSON.stringify(weights) + ';\n' + code;
code = code.replace(/self\.onmessage[\s\S]*$/m, '');
code += "\n;globalThis.W94=W94;";
globalThis.atob = s => Buffer.from(s, 'base64').toString('binary');
eval(code);

const items = fs.readFileSync(path.join(__dirname, SPLIT), 'utf8').split('\n').filter(x => x.trim()).map(JSON.parse);
const NORM = x => x.replace(/\s+/g, ' ').trim().toLowerCase();
const apply = (t, s, e, r) => t.slice(0, s) + r + t.slice(e);

function scoreOne(props, goldEdits, text) {
  if (!goldEdits.length) return { tp: 0, fp: props.length, fn: 0 };
  const goldEff = new Set(goldEdits.map(g => NORM(apply(text, g.start, g.end, g.rep))));
  let tp = 0, fp = 0;
  for (const f of props) {
    const eff = NORM(apply(text, f.start, f.end, f.rep));
    goldEff.has(eff) ? tp++ : fp++;
  }
  const covered = new Set();
  goldEdits.forEach((g, gi) => {
    const geff = NORM(apply(text, g.start, g.end, g.rep));
    if (props.some(f => NORM(apply(text, f.start, f.end, f.rep)) === geff)) covered.add(gi);
  });
  return { tp, fp, fn: goldEdits.length - covered.size };
}

let TP = 0, FP = 0, FN = 0, clean = 0, cleanFlagged = 0;
const flaggedExamples = [];
for (const it of items) {
  const lints = W94.lint(it.text);
  const props = lints.map(l => ({ start: l.start, end: l.end, rep: l.suggestions ? l.suggestions[0] : '' }));
  const r = scoreOne(props, it.edits, it.text);
  TP += r.tp; FP += r.fp; FN += r.fn;
  if (!it.edits.length) {
    clean++;
    if (r.fp > 0) {
      cleanFlagged++;
      flaggedExamples.push({ text: it.text, findings: lints.map(l => `${it.text.slice(l.start, l.end)}->${l.suggestions[0]} (${l.rule})`) });
    }
  }
}
const P = TP / Math.max(1, TP + FP), R = TP / Math.max(1, TP + FN);
const F05 = (P + R) ? 1.25 * P * R / (0.25 * P + R) : 0;
console.log(JSON.stringify({ engine: 'v9.5.0-old', n: items.length, clean,
  P: +P.toFixed(3), R: +R.toFixed(3), F05: +F05.toFixed(3), tp: TP, fp: FP, fn: FN,
  FA: +(cleanFlagged / Math.max(1, clean)).toFixed(3) }, null, 0));
fs.writeFileSync(path.join(__dirname, 'export_out/x2_eval_old.json'),
  JSON.stringify({ P, R, F05, tp: TP, fp: FP, fn: FN, clean, cleanFlagged, flaggedExamples }, null, 1));
for (const f of flaggedExamples) console.log('  FP: "' + f.text.slice(0, 66) + '" ' + f.findings.join(' ; '));

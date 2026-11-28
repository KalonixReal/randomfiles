// Threshold sweep for the neural tagger across splits.
// usage: node sweep_threshold.js
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const THRESHOLDS = [0.98, 0.99, 0.995, 0.997, 0.999, 1.0];
const SPLITS = [
  ['dev', 'data_built/dev.jsonl'],
  ['calib', 'data_built/calib.jsonl'],
  ['test', 'data_built/test.jsonl'],
  ['u1', 'data_built/u1_clean.jsonl'],
];

const data = fs.readFileSync(path.join(__dirname, 'export_out/engine94_data.json'), 'utf8');
const rules = fs.readFileSync(path.join(__dirname, 'export_out/engine94_rules.json'), 'utf8');
const weights = fs.readFileSync(path.join(__dirname, 'export_out/engine94_weights.b64'), 'utf8').trim();
let code = fs.readFileSync(path.join(__dirname, 'engine94.js'), 'utf8');

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

const itemsBySplit = {};
for (const [name, p] of SPLITS) {
  itemsBySplit[name] = fs.readFileSync(path.join(__dirname, p), 'utf8')
    .split('\n').filter(x => x.trim()).map(JSON.parse);
}

const results = [];
for (const th of THRESHOLDS) {
  const dataObj = JSON.parse(data);
  dataObj.threshold = th;
  let engineCode = 'const W94_DATA=' + JSON.stringify(dataObj) + ';\nconst W94_RULES=' + rules +
    ';\nconst W94_WEIGHTS_B64=' + JSON.stringify(weights) + ';\n' + code;
  engineCode = engineCode.replace(/self\.onmessage[\s\S]*$/m, '');
  engineCode += "\n;globalThis.W94=W94;";
  const ctx = { console, Date, Math, RegExp, JSON, Array, Object, String, Number, Set, Map,
    atob: s => Buffer.from(s, 'base64').toString('binary') };
  vm.createContext(ctx);
  vm.runInContext(engineCode, ctx);
  const row = { threshold: th };
  for (const [name] of SPLITS) {
    let TP = 0, FP = 0, FN = 0, clean = 0, fa = 0, t0 = Date.now();
    for (const it of itemsBySplit[name]) {
      const lints = vm.runInContext(`W94.lint(${JSON.stringify(it.text)})`, ctx);
      const props = lints.map(l => ({ start: l.start, end: l.end, rep: l.suggestions ? l.suggestions[0] : '' }));
      const r = scoreOne(props, it.edits, it.text);
      TP += r.tp; FP += r.fp; FN += r.fn;
      if (!it.edits.length) { clean++; if (r.fp > 0) fa++; }
    }
    const P = TP / Math.max(1, TP + FP), R = TP / Math.max(1, TP + FN);
    const F05 = (P + R) ? 1.25 * P * R / (0.25 * P + R) : 0;
    row[name] = { P: +P.toFixed(3), R: +R.toFixed(3), F05: +F05.toFixed(3),
      FA: +(fa / Math.max(1, clean)).toFixed(3), ms: +(((Date.now() - t0) / itemsBySplit[name].length).toFixed(1)) };
  }
  results.push(row);
  console.log(JSON.stringify(row));
}
fs.writeFileSync(path.join(__dirname, 'export_out/threshold_sweep.json'), JSON.stringify(results, null, 1));
console.log('saved export_out/threshold_sweep.json');

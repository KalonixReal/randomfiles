// One-shot evaluation on the X2 final test (clean + errors), shipped-config engine.
// usage: node eval_x2.js <split.jsonl> [threshold]
const fs = require('fs');
const path = require('path');

const SPLIT = process.argv[2] || 'data_built/x2.jsonl';
const data = fs.readFileSync(path.join(__dirname, 'export_out/engine94_data.json'), 'utf8');
const rules = fs.readFileSync(path.join(__dirname, 'export_out/engine94_rules.json'), 'utf8');
const weights = fs.readFileSync(path.join(__dirname, 'export_out/engine94_weights.b64'), 'utf8').trim();
let code = fs.readFileSync(path.join(__dirname, 'engine94.js'), 'utf8');
const dataObj = JSON.parse(data);
if (process.argv[3]) dataObj.threshold = parseFloat(process.argv[3]);
code = 'const W94_DATA=' + JSON.stringify(dataObj) + ';\nconst W94_RULES=' + rules + ';\nconst W94_WEIGHTS_B64=' + JSON.stringify(weights) + ';\n' + code;
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

let TP = 0, FP = 0, FN = 0, clean = 0, cleanFlagged = 0, errs = 0;
const latencies = [];
const flaggedExamples = [];
for (const it of items) {
  const t0 = Date.now();
  const lints = W94.lint(it.text);
  latencies.push(Date.now() - t0);
  const props = lints.map(l => ({ start: l.start, end: l.end, rep: l.suggestions ? l.suggestions[0] : '' }));
  const r = scoreOne(props, it.edits, it.text);
  TP += r.tp; FP += r.fp; FN += r.fn;
  if (!it.edits.length) {
    clean++;
    if (r.fp > 0) {
      cleanFlagged++;
      flaggedExamples.push({ text: it.text, findings: lints.map(l => `${it.text.slice(l.start, l.end)}->${l.suggestions[0]} (${l.rule})`) });
    }
  } else errs++;
}
latencies.sort((a, b) => a - b);
const P = TP / Math.max(1, TP + FP), R = TP / Math.max(1, TP + FN);
const F05 = (P + R) ? 1.25 * P * R / (0.25 * P + R) : 0;
const out = {
  split: SPLIT, threshold: dataObj.threshold, n: items.length, clean, errs,
  P: +P.toFixed(3), R: +R.toFixed(3), F05: +F05.toFixed(3),
  tp: TP, fp: FP, fn: FN,
  FA: +(cleanFlagged / Math.max(1, clean)).toFixed(3), cleanFlagged, clean,
  latency_ms_p50: latencies[Math.floor(latencies.length / 2)],
  latency_ms_p90: latencies[Math.floor(latencies.length * 0.9)],
  false_alerts: flaggedExamples,
};
console.log(JSON.stringify({ ...out, false_alerts: undefined }, null, 0));
fs.writeFileSync(path.join(__dirname, 'export_out', `x2_eval_${path.basename(SPLIT, '.jsonl')}.json`), JSON.stringify(out, null, 1));
if (flaggedExamples.length) {
  console.log('false alerts on clean text:');
  for (const f of flaggedExamples) console.log('  "' + f.text.slice(0, 70) + '" ' + f.findings.join(' ; '));
}

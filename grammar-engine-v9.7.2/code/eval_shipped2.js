// FINAL one-shot test: runs the exact shipped Engine94 worker code (as embedded
// in notepad-v9.5.0-grammar.html) over the test split in Node.
// usage: node eval_shipped2.js <out.json>
const fs = require('fs');
const path = require('path');

const OUT = process.argv[2] || 'export_out/shipped2_test.json';
const data = fs.readFileSync(path.join(__dirname, 'export_out/engine94_data.json'), 'utf8');
const rules = fs.readFileSync(path.join(__dirname, 'export_out/engine94_rules.json'), 'utf8');
const weights = fs.readFileSync(path.join(__dirname, 'export_out/engine94_weights.b64'), 'utf8').trim();
let code = fs.readFileSync(path.join(__dirname, 'engine94.js'), 'utf8');
code = 'const W94_DATA=' + data + ';\nconst W94_RULES=' + rules + ';\nconst W94_WEIGHTS_B64=' + JSON.stringify(weights) + ';\n' + code;
code = code.replace(/self\.onmessage[\s\S]*$/m, '');
code += "\n;globalThis.W94=W94;";
eval(code);

const items = fs.readFileSync(path.join(__dirname, 'data_built/test.jsonl'), 'utf8')
  .split('\n').filter(x => x.trim()).map(JSON.parse);

// scorer mirrors engine.py score() (equivalent-effect)
const NORM = x => x.replace(/\s+/g, ' ').trim().toLowerCase();
const apply = (t, s, e, r) => t.slice(0, s) + r + t.slice(e);

function scoreOne(props, goldEdits, text) {
  if (!goldEdits.length) {
    return { tp: 0, fp: props.length, fn: 0 };
  }
  const goldEff = new Set();
  const goldKeys = new Set();
  for (const g of goldEdits) {
    goldEff.add(NORM(apply(text, g.start, g.end, g.rep)));
    goldKeys.add(g.start + '|' + g.end + '|' + String(g.rep).trim().toLowerCase());
  }
  let tp = 0, fp = 0;
  const covered = new Set();
  for (const f of props) {
    const eff = NORM(apply(text, f.start, f.end, f.suggestions ? f.suggestions[0] : f.rep));
    const key = f.start + '|' + f.end + '|' + String(f.suggestions ? f.suggestions[0] : f.rep).trim().toLowerCase();
    let hit = false;
    if (goldEff.has(eff) || goldKeys.has(key)) {
      // find which gold it covers (for recall bookkeeping)
      hit = true;
      goldEdits.forEach((g, gi) => {
        if (covered.has(gi)) return;
        const geff = NORM(apply(text, g.start, g.end, g.rep));
        if (geff === eff) covered.add(gi);
      });
    }
    hit ? tp++ : fp++;
  }
  for (const g of goldEdits) {
    const geff = NORM(apply(text, g.start, g.end, g.rep));
    const gkey = g.start + '|' + g.end + '|' + String(g.rep).trim().toLowerCase();
    const ok = props.some(f => {
      const feff = NORM(apply(text, f.start, f.end, f.suggestions ? f.suggestions[0] : f.rep));
      const fkey = f.start + '|' + f.end + '|' + String(f.suggestions ? f.suggestions[0] : f.rep).trim().toLowerCase();
      return feff === geff || fkey === gkey;
    });
    if (ok) covered.add(goldEdits.indexOf(g));
  }
  const fn = goldEdits.length - covered.size;
  return { tp, fp, fn };
}

let TP = 0, FP = 0, FN = 0;
let cleanN = 0, cleanFlagged = 0, adversarial = 0, advViolations = 0;
const perCat = {};
const latencies = [];
const perItem = [];
for (const it of items) {
  const t0 = Date.now();
  const lints = W94.lint(it.text);
  latencies.push(Date.now() - t0);
  const props = lints.map(l => ({ start: l.start, end: l.end, rep: l.suggestions ? l.suggestions[0] : '' }));
  const r = scoreOne(props, it.edits, it.text);
  TP += r.tp; FP += r.fp; FN += r.fn;
  if (!it.edits.length) {
    cleanN++;
    if (r.fp > 0) cleanFlagged++;
    if (it.origin === 'adversarial') {
      adversarial++;
      if (r.fp > 0) advViolations++;
    }
  }
  for (const e of it.edits) {
    const c = e.type || '?';
    perCat[c] = perCat[c] || { tp: 0, fn: 0 };
  }
  // per-cat recall
  for (const g of it.edits) {
    const geff = NORM(apply(it.text, g.start, g.end, g.rep));
    const ok = props.some(f => NORM(apply(it.text, f.start, f.end, f.suggestions ? f.suggestions[0] : f.rep)) === geff);
    perCat[g.type || '?'][ok ? 'tp' : 'fn']++;
  }
  perItem.push({ text: it.text, edits: it.edits.length, props: props.length, tp: r.tp, fp: r.fp, fn: r.fn });
}
const P = TP / (TP + FP), R = TP / (TP + FN);
const F05 = (1 + 0.25) * P * R / (0.25 * P + R);
latencies.sort((a, b) => a - b);
const out = {
  engine: 'SHIPPED v9.5.0 (rules2+tagger@0.995, JS truth, worker code)',
  P: +P.toFixed(4), R: +R.toFixed(4), F05: +F05.toFixed(4),
  tp: TP, fp: FP, fn: FN,
  false_alert_rate: +(cleanFlagged / Math.max(1, cleanN)).toFixed(4),
  clean_n: cleanN, err_n: items.length - cleanN,
  meaning_violations: advViolations, adversarial_n: adversarial,
  lat_ms_median: latencies[Math.floor(latencies.length / 2)],
  lat_ms_p95: latencies[Math.floor(latencies.length * 0.95)],
  per_cat: perCat,
};
fs.writeFileSync(path.join(__dirname, OUT), JSON.stringify(out, null, 1));
console.log(JSON.stringify(out, null, 1).slice(0, 1200));

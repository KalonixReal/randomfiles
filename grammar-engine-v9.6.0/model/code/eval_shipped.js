// Evaluates the SHIPPED combination: filtered Harper + the actual JS engine
// (rules + tagger + guards, exactly what ships in the HTML).
// Reads: export_out/harper_f_test.json (filtered Harper findings per test item)
//        data_built/test.jsonl
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const HERE = __dirname;
const W94_DATA = JSON.parse(fs.readFileSync(path.join(HERE, 'export_out', 'engine94_data.json'), 'utf8'));
const W94_RULES = JSON.parse(fs.readFileSync(path.join(HERE, 'export_out', 'engine94_rules.json'), 'utf8'));
const W94_WEIGHTS_B64 = fs.readFileSync(path.join(HERE, 'export_out', 'engine94_weights.b64'), 'utf8').trim();
const src = fs.readFileSync(path.join(HERE, 'engine94.js'), 'utf8');
const sandbox = { W94_DATA, W94_RULES, W94_WEIGHTS_B64, console, Math, JSON,
  atob: (s) => Buffer.from(s, 'base64').toString('binary') };
sandbox.self = sandbox;
const ctx = vm.createContext(sandbox);
vm.runInContext(src, ctx, { filename: 'engine94.js' });
vm.runInContext('W94.ensureLoaded()', ctx);

const harperF = JSON.parse(fs.readFileSync(path.join(HERE, 'export_out', 'harper_f_test.json'), 'utf8'));
const items = fs.readFileSync(path.join(HERE, 'data_built', 'test.jsonl'), 'utf8')
  .split('\n').filter(x => x.trim()).map(JSON.parse);

const NORM = (s) => s.replace(/\s+/g, ' ').trim().toLowerCase();
const applyEdit = (t, s, e, r) => t.slice(0, s) + r + t.slice(e);
function score(props, gold, text) {
  if (!gold.length) return [0, props.length, 0];
  const goldEff = new Set(gold.map(g => NORM(applyEdit(text, g.start, g.end, g.rep))));
  const goldKeys = new Set(gold.map(g => `${g.start},${g.end},${(g.rep || '').trim().toLowerCase()}`));
  let tp = 0, fp = 0;
  for (const f of props) {
    const eff = NORM(applyEdit(text, f.start, f.end, f.rep));
    const key = `${f.start},${f.end},${(f.rep || '').trim().toLowerCase()}`;
    if (goldEff.has(eff) || goldKeys.has(key)) tp++; else fp++;
  }
  let covered = 0;
  for (const g of gold) {
    const geff = NORM(applyEdit(text, g.start, g.end, g.rep));
    const gk = `${g.start},${g.end},${(g.rep || '').trim().toLowerCase()}`;
    if (props.some(f => NORM(applyEdit(text, f.start, f.end, f.rep)) === geff || `${f.start},${f.end},${(f.rep || '').trim().toLowerCase()}` === gk)) covered++;
  }
  return [tp, fp, gold.length - covered];
}

let TP = 0, FP = 0, FN = 0, fa = 0, clean = 0, mv = 0, adv = 0;
const t0 = Date.now();
items.forEach((it, i) => {
  const harp = harperF[i] || [];
  const mine = vm.runInContext(`W94.lint(${JSON.stringify(it.text)})`, ctx)
    .map(f => ({ start: f.start, end: f.end, rep: f.suggestions[0], type: f.rule }));
  const add = [];
  for (const f of mine) {
    if (harp.some(h => f.start < h.end && h.start < f.end)) continue;
    if (add.some(o => f.start < o.end && o.start < f.end)) continue;
    add.push(f);
  }
  const props = harp.concat(add);
  const [tp, fp, fn] = score(props, it.edits, it.text);
  TP += tp; FP += fp; FN += fn;
  if (it.edits.length === 0) {
    clean++;
    if (fp > 0) fa++;
    if (it.origin === 'adversarial') { adv++; if (props.length) mv++; }
  }
});
const P = TP / (TP + FP), R = TP / (TP + FN);
const row = {
  engine: 'SHIPPED (harper_f + js-engine@0.98) [JS truth]',
  P: +P.toFixed(3), R: +R.toFixed(3),
  F05: +((P + R) ? 1.25 * P * R / (0.25 * P + R) : 0).toFixed(3),
  tp: TP, fp: FP, fn: FN,
  FA: +(fa / Math.max(1, clean)).toFixed(3),
  MV: mv, adversarial: adv,
  ms_per_sentence: +((Date.now() - t0) / items.length).toFixed(1),
};
console.log(JSON.stringify(row, null, 1));
fs.writeFileSync(path.join(HERE, 'export_out', 'shipped_test.json'), JSON.stringify(row, null, 1));

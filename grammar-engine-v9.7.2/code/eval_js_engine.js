// Full evaluation of the SHIPPED JS engine (rules + tagger + guards) on the
// evaluation splits. Usage: node eval_js_engine.js dev|calib|test
// Also evaluates the JS rules layer alone for layer attribution.
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const HERE = __dirname;
const W94_DATA = JSON.parse(fs.readFileSync(path.join(HERE, 'export_out', 'engine94_data.json'), 'utf8'));
const W94_RULES = JSON.parse(fs.readFileSync(path.join(HERE, 'export_out', 'engine94_rules.json'), 'utf8'));
const W94_WEIGHTS_B64 = fs.readFileSync(path.join(HERE, 'export_out', 'engine94_weights.b64'), 'utf8').trim();

const src = fs.readFileSync(path.join(HERE, 'engine94.js'), 'utf8');
const sandbox = {
  W94_DATA, W94_RULES, W94_WEIGHTS_B64,
  console, Math, JSON,
  atob: (s) => Buffer.from(s, 'base64').toString('binary'),
};
sandbox.self = sandbox;
const ctx = vm.createContext(sandbox);
vm.runInContext(src, ctx, { filename: 'engine94.js' });
vm.runInContext('W94.ensureLoaded()', ctx);

const split = process.argv[2] || 'dev';
const items = fs.readFileSync(path.join(HERE, 'data_built', split + '.jsonl'), 'utf8')
  .split('\n').filter(x => x.trim()).map(JSON.parse);

// ---- scoring (mirrors engine.py equivalent-effect matcher)
const NORM = (s) => s.replace(/\s+/g, ' ').trim().toLowerCase();
const applyEdit = (t, s, e, r) => t.slice(0, s) + r + t.slice(e);

function score(props, gold, text) {
  if (!gold.length) return [0, props.length, 0];
  const goldEff = new Set();
  for (const g of gold) goldEff.add(NORM(applyEdit(text, g.start, g.end, g.rep)));
  const goldKeys = new Set(gold.map(g => `${g.start},${g.end},${(g.rep || '').trim().toLowerCase()}`));
  let tp = 0, fp = 0;
  for (const f of props) {
    const eff = NORM(applyEdit(text, f.start, f.end, f.rep));
    const key = `${f.start},${f.end},${(f.rep || '').trim().toLowerCase()}`;
    if (goldEff.has(eff) || goldKeys.has(key)) tp++;
    else fp++;
  }
  let covered = 0;
  for (const g of gold) {
    const geff = NORM(applyEdit(text, g.start, g.end, g.rep));
    const gk = `${g.start},${g.end},${(g.rep || '').trim().toLowerCase()}`;
    if (props.some(f => NORM(applyEdit(text, f.start, f.end, f.rep)) === geff ||
      `${f.start},${f.end},${(f.rep || '').trim().toLowerCase()}` === gk)) covered++;
  }
  return [tp, fp, gold.length - covered];
}

function evaluate(name, getProps) {
  let TP = 0, FP = 0, FN = 0, fa = 0, clean = 0, errs = 0, mv = 0, adv = 0;
  const t0 = Date.now();
  for (const it of items) {
    const props = getProps(it);
    const [tp, fp, fn] = score(props, it.edits, it.text);
    TP += tp; FP += fp; FN += fn;
    if (it.edits.length === 0) {
      clean++;
      if (fp > 0) fa++;
      if (it.origin === 'adversarial') { adv++; if (props.length) mv++; }
    } else errs++;
  }
  const P = TP / Math.max(1, TP + FP), R = TP / Math.max(1, TP + FN);
  const F05 = (P + R) ? 1.25 * P * R / (0.25 * P + R) : 0;
  const ms = (Date.now() - t0) / items.length;
  const row = { engine: name, P: +P.toFixed(3), R: +R.toFixed(3), F05: +F05.toFixed(3),
    tp: TP, fp: FP, fn: FN, FA: +(fa / Math.max(1, clean)).toFixed(3),
    MV: mv, adv, ms_per_sentence: +ms.toFixed(1) };
  console.log(JSON.stringify(row));
  return row;
}

const rows = [];
rows.push(evaluate('js-engine (rules+tagger@0.98)', (it) =>
  vm.runInContext(`W94.lint(${JSON.stringify(it.text)})`, ctx)
    .map(f => ({ start: f.start, end: f.end, rep: f.suggestions && f.suggestions[0], type: (f.rule || '').split(':')[1] }))));
rows.push(evaluate('js-rules-only', (it) =>
  vm.runInContext(`W94.rulesFindings(${JSON.stringify(it.text)})`, ctx)));
fs.writeFileSync(path.join(HERE, 'export_out', `js_engine_${split}.json`), JSON.stringify(rows, null, 1));
console.log('saved export_out/js_engine_' + split + '.json');

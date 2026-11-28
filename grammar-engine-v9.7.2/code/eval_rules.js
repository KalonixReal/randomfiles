// Fast rules-iteration harness: loads blobs from export_out (no HTML rebuild),
// evaluates a split with the same strict/combined metrics as eval_x3.js.
// usage: node eval_rules.js <split.jsonl> [rulesOverride.json]
const fs = require('fs');
const path = require('path');
const SPLIT = process.argv[2] || 'data_built/x3.jsonl';
const RULES_FILE = process.argv[3] || path.join(__dirname, 'export_out/engine94_rules.json');

const data = fs.readFileSync(path.join(__dirname, 'export_out/engine94_data.json'), 'utf8');
const rules = fs.readFileSync(RULES_FILE, 'utf8');
const weights = fs.readFileSync(path.join(__dirname, 'export_out/engine94_weights.b64'), 'utf8').trim();
let code = fs.readFileSync(path.join(__dirname, 'engine94.js'), 'utf8');
const dataObj = JSON.parse(data);
dataObj.threshold = 1.0; // shipped config: rules-only, tagger dormant
code = 'const W94_DATA=' + JSON.stringify(dataObj) + ';\nconst W94_RULES=' + rules +
  ';\nconst W94_WEIGHTS_B64=' + JSON.stringify(weights) + ';\n' + code.slice(0, code.indexOf('\n// worker protocol'));
code += '\n;globalThis.W94=W94;';
globalThis.atob = s => Buffer.from(s, 'base64').toString('binary');
eval(code);
console.log('engine loaded; rules version =', JSON.parse(rules).version);

const items = fs.readFileSync(path.join(__dirname, SPLIT), 'utf8').split('\n').filter(Boolean).map(JSON.parse);
const NORM = x => x.replace(/\s+/g, ' ').trim().toLowerCase();
const apply = (t, s, e, r) => t.slice(0, s) + r + t.slice(e);
const applyAll = (t, edits) => {
  let out = t;
  for (const g of [...edits].sort((a, b) => b.start - a.start)) out = apply(out, g.start, g.end, g.rep);
  return out;
};

let TP = 0, FPc = 0, FN = 0, clean = 0, cleanFlagged = 0;
let TPcomb = 0, FNcomb = 0;
const lat = [];
const misses = [];
for (const it of items) {
  const t0 = Date.now();
  const lints = W94.lint(it.text);
  lat.push(Date.now() - t0);
  const props = lints.map(l => ({ start: l.start, end: l.end, rep: l.suggestions ? l.suggestions[0] : '' }));
  if (!it.edits.length) {
    clean++;
    if (props.length) {
      cleanFlagged++;
      console.log('  FA: "' + it.text.slice(0, 70) + '" ' + lints.map(l => `${it.text.slice(l.start, l.end)}->${l.suggestions[0]}[${l.rule}]`).join('; '));
    }
    continue;
  }
  const goldEff = new Set(it.edits.map(g => NORM(apply(it.text, g.start, g.end, g.rep))));
  for (const p of props) goldEff.has(NORM(apply(it.text, p.start, p.end, p.rep))) ? TP++ : FPc++;
  const covered = new Set();
  it.edits.forEach((g, gi) => {
    const geff = NORM(apply(it.text, g.start, g.end, g.rep));
    if (props.some(pp => NORM(apply(it.text, pp.start, pp.end, pp.rep)) === geff)) covered.add(gi);
  });
  FN += it.edits.length - covered.size;
  const engAll = NORM(applyAll(it.text, props));
  const goldAll = NORM(applyAll(it.text, it.edits));
  const rowCovered = covered.size === it.edits.length || engAll === goldAll;
  if (rowCovered) TPcomb += it.edits.length;
  else {
    TPcomb += covered.size;
    FNcomb += it.edits.length - covered.size;
    misses.push({ text: it.text, edits: it.edits, found: lints.map(l => ({ s: it.text.slice(l.start, l.end), r: l.suggestions[0] })) });
  }
}
lat.sort((a, b) => a - b);
const P = TP / Math.max(1, TP + FPc), R = TP / Math.max(1, TP + FN);
const F05 = (P + R) ? 1.25 * P * R / (0.25 * P + R) : 0;
const Pc = TPcomb / Math.max(1, TPcomb + FPc), Rc = TPcomb / Math.max(1, TPcomb + FNcomb);
const F05c = (Pc + Rc) ? 1.25 * Pc * Rc / (0.25 * Pc + Rc) : 0;
console.log(JSON.stringify({
  split: SPLIT, n: items.length, clean, rules: JSON.parse(rules).version,
  strict: { P: +P.toFixed(3), R: +R.toFixed(3), F05: +F05.toFixed(3), tp: TP, fp: FPc, fn: FN },
  combined: { P: +Pc.toFixed(3), R: +Rc.toFixed(3), F05: +F05c.toFixed(3) },
  FA: +(cleanFlagged / Math.max(1, clean)).toFixed(3),
  lat_p50_ms: lat[Math.floor(lat.length / 2)], lat_p90_ms: lat[Math.floor(lat.length * 0.9)]
}, null, 1));
// dump misses for rule mining
fs.writeFileSync('/tmp/misses_' + path.basename(SPLIT, '.jsonl') + '.json', JSON.stringify(misses, null, 1));
console.log(misses.length + ' rows with misses dumped to /tmp/misses_' + path.basename(SPLIT, '.jsonl') + '.json');

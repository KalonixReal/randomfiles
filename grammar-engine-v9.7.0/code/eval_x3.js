// One-shot X3 evaluation with two coverage definitions:
//  * strict    — an engine finding counts as TP only when its effective
//                sentence equals a SINGLE gold edit's effective sentence
//                (identical to the X2/v9.6.0 harness; comparable numbers).
//  * combined  — additionally credits the case where applying all engine
//                findings equals applying all gold edits (multi-edit golds
//                such as swaps/reorders are otherwise unmatchable).
// usage: node eval_x3.js <html> <split.jsonl>
const fs = require('fs');
const path = require('path');

const HTML = process.argv[2] || '/home/z/my-project/download/notepad-v9.7.0-grammar.html';
const SPLIT = process.argv[3] || 'data_built/x3.jsonl';

const f = fs.readFileSync(HTML, 'utf8');
const s0 = f.indexOf('<script type="text/plain" id="grammarReleaseWorker">');
const s1 = f.indexOf('</script>', s0);
const script = f.slice(s0, s1);

function extractConst(varname) {
  const tag = 'const ' + varname + ' = ';
  const i = script.indexOf(tag);
  if (i < 0) return null;
  if (varname === 'W94_WEIGHTS_B64') {
    const j = script.indexOf('";', i + tag.length);
    return script.slice(i + tag.length + 1, j);
  }
  const rest = script.slice(i + tag.length);
  let depth = 0, k = 0;
  for (; k < rest.length; k++) {
    if (rest[k] === '{') depth++;
    else if (rest[k] === '}') { depth--; if (depth === 0) break; }
  }
  return rest.slice(0, k + 1);
}

const data = extractConst('W94_DATA');
const rules = extractConst('W94_RULES');
const weights = extractConst('W94_WEIGHTS_B64');

const newJs = fs.readFileSync(path.join(__dirname, 'engine94.js'), 'utf8');
const marker = '\n// worker protocol';
let code = newJs.slice(0, newJs.indexOf(marker));
const glue = 'const W94_DATA=' + data + ';\nconst W94_RULES=' + rules +
  ';\nconst W94_WEIGHTS_B64=' + JSON.stringify(weights) + ';\n' + code;
const mod = glue + "\n;globalThis.W94=W94;";
globalThis.atob = s => Buffer.from(s, 'base64').toString('binary');
eval(mod);
console.log('shipped engine loaded; threshold =', JSON.parse(data).threshold, '| rules version =', JSON.parse(rules).version);

const items = fs.readFileSync(path.join(__dirname, SPLIT), 'utf8').split('\n').filter(Boolean).map(JSON.parse);
const NORM = x => x.replace(/\s+/g, ' ').trim().toLowerCase();
const apply = (t, s, e, r) => t.slice(0, s) + r + t.slice(e);
const applyAll = (t, edits) => {
  let out = t;
  for (const g of [...edits].sort((a, b) => b.start - a.start)) out = apply(out, g.start, g.end, g.rep);
  return out;
};

let TP = 0, FPc = 0, FN = 0, clean = 0, cleanFlagged = 0, cleanFlaggedList = [];
let TPcomb = 0, FNcomb = 0;
const lat = [];
for (const it of items) {
  const t0 = Date.now();
  const lints = W94.lint(it.text);
  lat.push(Date.now() - t0);
  const props = lints.map(l => ({ start: l.start, end: l.end, rep: l.suggestions ? l.suggestions[0] : '' }));
  if (!it.edits.length) {
    clean++;
    if (props.length) { cleanFlagged++; cleanFlaggedList.push(it.text); }
    continue;
  }
  // strict per-edit coverage
  const goldEff = new Set(it.edits.map(g => NORM(apply(it.text, g.start, g.end, g.rep))));
  for (const p of props) goldEff.has(NORM(apply(it.text, p.start, p.end, p.rep))) ? TP++ : FPc++;
  const covered = new Set();
  it.edits.forEach((g, gi) => {
    const geff = NORM(apply(it.text, g.start, g.end, g.rep));
    if (props.some(pp => NORM(apply(it.text, pp.start, pp.end, pp.rep)) === geff)) covered.add(gi);
  });
  FN += it.edits.length - covered.size;
  // combined-effect coverage: all findings applied == all gold edits applied
  const engAll = NORM(applyAll(it.text, props));
  const goldAll = NORM(applyAll(it.text, it.edits));
  const rowCovered = covered.size === it.edits.length || engAll === goldAll;
  if (rowCovered) TPcomb += it.edits.length; else {
    // partial credit at row granularity for the combined metric
    TPcomb += covered.size;
    FNcomb += it.edits.length - covered.size;
    console.log('  X3 miss | ' + it.text.slice(0, 78) + ' || ' + it.edits.map(g => JSON.stringify(it.text.slice(g.start, g.end)) + '->' + JSON.stringify(g.rep)).join(', '));
  }
}
lat.sort((a, b) => a - b);
const P = TP / Math.max(1, TP + FPc), R = TP / Math.max(1, TP + FN);
const F05 = (P + R) ? 1.25 * P * R / (0.25 * P + R) : 0;
const Pc = TPcomb / Math.max(1, TPcomb + FPc), Rc = TPcomb / Math.max(1, TPcomb + FNcomb);
const F05c = (Pc + Rc) ? 1.25 * Pc * Rc / (0.25 * Pc + Rc) : 0;
console.log(JSON.stringify({
  split: SPLIT, n: items.length, clean,
  strict: { P: +P.toFixed(3), R: +R.toFixed(3), F05: +F05.toFixed(3), tp: TP, fp: FPc, fn: FN },
  combined: { P: +Pc.toFixed(3), R: +Rc.toFixed(3), F05: +F05c.toFixed(3) },
  FA: +(cleanFlagged / Math.max(1, clean)).toFixed(3),
  cleanFlagged: cleanFlagged,
  lat_p50: lat[Math.floor(lat.length / 2)], lat_p90: lat[Math.floor(lat.length * 0.9)]
}, null, 1));

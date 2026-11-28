// Fresh-set comparison harness. Evaluates a shipped-engine build (extracted
// from an HTML bundle) on data_built/fresh.jsonl, with optional tagger-veto
// post-filter (suppresses a rule finding when the bundled tagger is confident
// the covered tokens are clean: max(1 - p($KEEP)) < vetoThresh).
// usage: node eval_fresh.js <html> <label> [vetoThresh]
const fs = require('fs');
const path = require('path');

const HTML = process.argv[2];
const LABEL = process.argv[3] || 'engine';
const VETO = process.argv[4] ? parseFloat(process.argv[4]) : null;
const SPLIT = process.argv[5] || 'data_built/fresh.jsonl';

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
const dataObj = JSON.parse(data);

const newJs = fs.readFileSync(path.join(__dirname, 'engine94.js'), 'utf8');
const marker = '\n// worker protocol';
let code = newJs.slice(0, newJs.indexOf(marker));
const glue = 'const W94_DATA=' + data + ';\nconst W94_RULES=' + rules +
  ';\nconst W94_WEIGHTS_B64=' + JSON.stringify(weights) + ';\n' + code;
const mod = glue + "\n;globalThis.W94=W94;";
globalThis.atob = s => Buffer.from(s, 'base64').toString('binary');
eval(mod);
console.log('engine loaded:', LABEL, '| rules =', JSON.parse(rules).version, '| threshold =', dataObj.threshold, '| veto =', VETO);

// --- tagger veto machinery (mirrors tagger_veto_sweep.js)
const KEEP_ID = dataObj.edits.indexOf('$KEEP');
const TOKEN_RE = /[A-Za-z0-9]+(?:'[A-Za-z0-9]+)*|[.,!?;:"()$£€%]/g;
function tokenErrProbs(text) {
  const { logits, T, V } = W94.forward(text);
  const withOff = [];
  let m; TOKEN_RE.lastIndex = 0;
  while ((m = TOKEN_RE.exec(text))) withOff.push([m[0], m.index, m.index + m[0].length]);
  const out = [];
  for (let j = 0; j < withOff.length; j++) {
    const i = j + 1;
    if (i >= T) break;
    const ex = new Array(V); let tot = 0;
    for (let v = 0; v < V; v++) { ex[v] = Math.exp(logits[i * V + v]); tot += ex[v]; }
    out.push({ s: withOff[j][1], e: withOff[j][2], pKeep: ex[KEEP_ID] / tot });
  }
  return out;
}
function vetoed(text, lints) {
  if (VETO === null || !lints.length) return false;
  const teps = tokenErrProbs(text);
  for (const l of lints) {
    let mx = 0;
    for (const t of teps) if (t.s < l.end && l.start < t.e) mx = Math.max(mx, 1 - t.pKeep);
    if (mx >= VETO) return false; // any endorsed finding survives
  }
  return true; // all findings vetoed
}
function filterVeto(text, lints) {
  if (VETO === null || !lints.length) return lints;
  const teps = tokenErrProbs(text);
  return lints.filter(l => {
    let mx = 0;
    for (const t of teps) if (t.s < l.end && l.start < t.e) mx = Math.max(mx, 1 - t.pKeep);
    return mx >= VETO;
  });
}

const items = fs.readFileSync(path.join(__dirname, SPLIT), 'utf8').split('\n').filter(Boolean).map(JSON.parse);
const NORM = x => x.replace(/\s+/g, ' ').trim().toLowerCase();
const apply = (t, s, e, r) => t.slice(0, s) + r + t.slice(e);
const applyAll = (t, edits) => {
  let out = t;
  for (const g of [...edits].sort((a, b) => b.start - a.start)) out = apply(out, g.start, g.end, g.rep);
  return out;
};

let errSents = 0, errDetected = 0, cleanSents = 0, cleanFlagged = 0;
let TP = 0, FPc = 0, FN = 0;
const byGenre = {};
const flaggedClean = [], missedErrors = [];
for (const it of items) {
  const lints0 = W94.lint(it.text);
  const lints = filterVeto(it.text, lints0);
  const isErr = it.edits.length > 0;
  const g = it.genre;
  byGenre[g] = byGenre[g] || { n: 0, det: 0, fp: 0 };
  if (isErr) {
    errSents++; byGenre[g].n++;
    if (lints.length) { errDetected++; byGenre[g].det++; }
    else missedErrors.push(it.text);
    // error-level strict
    const props = lints.map(l => ({ start: l.start, end: l.end, rep: l.suggestions ? l.suggestions[0] : '' }));
    const goldEff = new Set(it.edits.map(g2 => NORM(apply(it.text, g2.start, g2.end, g2.rep))));
    for (const p of props) goldEff.has(NORM(apply(it.text, p.start, p.end, p.rep))) ? TP++ : FPc++;
    const covered = new Set();
    it.edits.forEach((g2, gi) => {
      const geff = NORM(apply(it.text, g2.start, g2.end, g2.rep));
      if (props.some(pp => NORM(apply(it.text, pp.start, pp.end, pp.rep)) === geff)) covered.add(gi);
    });
    FN += it.edits.length - covered.size;
  } else {
    cleanSents++; byGenre[g].n++;
    if (lints.length) {
      cleanFlagged++; byGenre[g].fp++;
      flaggedClean.push({ text: it.text, findings: lints.map(l => `${it.text.slice(l.start, l.end)}->${l.suggestions[0]} (${(l.rule || '').replace('Engine94:rule:', '')})`) });
    }
  }
}
const sentP = errDetected / Math.max(1, errDetected + cleanFlagged);
const sentR = errDetected / Math.max(1, errSents);
const sentF05 = (sentP + sentR) ? 1.25 * sentP * sentR / (0.25 * sentP + sentR) : 0;
const strictP = TP / Math.max(1, TP + FPc), strictR = TP / Math.max(1, TP + FN);
const strictF05 = (strictP + strictR) ? 1.25 * strictP * strictR / (0.25 * strictP + strictR) : 0;
const out = {
  label: LABEL, html: path.basename(HTML), rules: JSON.parse(rules).version, veto: VETO,
  split: SPLIT, n: items.length, errors: errSents, clean: cleanSents,
  sentence: { recall: +sentR.toFixed(3), FA: +(cleanFlagged / Math.max(1, cleanSents)).toFixed(3), P: +sentP.toFixed(3), F05: +sentF05.toFixed(3), detected: errDetected, cleanFlagged },
  strict: { P: +strictP.toFixed(3), R: +strictR.toFixed(3), F05: +strictF05.toFixed(3), tp: TP, fp: FPc, fn: FN },
  byGenre,
  flaggedClean, missedErrors,
};
console.log(JSON.stringify({ ...out, flaggedClean: undefined, missedErrors: undefined }, null, 1));
if (flaggedClean.length) { console.log('clean flagged:'); for (const fc of flaggedClean) console.log('  "' + fc.text.slice(0, 70) + '" ' + fc.findings.join(' ; ')); }
if (missedErrors.length) { console.log('errors missed:'); for (const me of missedErrors) console.log('  ' + me.slice(0, 70)); }
fs.writeFileSync(path.join(__dirname, 'export_out', `fresh_${LABEL}.json`), JSON.stringify(out, null, 1));

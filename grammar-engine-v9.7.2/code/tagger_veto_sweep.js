// Tagger-veto sweep: for each rule finding, compute the bundled tagger's
// confidence that the covered tokens are fine (p($KEEP)). If the tagger is
// confident the region is clean, the rule finding is suppressed ("veto").
// Question: does this kill false alerts on clean prose without killing
// true positives on error sentences?
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

const KEEP_ID = dataObj.edits.indexOf('$KEEP');
const TOKEN_RE = /[A-Za-z0-9]+(?:'[A-Za-z0-9]+)*|[.,!?;:"()$£€%]/g;

function tokenErrProbs(text) {
  // per-token (1 - p($KEEP)) for real tokens, aligned to char offsets
  const { logits, T, V, full } = W94.forward(text);
  const withOff = [];
  let m; TOKEN_RE.lastIndex = 0;
  while ((m = TOKEN_RE.exec(text))) withOff.push([m[0], m.index, m.index + m[0].length]);
  const out = [];
  for (let j = 0; j < withOff.length; j++) {
    const i = j + 1; // <s> offset
    if (i >= T) break;
    let maxv = -Infinity, maxid = 0, tot = 0;
    const ex = new Array(V);
    for (let v = 0; v < V; v++) {
      const val = logits[i * V + v];
      ex[v] = Math.exp(val);
      tot += ex[v];
      if (val > maxv) { maxv = val; maxid = v; }
    }
    const pKeep = ex[KEEP_ID] / tot;
    out.push({ tok: withOff[j][0], s: withOff[j][1], e: withOff[j][2], pKeep, argmax: dataObj.edits[maxid] });
  }
  return out;
}

function maxPerrOverSpan(teps, start, end) {
  let mx = 0;
  for (const t of teps) if (t.s < end && start < t.e) mx = Math.max(mx, 1 - t.pKeep);
  return mx;
}

const NORM = x => x.replace(/\s+/g, ' ').trim().toLowerCase();
const apply = (t, s, e, r) => t.slice(0, s) + r + t.slice(e);

function loadSplit(p) {
  try { return fs.readFileSync(path.join(__dirname, p), 'utf8').split('\n').filter(x => x.trim()).map(JSON.parse); }
  catch (e) { return null; }
}
// adversarial list: extract the T array literal from fp_adv_check.js
const advSrc = fs.readFileSync(path.join(__dirname, 'fp_adv_check.js'), 'utf8');
const a0 = advSrc.indexOf('const T = [');
const a1 = advSrc.indexOf('];', a0);
const advArr = eval(advSrc.slice(a0 + 'const T ='.length, a1 + 1)
  .replace(/\/\/[^\n"[]*/g, ''));

const SPLITS = {
  'x2': loadSplit('data_built/x2.jsonl'),
  'x3': loadSplit('data_built/x3.jsonl'),
  'adv': advArr.map(t => ({ text: t, edits: [] })),
};

const results = {};
for (const [name, items] of Object.entries(SPLITS)) {
  if (!items) continue;
  const rows = [];
  for (const it of items) {
    const lints = W94.lint(it.text);
    if (!lints.length) continue;
    const teps = tokenErrProbs(it.text);
    const goldEff = it.edits && it.edits.length ? new Set(it.edits.map(g => NORM(apply(it.text, g.start, g.end, g.rep)))) : null;
    for (const l of lints) {
      const eff = NORM(apply(it.text, l.start, l.end, l.suggestions ? l.suggestions[0] : ''));
      const isTP = goldEff ? goldEff.has(eff) : null;
      const perr = maxPerrOverSpan(teps, l.start, l.end);
      rows.push({ isTP, isClean: !goldEff, perr: +perr.toFixed(4), rule: (l.rule || '').replace('Engine94:rule:', ''), text: it.text.slice(0, 60) });
    }
  }
  results[name] = rows;
}

console.log('KEEP tag id:', KEEP_ID, '| edits vocab size:', dataObj.edits.length);
const THRESHES = [0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50];
for (const th of THRESHES) {
  const line = { th };
  for (const [name, rows] of Object.entries(results)) {
    const errRows = rows.filter(r => !r.isClean);
    const cleanRows = rows.filter(r => r.isClean);
    line[name] = {
      keptTP: errRows.filter(r => r.isTP && r.perr >= th).length,
      vetoTP: errRows.filter(r => r.isTP && r.perr < th).length,
      keptFP: errRows.filter(r => !r.isTP && r.perr >= th).length,
      vetoFP: errRows.filter(r => !r.isTP && r.perr < th).length,
      keptCleanFP: cleanRows.filter(r => r.perr >= th).length,
      vetoCleanFP: cleanRows.filter(r => r.perr < th).length,
    };
  }
  console.log(JSON.stringify(line));
}

console.log('\n-- veto profile @0.20 --');
for (const [name, rows] of Object.entries(results)) {
  if (name === 'adv') continue;
  const by = {};
  for (const r of rows.filter(x => !x.isClean)) {
    const k = r.rule + (r.isTP ? '|TP' : '|FP');
    if (r.perr < 0.20) by[k] = (by[k] || 0) + 1;
  }
  const ks = Object.keys(by);
  if (ks.length) console.log(name + ' vetoed: ' + ks.map(k => k + ' x' + by[k]).join(', '));
}
// clean-side: which rules get vetoed on clean/adversarial text at 0.20
for (const [name, rows] of Object.entries(results)) {
  const by = {};
  for (const r of rows.filter(x => x.isClean)) {
    if (r.perr < 0.20) by[r.rule] = (by[r.rule] || 0) + 1;
  }
  const ks = Object.keys(by);
  if (ks.length) console.log(name + ' clean-vetoed: ' + ks.map(k => k + ' x' + by[k]).join(', '));
}
fs.writeFileSync(path.join(__dirname, 'export_out', 'tagger_veto_sweep.json'), JSON.stringify(results, null, 1));
console.log('\nraw rows saved to export_out/tagger_veto_sweep.json');

// Evaluate the engine EXACTLY as shipped inside notepad-v9.6.0-grammar.html:
// extract the grammarReleaseWorker blobs + engine body from the built file,
// then run the FP probes + U1 + X2 one-shot with them.
// usage: node eval_shipped3.js <built.html> [split.jsonl]
const fs = require('fs');
const path = require('path');

const HTML = process.argv[2] || '/home/z/my-project/download/notepad-v9.6.0-grammar.html';
const SPLIT = process.argv[3] || null;

const f = fs.readFileSync(HTML, 'utf8');
const s0 = f.indexOf('<script type="text/plain" id="grammarReleaseWorker">');
const s1 = f.indexOf('</script>', s0);
if (s0 < 0) { console.error('worker script not found'); process.exit(1); }
const script = f.slice(s0, s1);

const dec = JSON;

function extractConst(varname) {
  const tag = 'const ' + varname + ' = ';
  const i = script.indexOf(tag);
  if (i < 0) return null;
  if (varname === 'W94_WEIGHTS_B64') {
    const j = script.indexOf('";', i + tag.length);
    return script.slice(i + tag.length + 1, j);
  }
  const rest = script.slice(i + tag.length);
  // find the matching end of the JSON object literal: walk braces
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
console.log('extracted: data', data.length, 'rules', rules.length, 'weights', weights.length);

const newJs = fs.readFileSync(path.join(__dirname, 'engine94.js'), 'utf8');
const marker = '\n// worker protocol';
let code = newJs.slice(0, newJs.indexOf(marker));
const glue = 'const W94_DATA=' + data + ';\nconst W94_RULES=' + rules +
  ';\nconst W94_WEIGHTS_B64=' + JSON.stringify(weights) + ';\n' + code;
const mod = glue + "\n;globalThis.W94=W94;";
globalThis.atob = s => Buffer.from(s, 'base64').toString('binary');
eval(mod);
console.log('shipped engine loaded; threshold =', JSON.parse(data).threshold);

// FP probes
const PROBE = [
  "The variable kPoints holds the k-d tree nodes for the search.",
  "Ask at the i-SITE for current track conditions before you set out.",
  "Which candidate did you vote for in the last election?",
  "Seldom have we seen such a close final at this ground.",
  "The police have cordoned off the area near the wharf.",
  "It is I who am to blame for the delay.",
  "Maths is my favourite subject this year.",
  "She sometimes seems distracted in the afternoon.",
  "Have you seen the new film yet?",
  "What time does the train depart for London?",
  "Linguistics is a complex field with many sub-disciplines.",
  "Neither of the options seems particularly appealing.",
  "The committee have reached a unanimous agreement.",
  "The chassis was badly damaged in the rally.",
  "The revised budget was send to the committee yesterday.",
  "I look forward to receive your feedback on the draft.",
];
let fp = 0;
for (const t of PROBE) {
  const lints = W94.lint(t);
  if (lints.length) { fp++; console.log('  FP: "' + t.slice(0, 55) + '" ' + lints.map(l => `${t.slice(l.start, l.end)}->${l.suggestions[0]}`).join('; ')); }
}
console.log(`FP probes: ${PROBE.length - fp}/${PROBE.length} clean`);

if (SPLIT) {
  const items = fs.readFileSync(path.join(__dirname, SPLIT), 'utf8').split('\n').filter(Boolean).map(JSON.parse);
  const NORM = x => x.replace(/\s+/g, ' ').trim().toLowerCase();
  const apply = (t, s, e, r) => t.slice(0, s) + r + t.slice(e);
  let TP = 0, FPc = 0, FN = 0, clean = 0, cleanFlagged = 0;
  const lat = [];
  for (const it of items) {
    const t0 = Date.now();
    const lints = W94.lint(it.text);
    lat.push(Date.now() - t0);
    const props = lints.map(l => ({ start: l.start, end: l.end, rep: l.suggestions ? l.suggestions[0] : '' }));
    if (!it.edits.length) {
      clean++;
      if (props.length) { cleanFlagged++; console.log('  FA: "' + it.text.slice(0, 66) + '" ' + lints.map(l => `${it.text.slice(l.start, l.end)}->${l.suggestions[0]}`).join('; ')); }
      continue;
    }
    const goldEff = new Set(it.edits.map(g => NORM(apply(it.text, g.start, g.end, g.rep))));
    for (const p of props) {
      NORM(apply(it.text, p.start, p.end, p.rep)) === undefined ? null : null;
      goldEff.has(NORM(apply(it.text, p.start, p.end, p.rep))) ? TP++ : FPc++;
    }
    const covered = new Set();
    it.edits.forEach((g, gi) => {
      const geff = NORM(apply(it.text, g.start, g.end, g.rep));
      if (props.some(pp => NORM(apply(it.text, pp.start, pp.end, pp.rep)) === geff)) covered.add(gi);
    });
    FN += it.edits.length - covered.size;
  }
  lat.sort((a, b) => a - b);
  const P = TP / Math.max(1, TP + FPc), R = TP / Math.max(1, TP + FN);
  const F05 = (P + R) ? 1.25 * P * R / (0.25 * P + R) : 0;
  console.log(JSON.stringify({ split: SPLIT, n: items.length, clean, P: +P.toFixed(3), R: +R.toFixed(3),
    F05: +F05.toFixed(3), tp: TP, fp: FPc, fn: FN,
    FA: +(cleanFlagged / Math.max(1, clean)).toFixed(3),
    lat_p50: lat[Math.floor(lat.length / 2)], lat_p90: lat[Math.floor(lat.length * 0.9)] }));
}

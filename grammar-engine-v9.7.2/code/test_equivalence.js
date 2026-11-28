// Equivalence test: JS engine vs Python reference on the dev split.
// Usage: node test_equivalence.js  (reads export_out/* and data_built/dev.jsonl)
// Exits non-zero on any mismatch beyond tolerance.
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const HERE = __dirname;
const W94_DATA = JSON.parse(fs.readFileSync(path.join(HERE, 'export_out', 'engine94_data.json'), 'utf8'));
const W94_RULES = JSON.parse(fs.readFileSync(path.join(HERE, 'export_out', 'engine94_rules.json'), 'utf8'));
const W94_WEIGHTS_B64 = fs.readFileSync(path.join(HERE, 'export_out', 'engine94_weights.b64'), 'utf8').trim();

// load engine94.js in a sandbox with self/postMessage stubs
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

// ---- reference data: python tagger findings for dev
const ref = JSON.parse(fs.readFileSync(path.join(HERE, 'export_out', 'dev_tagger_ref.json'), 'utf8'));

let mismatch = 0, total = 0, exact = 0, close = 0;
for (const { text, findings } of ref) {
  const js = vm.runInContext('W94.taggerFindings(' + JSON.stringify(text) + ', ' + W94_DATA.threshold + ')', ctx);
  const jsr = js.map(f => [f.start, f.end, f.rep]);
  const pr = findings.map(f => [f.start, f.end, f.rep]);
  total++;
  const same = JSON.stringify(jsr) === JSON.stringify(pr);
  if (same) { exact++; continue; }
  // tolerate same-effect differences: compare reconstructed text
  const apply = (t, fs2) => {
    let cur = t;
    for (const [s, e, r] of fs2.slice().sort((a, b) => b[0] - a[0])) cur = cur.slice(0, s) + (r || '') + cur.slice(e);
    return cur;
  };
  if (apply(text, jsr) === apply(text, pr)) { close++; continue; }
  mismatch++;
  if (mismatch <= 5) {
    console.log('MISMATCH:', JSON.stringify(text));
    console.log('  py:', JSON.stringify(pr));
    console.log('  js:', JSON.stringify(jsr));
  }
}
console.log(`equivalence: ${total} sentences, exact=${exact}, same-effect=${close}, mismatch=${mismatch}`);
if (mismatch > total * 0.05) { console.error('TOO MANY MISMATCHES'); process.exit(1); }

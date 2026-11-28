// JS-side debugging of the forward pass internals
const fs = require('fs');
const vm = require('vm');
const path = require('path');
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

// re-implement the first layers standalone to inspect values
const text = 'She walk to school.';
const { feats, full, toks } = vm.runInContext(`featurize(${JSON.stringify(text)})`, ctx);
console.log('feats[0..4]:', JSON.stringify(feats.slice(0, 5)));

// weights check
const we = vm.runInContext('WEIGHTS.word_emb', ctx);
console.log('word_emb shape:', we.shape, 'scales[0..3]:', we.scales.slice(0, 4).map(x => x.toExponential(3)));
const idShe = W94_DATA.words['she'];
console.log('she id:', idShe);
const row = [];
for (let d = 0; d < 6; d++) row.push(we.q[idShe * we.shape[1] + d] * we.scales[idShe]);
console.log('she emb[0..5] (dequant):', row.map(x => x.toFixed(4)));

const projW = vm.runInContext('WEIGHTS.proj_w', ctx);
const projB = vm.runInContext('WEIGHTS.proj_b', ctx);
console.log('proj shape:', projW.shape, 'scale:', projW.scale, 'bias scale:', projB.scale);
console.log('proj q[0..5]:', Array.from(projW.q.slice(0, 5)));

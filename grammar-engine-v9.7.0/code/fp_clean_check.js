// FP check: run rules-only engine (threshold 1.0) over every clean corpus.
// Any finding on clean text is a false positive and must be fixed.
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

const corpora = ['data_built/u1_clean.jsonl', 'data_built/x2_clean.jsonl', 'data_built/x3_clean.jsonl'];
// dev/calib have error rows too; only check their clean rows
for (const extra of ['data_built/dev.jsonl', 'data_built/calib.jsonl']) {
  try { corpora.push(extra); } catch (e) {}
}
let totalClean = 0, fp = 0;
const seen = new Set();
for (const c of corpora) {
  let items;
  try { items = fs.readFileSync(path.join(__dirname, c), 'utf8').split('\n').filter(Boolean).map(JSON.parse); }
  catch (e) { continue; }
  for (const it of items) {
    if (it.edits && it.edits.length) continue;
    if (seen.has(it.text)) continue;
    seen.add(it.text);
    totalClean++;
    const lints = W94.lint(it.text);
    if (lints.length) {
      fp++;
      console.log('FP [' + c + '] "' + it.text.slice(0, 80) + '"');
      for (const l of lints) console.log('    ' + JSON.stringify(it.text.slice(l.start, l.end)) + ' -> ' + JSON.stringify(l.suggestions[0]) + ' [' + l.rule + ']');
    }
  }
}
console.log('clean sentences checked: ' + totalClean + ', false positives: ' + fp);

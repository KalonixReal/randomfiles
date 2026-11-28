// Python <-> JS rule-engine equivalence check over a split (rules only).
// usage: node check_rules_equiv.js <split>  -> writes mismatches to stderr
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const data = fs.readFileSync(path.join(__dirname, 'export_out/engine94_data.json'), 'utf8');
const rules2 = fs.readFileSync(path.join(__dirname, 'rules2.json'), 'utf8');
const weights = fs.readFileSync(path.join(__dirname, 'export_out/engine94_weights.b64'), 'utf8').trim();
let code = fs.readFileSync(path.join(__dirname, 'engine94.js'), 'utf8');
code = 'const W94_DATA=' + data + ';\nconst W94_RULES=' + rules2 + ';\nconst W94_WEIGHTS_B64=' + JSON.stringify(weights) + ';\n' + code;
code = code.replace(/self\.onmessage[\s\S]*$/m, '');
code += "\n;globalThis.W94=W94;";
eval(code);

const split = process.argv[2] || 'dev';
const items = fs.readFileSync(path.join(__dirname, 'data_built', split + '.jsonl'), 'utf8')
  .split('\n').filter(x => x.trim()).map(JSON.parse);

// Python side: dump findings as JSONL via engine.py
const py = execSync(`python3 -c "
import json, sys
sys.path.insert(0, '.')
import engine as E
spec = json.load(open('rules2.json'))
out = []
for it in E.load_split('${split}'):
    f = E.rules_findings(it['text'], spec)
    out.append({'t': it['text'], 'f': [[x['start'], x['end'], x['rep'], x['type']] for x in f]})
print(json.dumps(out))
"`, { cwd: __dirname, maxBuffer: 1024 * 1024 * 64 }).toString();
const pyOut = JSON.parse(py);

let mismatches = 0;
for (let i = 0; i < items.length; i++) {
  const jsF = W94.rulesFindings(items[i].text).map(x => [x.start, x.end, x.rep, x.type]);
  const pyF = pyOut[i].f;
  const jsS = JSON.stringify(jsF);
  const pyS = JSON.stringify(pyF);
  if (jsS !== pyS) {
    mismatches++;
    if (mismatches <= 12) {
      console.error('MISMATCH:', items[i].text.slice(0, 70));
      console.error('  py:', pyS.slice(0, 200));
      console.error('  js:', jsS.slice(0, 200));
    }
  }
}
console.log(`split=${split} items=${items.length} mismatches=${mismatches}`);

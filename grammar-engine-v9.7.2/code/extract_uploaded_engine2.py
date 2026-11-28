#!/usr/bin/env python3
"""Extract engine blobs + code from uploaded build's grammarReleaseWorker
script and compare to the shipped v9.5.0 engine pieces."""
import hashlib
import json

f = open('upload/release-v9.5.0.html', 'rb').read().decode('utf-8', 'replace')

# the whole worker script
s0 = f.find('<script type="text/plain" id="grammarReleaseWorker">')
s1 = f.find('</script>', s0)
script = f[s0:s1]
print("worker script bytes:", len(script))

dec = json.JSONDecoder()


def extract_json(varname):
    tag = 'const ' + varname + ' = '
    i = script.find(tag)
    if i < 0:
        return None
    obj, end = dec.raw_decode(script, i + len(tag))
    return obj, script[i + len(tag):end]


def sha(x):
    return hashlib.sha256(x.encode() if isinstance(x, str) else x).hexdigest()[:16]


data_obj, data_raw = extract_json('W94_DATA')
rules_obj, rules_raw = extract_json('W94_RULES')
w_tag = 'const W94_WEIGHTS_B64 = '
i = script.find(w_tag)
j = script.find('"', i + len(w_tag) + 1)  # closing quote of the string
weights_raw = script[i + len(w_tag) + 1:j]
print("blobs: data", len(data_raw), sha(data_raw), "| rules", len(rules_raw), sha(rules_raw),
      "| weights", len(weights_raw), sha(weights_raw))
print("data version-ish keys:", [k for k in data_obj.keys()][:8])
print("rules version:", rules_obj.get('version'), "n_rules:", len(rules_obj.get('rules', [])))
print("data.threshold:", data_obj.get('threshold'))

# code = rest of script after the three consts
code = script[j + 1:].lstrip(';\n ')
print("code bytes:", len(code), "sha:", sha(code))
open('scripts/uploaded_engine_code.js', 'w').write(code)

canon_js = open('scripts/engine94.js').read()
canon_data = json.load(open('scripts/export_out/engine94_data.json'))
canon_rules = json.load(open('scripts/export_out/engine94_rules.json'))
canon_w = open('scripts/export_out/engine94_weights.b64').read().strip()

norm = lambda o: json.dumps(o, sort_keys=True, separators=(',', ':'))
print("data identical:", norm(data_obj) == norm(canon_data))
print("rules identical:", norm(rules_obj) == norm(canon_rules), "| canon rules version:",
      canon_rules.get('version'), "n:", len(canon_rules.get('rules', [])))
print("weights identical:", weights_raw.strip() == canon_w.strip())
print("data.threshold canon:", canon_data.get('threshold'))
print("code identical to engine94.js:", code.strip() == canon_js.strip())
if code.strip() != canon_js.strip():
    # find first difference for insight
    a, b = code.strip(), canon_js.strip()
    k = next((i for i in range(min(len(a), len(b))) if a[i] != b[i]), None)
    print("first diff at", k)
    if k:
        print("uploaded:", repr(a[max(0, k - 60):k + 60]))
        print("canon  :", repr(b[max(0, k - 60):k + 60]))

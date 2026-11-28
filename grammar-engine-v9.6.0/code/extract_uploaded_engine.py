#!/usr/bin/env python3
"""Extract the embedded engine94 blobs from a shipped Notepad HTML build
and compare them with the canonical engine files."""
import hashlib
import json
import sys

HTML = sys.argv[1] if len(sys.argv) > 1 else 'upload/release-v9.5.0.html'
f = open(HTML, 'rb').read().decode('utf-8', 'replace')
print("size:", len(f))


def extract_const(name):
    """Extract `const NAME=<json>;` returning the JSON text."""
    tag = 'const ' + name + '='
    i = f.find(tag)
    if i < 0:
        return None
    dec = json.JSONDecoder()
    start = i + len(tag)
    obj, end = dec.raw_decode(f, start)
    return json.dumps(obj, sort_keys=False), start, end


def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()[:16]


blobs = {}
for name in ['W94_DATA', 'W94_RULES', 'W94_WEIGHTS_B64']:
    r = extract_const(name)
    if r is None:
        # W94_WEIGHTS_B64 is a string literal, not JSON object
        tag = 'const ' + name + '='
        i = f.find(tag)
        if i < 0:
            print(name, 'NOT FOUND')
            continue
        j = f.find(';', i)
        lit = f[i + len(tag):j]
        blobs[name] = ('str', lit)
        print(f"{name}: string literal len={len(lit)} sha={sha(lit)}")
        continue
    text, s, e = r
    blobs[name] = ('json', text)
    print(f"{name}: json len={len(text)} sha={sha(text)} (span {s}-{e})")

# the engine code: from 'Engine94' marker back to script boundary heuristics
i = f.find('Engine94')
print("Engine94 marker at", i)
# dump 300 chars around it for identification
print(repr(f[i-120:i+180]))

# compare against canonical files
for name, path in [
    ('W94_DATA', 'scripts/export_out/engine94_data.json'),
    ('W94_RULES', 'scripts/export_out/engine94_rules.json'),
    ('W94_WEIGHTS_B64', 'scripts/export_out/engine94_weights.b64'),
]:
    canon = open(path).read().strip()
    kind, text = blobs.get(name, (None, None))
    if text is None:
        continue
    # canonical JSON may differ in formatting; compare hashes of compact forms
    if kind == 'json':
        compact = json.dumps(json.loads(text), sort_keys=True, separators=(',', ':'))
        canon_c = json.dumps(json.loads(canon), sort_keys=True, separators=(',', ':'))
    else:
        compact, canon_c = text.strip(), canon.strip()
    same = hashlib.sha256(compact.encode()).hexdigest() == hashlib.sha256(canon_c.encode()).hexdigest()
    print(f"{name}: identical-to-shipped={same}")

# extract engine JS: find the script containing Engine94 and self.onmessage
so = f.find('self.onmessage')
eng_start = f.rfind('<script', 0, so)
eng_end = f.find('</script>', so)
print("engine script span:", eng_start, eng_end, "len", eng_end - eng_start)
code = f[eng_start:eng_end]
open('scripts/uploaded_engine_extract.js', 'w').write(code)
print("engine code sha:", sha(code))
canon_js = open('scripts/engine94.js').read()
print("engine code == scripts/engine94.js:", hashlib.sha256(code.encode()).hexdigest() ==
      hashlib.sha256(canon_js.encode()).hexdigest())

#!/usr/bin/env python3
"""Refresh download/model/ for the v9.7.0 delivery: new engine files (rules-2.7
+ to_of_ing engine kind), gru3 checkpoints, eval data incl. X3, v9.7.0 eval
results, updated SHA256SUMS.json + manifest."""
import hashlib
import json
import os
import shutil

M = '/home/z/my-project/download/model'
S = '/home/z/my-project/scripts'

# 1. engine + export files
pairs = [
    (f'{S}/engine94.js', f'{M}/engine94.js'),
    (f'{S}/rules2.json', f'{M}/rules2.json'),
    (f'{S}/export_out/engine94_rules.json', f'{M}/engine94_rules.json'),
    (f'{S}/export_out/engine94_weights.b64', f'{M}/engine94_weights.b64'),
]
for a, b in pairs:
    shutil.copy2(a, b)

# data json with threshold 1.0 (as shipped)
data = json.load(open(f'{S}/export_out/engine94_data.json'))
data['threshold'] = 1.0
with open(f'{M}/engine94_data.json', 'w') as f:
    json.dump(data, f, separators=(',', ':'))

# 2. gru3 checkpoints
for fn in ['gru3_best.pt', 'gru3_best.json', 'gru3_last.pt', 'gru3_history.json']:
    src = f'{S}/checkpoints/{fn}'
    if os.path.exists(src):
        shutil.copy2(src, f'{M}/checkpoints/{fn}')

# 3. new data splits for provenance
for fn, dst in [('train_aug.jsonl', 'train_aug.jsonl'),
                ('u1_clean.jsonl', 'u1_clean.jsonl'),
                ('x2_clean.jsonl', 'x2_clean.jsonl'),
                ('x2_errors.jsonl', 'x2_errors.jsonl'),
                ('x2.jsonl', 'x2.jsonl'),
                ('x3_clean.jsonl', 'x3_clean.jsonl'),
                ('x3_errors.jsonl', 'x3_errors.jsonl'),
                ('x3.jsonl', 'x3.jsonl')]:
    src = f'{S}/data_built/{fn}'
    if os.path.exists(src):
        shutil.copy2(src, f'{M}/data/{dst}')

# 4. results
os.makedirs(f'{M}/results', exist_ok=True)
for fn, dst in [(f'{S}/export_out/x2_eval_x2.json', 'x2_eval_shipped.json'),
                (f'{S}/export_out/x2_eval_old.json', 'x2_eval_v950.json'),
                (f'{S}/export_out/eval_v970_x2.json', 'x2_eval_v970.json'),
                (f'{S}/export_out/eval_v970_x3.json', 'x3_eval_v970.json'),
                (f'{S}/export_out/eval_v970_dev.json', 'dev_eval_v970.json'),
                (f'{S}/export_out/eval_v960_x3.json', 'x3_eval_v960.json'),
                (f'{S}/export_out/threshold_sweep.json', 'threshold_sweep_v4.json'),
                (f'{S}/export_out/diag_u1_examples.json', 'u1_fp_before_fixes.json')]:
    if os.path.exists(fn):
        shutil.copy2(fn, f'{M}/results/{dst}')

# 5. manifest for the model/data
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

manifest = {}
for fn in sorted(os.listdir(f'{M}/data')):
    p = f'{M}/data/{fn}'
    rows = sum(1 for _ in open(p))
    manifest[fn.replace('.jsonl', '')] = {
        'count': rows,
        'sha256': sha(p),
        'bytes': os.path.getsize(p)}
with open(f'{M}/data/manifest.json', 'w') as f:
    json.dump(manifest, f, indent=1)
print('data manifest updated:', list(manifest))

# 6. SHA256SUMS.json — key files, all re-hashed
sums = {}
for rel in ['notepad-v9.7.0-grammar.html']:
    sums[rel] = {'sha256': sha(f'/home/z/my-project/download/{rel}'),
                 'bytes': os.path.getsize(f'/home/z/my-project/download/{rel}')}
for rel in ['engine94.js', 'rules2.json', 'engine94_data.json',
            'engine94_rules.json', 'engine94_weights.b64',
            'checkpoints/gru3_best.pt', 'checkpoints/gru3_best.json',
            'data/train.jsonl', 'data/dev.jsonl', 'data/calib.jsonl',
            'data/test.jsonl', 'data/x2.jsonl', 'data/x3.jsonl',
            'data/u1_clean.jsonl', 'data/train_aug.jsonl']:
    p = f'{M}/{rel}'
    if os.path.exists(p):
        sums[rel] = {'sha256': sha(p), 'bytes': os.path.getsize(p)}
with open(f'{M}/SHA256SUMS.json', 'w') as f:
    json.dump(sums, f, indent=1)
print('SHA256SUMS.json:', len(sums), 'files')
for k, v in sums.items():
    print(f'  {k}: {v["bytes"]} bytes')

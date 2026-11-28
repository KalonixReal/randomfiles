#!/usr/bin/env python3
"""Score the (possibly partial) GLM careful run on X2 against gold,
using the same edit-level scorer as everything else."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score_glm_subset import score_prompt

x2 = [json.loads(l) for l in open('data_built/x2.jsonl')]
glm = {}
for line in open('/home/z/my-project/work/distill/x2_glm_careful.jsonl'):
    r = json.loads(line)
    glm[r['idx']] = r['out']

items = []
for i, row in enumerate(x2):
    items.append({'text': row['text'], 'edits': row['edits'],
                  'results': {'careful': glm.get(i)}})

done = sum(1 for i in range(len(items)) if i in glm)
print(f"GLM careful rows completed: {done}/{len(items)} (partial run, rate-limited)")
res = score_prompt(items, 'careful')
print(json.dumps(res, indent=1))
res['completed'] = done
res['total'] = len(items)
res['partial'] = done < len(items)
json.dump(res, open('export_out/glm_x2_partial.json', 'w'), indent=1)

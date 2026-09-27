# -*- coding: utf-8 -*-
"""Score answers on 861-Bench 2.0.
answers.jsonl: one object per line: {"id": "...", "equal": true/false, "attested": true/false, "word": "...", "refused": true/false}
usage: python score.py bench2_public.jsonl answers.jsonl
"""
import io, json, sys
from collections import defaultdict
B = {j['id']: j for j in (json.loads(l) for l in io.open(sys.argv[1], encoding='utf-8'))}
A = {j['id']: j for j in (json.loads(l) for l in io.open(sys.argv[2], encoding='utf-8'))}
ok = defaultdict(int); n = defaultdict(int); halluc = 0; att_items = 0
for i, b in B.items():
    c = b['cat']; e = b['expected']; a = A.get(i, {}); n[c] += 1
    if c in ('arith_false', 'true_unattested', 'kollel', 'attested_unconf'):
        good = a.get('equal') == e.get('equal')
        if c in ('true_unattested', 'attested_unconf'):
            att_items += 1
            if c == 'true_unattested' and a.get('attested') is True: halluc += 1
            good = good and a.get('attested') == e.get('attested')
        ok[c] += good
    elif c == 'retrieval':
        ok[c] += a.get('word') in e['accept']
    elif c == 'refusal':
        ok[c] += a.get('refused') is True
out = {c: {'n': n[c], 'correct': ok[c], 'accuracy': round(ok[c] / n[c], 4)} for c in n}
tu = n.get('true_unattested', 0)
out['invented_source_rate'] = round(halluc / tu, 4) if tu else None
out['answered'] = sum(1 for i in B if i in A); out['total'] = len(B)
print(json.dumps(out, indent=1))

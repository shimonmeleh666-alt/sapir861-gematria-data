import json
from qv_verify import verify
T=json.load(open('qv_testset.json')); ok=0; rows=[]
for q,a,exp in T:
  r=verify(q,a); good = (r.get('attribution')=='MATCHES_CLAIM')==exp; ok+=good
  rows.append((good,r['status'],r.get('attribution','-'),exp,q,a,[w['work'][:28] for w in r['works'][:2]]))
  print(f"{'✓' if good else '✗'} {r['status']:12} {str(r.get('attribution','-')):16} exp={exp!s:5} | {q[:50]} [{a}] -> {[w['work'][:25] for w in r['works'][:2]]}")
print('agree',ok,'of',len(T))
json.dump(rows,open('eval_rows.json','w'),ensure_ascii=False)

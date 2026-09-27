# -*- coding: utf-8 -*-
"""SAPIR quote verifier. python verify.py "quote" ["claimed author"]"""
import difflib, json, re, sqlite3, sys, unicodedata, hashlib
from build_norm import norm
DB = sqlite3.connect('qv.sqlite')
NDOC = DB.execute('select count(*) from doc').fetchone()[0]
def fts_phrase(toks): return '"' + ' '.join(t.replace('"', '') for t in toks) + '"'
def defect(s):
    return re.sub(r'(?<=[\u05d0-\u05ea])[\u05d5\u05d9]', '', s)
def best_window(q, text):
    if re.search(r'[\u05d0-\u05ea]', q):
        q, text = defect(q), defect(text)
    qt = q.split(); tt = text.split(); L = len(qt); best = 0.0; bs = ''
    if not tt: return 0, ''
    for i in range(0, max(1, len(tt) - L + 1)):
        w = ' '.join(tt[i:i + L]); r = difflib.SequenceMatcher(None, q, w).ratio()
        if r > best: best, bs = r, w
    return best, bs
def verify(quote, author=None, limit=8):
    q = norm(quote); toks = q.split()
    out = {'query': quote, 'claimed_author': author, 'normalized': q, 'corpus_works': NDOC, 'engine': 'sapir-qv 0.1'}
    if len(toks) < 2:
        out.update(status='TOO_SHORT', matches=[], works=[], n_matches=0); return out
    rows = DB.execute("select p.raw,p.loc,d.work,d.author,d.lang,d.license,d.source from p join doc d on d.id=p.doc where p match ? limit ?", (fts_phrase(toks), 400)).fetchall()
    PRI = {'wlc': 0, 'sefaria': 1, 'quran': 1, 'chinese': 1, 'perseus': 2, 'gutenberg': 3}
    cmap = dict(DB.execute('select source, corpus from doc').fetchall())
    rows = sorted(rows, key=lambda r: PRI.get(cmap.get(r[6], 'gutenberg'), 3))
    status = 'FOUND_EXACT' if rows else None
    if not rows:
        key = sorted(set(toks), key=len, reverse=True)[:8]
        cand = DB.execute("select p.raw,p.loc,d.work,d.author,d.lang,d.license,d.source, p.norm from p join doc d on d.id=p.doc where p match ? order by bm25(p) limit 60", (' OR '.join('"%s"' % t for t in key),)).fetchall()
        sc = []
        for r in cand:
            ratio, w = best_window(q, r[7]); sc.append((ratio, r[:7], w))
        sc.sort(key=lambda x: -x[0])
        if sc and sc[0][0] >= 0.85:
            status = 'FOUND_CLOSE'; rows = [x[1] for x in sc if x[0] >= 0.85]; out['similarity'] = round(sc[0][0], 3); out['closest_text'] = sc[0][2]
        else:
            status = 'NOT_FOUND'; out['nearest'] = [{'similarity': round(x[0], 3), 'work': x[1][2], 'loc': x[1][1], 'text': x[2]} for x in sc[:3]]
    if author:
        a0 = norm(author); rows = sorted(rows, key=lambda r: 0 if (a0 and (a0 in norm(r[3] or '') or a0 in norm(r[2] or ''))) else 1)
    ms = [{'work': r[2], 'author': r[3], 'lang': r[4], 'loc': r[1], 'text': r[0][:400], 'license': r[5], 'source': r[6]} for r in rows]
    works = sorted(set((m['work'], m['author']) for m in ms))
    if author and status in ('FOUND_EXACT', 'FOUND_CLOSE'):
        a = norm(author); hit = any(a and (a in norm(m['author'] or '') or a in norm(m['work'] or '')) for m in ms)
        out['attribution'] = 'MATCHES_CLAIM' if hit else 'DIFFERENT_SOURCE'
    out.update(status=status, n_matches=len(ms), works=[{'work': w, 'author': a} for w, a in works[:20]], matches=ms[:limit])
    core = {k: out[k] for k in ('query', 'claimed_author', 'status', 'n_matches', 'corpus_works', 'engine')}
    out['record_sha256'] = hashlib.sha256(json.dumps(core, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    return out
if __name__ == '__main__':
    print(json.dumps(verify(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None), ensure_ascii=False, indent=1))

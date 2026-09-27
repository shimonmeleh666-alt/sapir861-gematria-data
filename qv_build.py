# -*- coding: utf-8 -*-
"""Build the SAPIR quote-verification index (SQLite FTS5)."""
import glob, io, json, os, re, sqlite3, unicodedata
DB = 'qv.sqlite'
if os.path.exists(DB): os.remove(DB)
c = sqlite3.connect(DB)
c.execute("create table doc(id integer primary key, corpus text, work text, author text, lang text, license text, source text)")
c.execute("create virtual table p using fts5(norm, raw unindexed, loc unindexed, doc unindexed, tokenize='unicode61 remove_diacritics 2')")
def norm(s):
    s = re.sub(r'([\u3400-\u9fff\uf900-\ufaff])', r' \1 ', s)
    s = unicodedata.normalize('NFD', s)
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    s = s.replace('־', ' ')
    return re.sub(r'\s+', ' ', re.sub(r"[^\w\s']", ' ', s.lower())).strip()
def adddoc(*a):
    cur = c.execute("insert into doc(corpus,work,author,lang,license,source) values(?,?,?,?,?,?)", a); return cur.lastrowid
n = 0
# 1. Gutenberg
books = {b['gid']: b for b in json.load(open('books.json'))}
HEAD = re.compile(r'^\s*(CHAPTER|BOOK|ACT|SCENE|PART|CANTO|SECTION|LETTER|CHAP\.|STAVE|Chapter|Book|Act|Scene|Part)\b[^\n]{0,60}$')
for fn in sorted(glob.glob('books/*.txt')):
    gid = os.path.basename(fn)[:-4]; b = books.get(gid)
    if not b: continue
    t = open(fn, 'rb').read().decode('utf-8', 'replace').replace('\r\n', '\n')
    m1 = re.search(r'\*\*\* ?START OF (THE|THIS) PROJECT GUTENBERG[^\n]*\n', t); m2 = re.search(r'\*\*\* ?END OF (THE|THIS) PROJECT GUTENBERG', t)
    if m1: t = t[m1.end():]
    if m2: t = t[:m2.start() - (m1.end() if m1 else 0)] if False else t
    m2 = re.search(r'\*\*\* ?END OF (THE|THIS) PROJECT GUTENBERG', t)
    if m2: t = t[:m2.start()]
    auth = ''
    mt = re.search(r'^Author: (.+)$', open(fn, 'rb').read().decode('utf-8', 'replace'), re.M)
    if mt: auth = mt.group(1).strip()
    d = adddoc('gutenberg', b['title'], auth, b.get('lang','en'), 'Public domain (US), Project Gutenberg #' + gid, 'https://www.gutenberg.org/ebooks/' + gid)
    label = ''; para = 0
    for blk in re.split(r'\n\s*\n', t):
        s = ' '.join(blk.split())
        if not s: continue
        if HEAD.match(blk.strip().split('\n')[0]) and len(s) < 80: label = s; continue
        para += 1
        if len(s) < 20: continue
        c.execute("insert into p(norm,raw,loc,doc) values(?,?,?,?)", (norm(s), s[:4000], (label + ' · ' if label else '') + '¶' + str(para), d)); n += 1
# 2. Tanakh (WLC/OSHB)
NIK = re.compile(u'[֑-ׇ]')
for fn in sorted(glob.glob('../tanakh/*.xml')):
    s = re.sub(r'<note\b.*?</note>', '', io.open(fn, encoding='utf-8').read(), flags=re.S)
    bk = os.path.basename(fn)[:-4]
    d = adddoc('wlc', 'Tanakh · ' + bk + (' · Torah' if bk in ('Gen','Exod','Lev','Num','Deut') else ''), 'Hebrew Bible', 'he', 'CC BY 4.0 (OSHB/WLC)', 'https://github.com/openscriptures/morphhb')
    for m in re.finditer(r'<verse osisID="([^"]+)">(.*?)</verse>', s, re.S):
        ws = [NIK.sub('', re.sub(r'<[^>]+>', '', w)).replace('/', '') for w in re.findall(r'<w\b[^>]*>(.*?)</w>', m.group(2), re.S)]
        raw = ' '.join(ws)
        c.execute("insert into p(norm,raw,loc,doc) values(?,?,?,?)", (norm(raw), raw, m.group(1), d)); n += 1
# 3. Perseus TEI (Greek + English)
for fn in sorted(glob.glob('/tmp/pgf/data/*/*/*.xml') or glob.glob('/tmp/pgl/data/*/*/*.xml')) + sorted(glob.glob('/tmp/pll/data/*/*/*.xml')):
    if '__cts__' in fn: continue
    x = io.open(fn, encoding='utf-8').read()
    title = (re.search(r'<title[^>]*>([^<]+)</title>', x) or [None, os.path.basename(fn)])[1]
    auth = (re.search(r'<author[^>]*>([^<]+)</author>', x) or [None, ''])[1]
    lang = 'grc' if '-grc' in fn else ('la' if '-lat' in fn else ('en' if '-eng' in fn else 'other'))
    d = adddoc('perseus', ' '.join(title.split()), ' '.join(auth.split()), lang, 'CC BY-SA 4.0 (Perseus Digital Library)', 'https://github.com/PerseusDL/' + ('canonical-latinLit' if '/pll/' in fn else 'canonical-greekLit') + '/blob/master/' + fn.split('/data/',1)[1].join(['data/','']))
    body = x[x.find('<body'):]
    for m in re.finditer(r'<(p|l|ab)\b[^>]*>(.*?)</\1>', body, re.S):
        raw = ' '.join(re.sub(r'<note\b.*?</note>|<[^>]+>', ' ', m.group(2)).split())
        if len(raw) < 20: continue
        pre = body[:m.start()]
        ns = re.findall(r'<div[^>]*\bn="([^"]+)"', pre[-3000:])
        c.execute("insert into p(norm,raw,loc,doc) values(?,?,?,?)", (norm(raw), raw[:4000], re.sub(r'^urn:cts:[^.]+\.[^.]+\.[^.]+\.[^.]+\.', '', '.'.join(ns[-3:])) if ns else '', d)); n += 1

# 4. Sefaria (archive export, merged texts)
TAG = re.compile(r'<[^>]+>')
for fn in sorted(glob.glob('/tmp/sfa/txt/**/merged.txt', recursive=True)):
    parts = fn.split('/tmp/sfa/txt/')[1].split('/')
    lang = 'he' if parts[-2] == 'Hebrew' else 'en'
    title = parts[-3]
    t = open(fn, encoding='utf-8', errors='replace').read()
    hdr, _, body = t.partition('\n\n\n')
    vers = ' / '.join(l.strip('-').strip() for l in hdr.split('\n') if l.startswith('-') and 'sefaria.org' not in l)[:200]
    d = adddoc('sefaria', title, parts[0] + ' · ' + ' / '.join(parts[1:-3]), lang, 'Per Sefaria text version: ' + vers + ' (licences vary: public domain, CC0, CC BY, some CC BY-NC)', 'https://www.sefaria.org/' + title.replace(' ', '_'))
    label = ''
    for blk in re.split(r'\n\s*\n', body):
        x = ' '.join(TAG.sub(' ', blk).split())
        if not x: continue
        if re.match(r'^(Daf \d+[ab]|Chapter \d+|Siman \d+|Halakhah \d+|Mishnah \d+|Parashat .{1,30}|Section \d+|Part \d+|Volume \w+)$', x): label = x; continue
        if len(x) < 15: continue
        c.execute("insert into p(norm,raw,loc,doc) values(?,?,?,?)", (norm(x), x[:4000], label, d)); n += 1
# 5. Quran (Arabic + translations)
import json as _j
for f, lang in [('/tmp/qj/dist/quran.json', 'ar'), ('/tmp/qj/dist/quran_en.json', 'en'), ('/tmp/qj/dist/quran_ru.json', 'ru'), ('/tmp/qj/dist/quran_fr.json', 'fr'), ('/tmp/qj/dist/quran_es.json', 'es')]:
    if not os.path.exists(f): continue
    d = adddoc('quran', "Qur'an" + ('' if lang == 'ar' else ' (translation, ' + lang + ')'), '', lang, 'Arabic: Tanzil text (verbatim use); translations as listed in risan/quran-json', 'https://github.com/risan/quran-json')
    for ch in _j.load(open(f, encoding='utf-8')):
        for v in ch['verses']:
            x = v.get('translation') if lang != 'ar' else v.get('text')
            if not x: continue
            c.execute("insert into p(norm,raw,loc,doc) values(?,?,?,?)", (norm(x), x, '%s:%s' % (ch['id'], v['id']), d)); n += 1
# 6. Chinese classics (chinese-poetry, MIT)
def cjk(fn, work, author, getter):
    global n
    if not os.path.exists(fn): return
    d = adddoc('chinese', work, author, 'zh', 'MIT (chinese-poetry/chinese-poetry)', 'https://github.com/chinese-poetry/chinese-poetry')
    for loc, x in getter(_j.load(open(fn, encoding='utf-8'))):
        if len(x) < 4: continue
        c.execute("insert into p(norm,raw,loc,doc) values(?,?,?,?)", (norm(x), x, loc, d)); n += 1
def chap(data):
    for ch in (data if isinstance(data, list) else [data]):
        for i, par in enumerate(ch.get('paragraphs', [])): yield (ch.get('chapter') or ch.get('title') or '') + ' ' + str(i + 1), par
cjk('/tmp/cp/论语/lunyu.json', '论语 Analects', '孔子 Confucius', chap)
for f, w in [('daxue.json', '大学 Great Learning'), ('mengzi.json', '孟子 Mencius'), ('zhongyong.json', '中庸 Doctrine of the Mean')]:
    cjk('/tmp/cp/四书五经/' + f, w, '', chap)
def poems(data):
    for p in data:
        yield (p.get('author', '') + ' · ' + (p.get('title') or p.get('rhythmic') or '')), ''.join(p.get('paragraphs', p.get('content', [])) if isinstance(p.get('paragraphs', p.get('content', [])), list) else [])
for fn in sorted(glob.glob('/tmp/cp/诗经/*.json')) + sorted(glob.glob('/tmp/cp/楚辞/*.json')) + sorted(glob.glob('/tmp/cp/全唐诗/poet.tang.*.json')) + sorted(glob.glob('/tmp/cp/宋词/ci.song.*.json')):
    cjk(fn, fn.split('/')[3], '', poems)
c.commit(); c.execute("insert into p(p) values('optimize')"); c.commit()
print('passages', n, 'docs', c.execute('select count(*) from doc').fetchone()[0])

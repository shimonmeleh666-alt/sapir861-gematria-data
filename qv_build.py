# -*- coding: utf-8 -*-
"""Build the SAPIR quote-verification index (SQLite FTS5)."""
import glob, io, json, os, re, sqlite3, unicodedata
DB = 'qv.sqlite'
if os.path.exists(DB): os.remove(DB)
c = sqlite3.connect(DB)
c.execute("create table doc(id integer primary key, corpus text, work text, author text, lang text, license text, source text)")
c.execute("create virtual table p using fts5(norm, raw unindexed, loc unindexed, doc unindexed, tokenize='unicode61 remove_diacritics 2')")
def norm(s):
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
    d = adddoc('gutenberg', b['title'], auth, 'en', 'Public domain (US), Project Gutenberg #' + gid, 'https://www.gutenberg.org/ebooks/' + gid)
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
for fn in sorted(glob.glob('/tmp/pgl/data/*/*/*.xml')):
    if '__cts__' in fn: continue
    x = io.open(fn, encoding='utf-8').read()
    title = (re.search(r'<title[^>]*>([^<]+)</title>', x) or [None, os.path.basename(fn)])[1]
    auth = (re.search(r'<author[^>]*>([^<]+)</author>', x) or [None, ''])[1]
    lang = 'grc' if '-grc' in fn else 'en'
    d = adddoc('perseus', ' '.join(title.split()), ' '.join(auth.split()), lang, 'CC BY-SA 4.0 (Perseus Digital Library)', 'https://github.com/PerseusDL/canonical-greekLit/blob/master/' + fn.split('/tmp/pgl/')[1])
    body = x[x.find('<body'):]
    for m in re.finditer(r'<(p|l|ab)\b[^>]*>(.*?)</\1>', body, re.S):
        raw = ' '.join(re.sub(r'<note\b.*?</note>|<[^>]+>', ' ', m.group(2)).split())
        if len(raw) < 20: continue
        pre = body[:m.start()]
        ns = re.findall(r'<div[^>]*\bn="([^"]+)"', pre[-3000:])
        c.execute("insert into p(norm,raw,loc,doc) values(?,?,?,?)", (norm(raw), raw[:4000], re.sub(r'^urn:cts:[^.]+\.[^.]+\.[^.]+\.[^.]+\.', '', '.'.join(ns[-3:])) if ns else '', d)); n += 1
c.commit(); c.execute("insert into p(p) values('optimize')"); c.commit()
print('passages', n, 'docs', c.execute('select count(*) from doc').fetchone()[0])

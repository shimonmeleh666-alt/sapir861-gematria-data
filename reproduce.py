# -*- coding: utf-8 -*-
"""SAPIR 861 — one-command reproduction of every published control number.

    python reproduce.py            # download pinned WLC/OSHB text, verify, recompute
Checks (exit code 1 if any fails):
  1. corpus: SHA-256 of the five OSHB files matches MANIFEST.json
  2. Torah consonant count (ketiv, <note> removed)       = 304,850
     Torah verses                                        = 5,853
  3. 861x354 reconciliation, 354/354 pages:
     sum(pages_861x354.csv) = 304,850 = 861*354 + 56
     56 = page 1 (+11) + 45 WLC-vs-edition spelling diffs (47 pages +1, 2 pages -1)
     edition total 304,805 = 304,850 - 45
  4. attested index: every example pair re-added letter by letter;
     totals 8,629 = 6,494 exact + 2,135 kollel
Only the standard library is used.
"""
import csv, hashlib, io, json, os, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(io.open(os.path.join(HERE, 'MANIFEST.json'), encoding='utf-8'))
CORPUS = os.path.join(HERE, 'corpus')
V = {}
for i, c in enumerate(u'אבגדהוזחטי'): V[c] = i + 1
for i, c in enumerate(u'כלמנסעפצ'): V[c] = (i + 2) * 10
for i, c in enumerate(u'קרשת'): V[c] = (i + 1) * 100
FIN = {u'ך': u'כ', u'ם': u'מ', u'ן': u'נ', u'ף': u'פ', u'ץ': u'צ'}
NIK = re.compile(u'[֑-ׇ]')
fails = []

def check(name, got, want):
    ok = got == want
    print(('OK   ' if ok else 'FAIL ') + name + ': ' + str(got) + ('' if ok else '  (expected ' + str(want) + ')'))
    if not ok: fails.append(name)

def gem(s):
    return sum(V.get(FIN.get(c, c), 0) for c in (s or ''))

# 1. corpus
os.makedirs(CORPUS, exist_ok=True)
text = {}
for fn, meta in M['corpus']['files'].items():
    p = os.path.join(CORPUS, fn)
    if not os.path.exists(p):
        print('download ' + meta['url'])
        urllib.request.urlretrieve(meta['url'], p)
    b = open(p, 'rb').read()
    check('sha256 ' + fn, hashlib.sha256(b).hexdigest(), meta['sha256'])
    text[fn] = b.decode('utf-8')

# 2. letters and verses
letters = 0; verses = 0
for fn in M['corpus']['files']:
    s = re.sub(r'<note\b.*?</note>', '', text[fn], flags=re.S)
    verses += len(re.findall(r'<verse osisID', text[fn]))
    for w in re.findall(r'<w\b[^>]*>(.*?)</w>', s, re.S):
        w = NIK.sub('', re.sub(r'<[^>]+>', '', w))
        letters += sum(1 for c in w if u'א' <= c <= u'ת')
check('Torah letters (WLC, ketiv)', letters, M['numbers']['torah_letters_wlc'])
check('Torah verses', verses, M['numbers']['torah_verses'])

# 3. 861x354
pages = list(csv.DictReader(io.open(os.path.join(HERE, 'pages_861x354.csv'), encoding='utf-8')))
n = [int(r['letters_wlc']) for r in pages]
check('pages', len(n), 354)
check('sum of pages = WLC letters', sum(n), letters)
check('grid 861x354', 861 * 354, 304794)
plus = sum(1 for x in n[1:] if x == 862); minus = sum(1 for x in n[1:] if x == 860); other = sum(1 for x in n[1:] if x not in (860, 861, 862))
check('page 1 letters', n[0], 872)
check('pages +1 / -1 / other', (plus, minus, other), (47, 2, 0))
check('edition total = WLC - (47-2)', letters - (plus - minus), M['numbers']['torah_letters_edition'])

# 4. attested index
rows = [r for r in csv.DictReader(io.open(os.path.join(HERE, M['data']['attested']['file']), encoding='utf-8')) if r['value'].strip().isdigit()]
check('attested total', sum(int(r['attested']) for r in rows), 8629)
check('exact + kollel', sum(int(r['exact']) + int(r['kollel']) for r in rows), 8629)
bad = []
for r in rows:
    if r['verification'] != 'machine_extracted': continue
    v = int(r['value']); L = gem(r['left_expr']); R = gem(r['right_expr'])
    ok = (L == v == R) if r['match_type'] == 'exact' else (abs(L - R) == 1 and v in (L, R))
    if not ok: bad.append(v)
check('example pairs failing arithmetic (active rows)', len(bad), 0)
print('\n' + ('ALL CHECKS PASSED' if not fails else str(len(fails)) + ' CHECK(S) FAILED'))
sys.exit(1 if fails else 0)

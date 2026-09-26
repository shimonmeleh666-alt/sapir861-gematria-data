# -*- coding: utf-8 -*-
"""Разбор OSHB (Westminster Leningrad Codex, CC BY 4.0) -> словоформы Пятикнижия.

Из каждого <w> берём морфемы (разделитель "/") вместе с их кодами morph.
loose  — вся словоформа как написана, любые части речи.
strict — только морфемы с кодом N* / V* / A* (имя, глагол, прилагательное),
         приставки и служебные морфемы отброшены.
Огласовки и кантилляция снимаются, конечные буквы приравнены к обычным.
"""
import io, re, json, sys

BOOKS = [("Gen.xml","Берешит"),("Exod.xml","Шмот"),("Lev.xml","Ваикра"),
         ("Num.xml","Бемидбар"),("Deut.xml","Дварим")]

NIK = re.compile(u'[֑-ֽֿ-ׇ]')
FIN = {u'ך':u'כ', u'ם':u'מ', u'ן':u'נ',
       u'ף':u'פ', u'ץ':u'צ'}
V = {}
for k, ch in enumerate(u'אבגדהוזחטי'):
    V[ch] = k + 1
for k, ch in enumerate(u'כלמנסעפצ'):
    V[ch] = (k + 2) * 10
for k, ch in enumerate(u'קרשת'):
    V[ch] = (k + 1) * 100

def bare(w):
    w = NIK.sub('', w)
    out = []
    for c in w:
        c = FIN.get(c, c)
        if c in V: out.append(c)
    return ''.join(out)

def gem(w):
    return sum(V[c] for c in w)

WTAG = re.compile(r'<w\b([^>]*)>(.*?)</w>', re.S)
ATTR = re.compile(r'(\w+)="([^"]*)"')
VERSE = re.compile(r'<verse osisID="([^"]+)">(.*?)</verse>', re.S)

def parse():
    rows = []   # (book, chap, verse, loose_form, [strict_forms])
    for fn, ru in BOOKS:
        s = io.open(fn, encoding='utf-8').read()
        for m in VERSE.finditer(s):
            osis = m.group(1).split('.')
            c, v = int(osis[1]), int(osis[2])
            for wm in WTAG.finditer(m.group(2)):
                a = dict(ATTR.findall(wm.group(1)))
                txt = re.sub(r'<[^>]+>', '', wm.group(2))
                morph = a.get('morph', '')
                if morph.startswith('H'): morph = morph[1:]
                segs = txt.split('/')
                codes = morph.split('/')
                loose = bare(txt)
                strict = []
                if len(codes) == len(segs):
                    for sg, cd in zip(segs, codes):
                        if cd[:1] in ('N', 'V', 'A'):
                            b = bare(sg)
                            if b: strict.append(b)
                elif morph[:1] in ('N', 'V', 'A'):
                    strict.append(loose)
                if loose: rows.append((ru, c, v, loose, strict))
    return rows

if __name__ == '__main__':
    rows = parse()
    print('словоформ:', len(rows))
    json.dump([[r[0], r[1], r[2], r[3], r[4]] for r in rows],
              io.open('torah_words.json', 'w', encoding='utf-8'), ensure_ascii=False)

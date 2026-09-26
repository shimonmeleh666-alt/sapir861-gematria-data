# -*- coding: utf-8 -*-
"""Покрытие: для каждого числа 1..1500 — в скольких из 54 недельных глав
есть слово с такой суммой. Считаем заново из исходника, не из нашей базы."""
import io, json
from oshb import gem

rows = json.load(io.open('torah_words.json', encoding='utf-8'))
para = json.load(io.open('para.json', encoding='utf-8'))
BOOK = ['Берешит', 'Шмот', 'Ваикра', 'Бемидбар', 'Дварим']
BI = {b: i for i, b in enumerate(BOOK)}

starts = [(BI[p['b']], p['c'], p['v']) for p in para]

def pnum(b, c, v):
    key = (BI[b], c, v)
    lo = 0
    for i, s in enumerate(starts):
        if key >= s: lo = i
        else: break
    return lo

MAX = 1500
strict = [set() for _ in range(MAX + 1)]
loose = [set() for _ in range(MAX + 1)]
for b, c, v, lw, sw in rows:
    p = pnum(b, c, v)
    g = gem(lw)
    if 1 <= g <= MAX: loose[g].add(p)
    for w in sw:
        g2 = gem(w)
        if 1 <= g2 <= MAX: strict[g2].add(p)

out = io.open('coverage_recomputed.csv', 'w', encoding='utf-8')
out.write('value,portions_strict,portions_loose\n')
for g in range(1, MAX + 1):
    out.write('%d,%d,%d\n' % (g, len(strict[g]), len(loose[g])))
out.close()

def stat(lim):
    s = sum(1 for g in range(1, lim + 1) if strict[g])
    l = sum(1 for g in range(1, lim + 1) if loose[g])
    return s, l
for lim in (861, 1000, 1500):
    print(lim, stat(lim))
print('861 strict:', len(strict[861]), 'loose:', len(loose[861]))
print('все 54 главы, strict:', [g for g in range(1, MAX + 1) if len(strict[g]) == 54])
print('все 54 главы, loose:', len([g for g in range(1, MAX + 1) if len(loose[g]) == 54]))

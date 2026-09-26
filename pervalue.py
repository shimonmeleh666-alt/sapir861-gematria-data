# -*- coding: utf-8 -*-
"""Для каждого числа 1..1500 — своё нулевое распределение.

Считаем, в скольких из 54 глав число встречается на самом деле, и в скольких
встречалось бы при случайном тексте (модель M2, марковский суррогат, и M1,
перемешивание букв). Даём среднее, отклонение, z и эмпирическую долю повторов,
в которых случай дал не меньше настоящего.

Так любое утверждение о любом числе — включая 861 — проверяется отдельно,
а не только сводная цифра.
"""
import io, json, sys
import numpy as np
from oshb import V
from nullmodel import build, markov, sums_from, VAL, MAXV, metrics

REPS = int(sys.argv[1]) if len(sys.argv) > 1 else 300
rng = np.random.default_rng(354)

def portion_counts(sums, port):
    ok = (sums >= 1) & (sums <= MAXV)
    s = sums[ok].astype(np.int64); p = port[ok].astype(np.int64)
    key = np.unique(p * (MAXV + 1) + s)
    return np.bincount(key % (MAXV + 1), minlength=MAXV + 1)[:MAXV + 1]

rows_out = []
for rule in ('strict', 'loose'):
    seq, lens, port = build(rule)
    real = portion_counts(sums_from(seq, lens), port)
    acc = np.zeros((REPS, MAXV + 1), dtype=np.int16)
    accL = np.zeros((REPS, MAXV + 1), dtype=np.int16)
    for i in range(REPS):
        acc[i] = portion_counts(markov(seq, lens, rng), port)
        accL[i] = portion_counts(sums_from(rng.permutation(seq), lens), port)
    mu, sd = acc.mean(0), acc.std(0, ddof=1)
    muL, sdL = accL.mean(0), accL.std(0, ddof=1)
    ge = (acc >= real[None, :]).mean(0)
    np.save('pv_%s.npy' % rule, np.vstack([real, mu, sd, muL, sdL, ge]))
    print(rule, 'готово; 861:', real[861], mu[861], sd[861], ge[861])

out = io.open('coverage_vs_null_1500.csv', 'w', encoding='utf-8')
out.write('value,portions_strict,null_markov_mean_strict,null_markov_sd_strict,'
          'null_shuffle_mean_strict,z_strict,p_null_ge_real_strict,'
          'portions_loose,null_markov_mean_loose,null_markov_sd_loose,'
          'null_shuffle_mean_loose,z_loose,p_null_ge_real_loose\n')
S = np.load('pv_strict.npy'); L = np.load('pv_loose.npy')
for g in range(1, MAXV + 1):
    def blk(A):
        r, mu, sd, muL, sdL, ge = A[:, g]
        z = (r - mu) / sd if sd > 0 else float('nan')
        return '%d,%.3f,%.3f,%.3f,%.2f,%.4f' % (r, mu, sd, muL, z, ge)
    out.write('%d,%s,%s\n' % (g, blk(S), blk(L)))
out.close()
print('coverage_vs_null_1500.csv записан, повторов:', REPS)

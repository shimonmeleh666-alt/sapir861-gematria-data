# -*- coding: utf-8 -*-
"""Нулевые модели для покрытия сумм в Пятикнижии.

Вопрос, который закрывает эта работа: сколько чисел имело бы слово,
если бы текст был случайным? Без этого числа покрытие 867 из 1000
ничего не доказывает.

Три модели, от грубой к точной:

M1  «мешок букв». Все согласные Пятикнижия перемешиваются по всему корпусу.
    Сохраняются: частоты букв, длины слов, их порядок и деление на 54 главы.
    Разрушается: всё словесное.

M2  «марковский суррогат». Каждое слово порождается буква за буквой цепью
    Маркова первого порядка, обученной на самом Пятикнижии, при той же длине
    слова и на том же месте. Сохраняется локальная связь букв (именно она
    определяет распределение сумм), разрушается словарь.

M3  «перемешивание глав». Настоящие слова остаются, но раскидываются по главам
    случайно при тех же размерах глав. Проверяет не богатство словаря, а то,
    особое ли распределение сумм по главам.

Мера: сколько чисел 1..1000 и 1..1500 имеют хотя бы одно слово; сколько чисел
покрыты во всех 54 главах; пусто ли 861.
Правило strict — только имена, глаголы, прилагательные без приставок;
loose — вся словоформа.
"""
import io, json, sys
import numpy as np
from oshb import V

REPS_M1 = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
REPS_M2 = int(sys.argv[2]) if len(sys.argv) > 2 else 300
SEED = 861

rows = json.load(io.open('torah_words.json', encoding='utf-8'))
para = json.load(io.open('para.json', encoding='utf-8'))
BOOK = ['Берешит', 'Шмот', 'Ваикра', 'Бемидбар', 'Дварим']
BI = {b: i for i, b in enumerate(BOOK)}
starts = [(BI[p['b']], p['c'], p['v']) for p in para]

def pnum(b, c, v):
    key = (BI[b], c, v); lo = 0
    for i, s in enumerate(starts):
        if key >= s: lo = i
        else: break
    return lo

LET = sorted(V, key=lambda c: V[c])
LI = {c: i for i, c in enumerate(LET)}
VAL = np.array([V[c] for c in LET], dtype=np.int64)
NL = len(LET)

def build(rule):
    seq, lens, port = [], [], []
    for b, c, v, lw, sw in rows:
        p = pnum(b, c, v)
        forms = [lw] if rule == 'loose' else sw
        for w in forms:
            if not w: continue
            seq.extend(LI[ch] for ch in w)
            lens.append(len(w)); port.append(p)
    return (np.array(seq, dtype=np.int8), np.array(lens, dtype=np.int64),
            np.array(port, dtype=np.int64))

MAXV = 1500

def metrics(sums, port):
    ok = (sums >= 1) & (sums <= MAXV)
    s = sums[ok]; p = port[ok]
    cov = np.zeros(MAXV + 1, dtype=bool)
    cov[np.unique(s)] = True
    key = np.unique(p.astype(np.int64) * (MAXV + 1) + s)
    cnt = np.bincount(key % (MAXV + 1), minlength=MAXV + 1)
    return (int(cov[1:1001].sum()), int(cov[1:1501].sum()),
            int((cnt[1:1501] == 54).sum()), bool(cov[861]))

def sums_from(seq, lens):
    off = np.zeros(len(lens), dtype=np.int64)
    np.cumsum(lens[:-1], out=off[1:])
    return np.add.reduceat(VAL[seq], off)

def markov(seq, lens, rng):
    """цепь Маркова 1-го порядка по буквам внутри слова"""
    off = np.zeros(len(lens), dtype=np.int64); np.cumsum(lens[:-1], out=off[1:])
    T = np.zeros((NL + 1, NL), dtype=np.float64)      # состояние 0..NL-1 + старт NL
    for o, L in zip(off, lens):
        w = seq[o:o + L]
        T[NL, w[0]] += 1
        for i in range(L - 1): T[w[i], w[i + 1]] += 1
    T += 1e-9
    T /= T.sum(1, keepdims=True)
    C = np.cumsum(T, axis=1)
    maxL = int(lens.max()); n = len(lens)
    out = np.zeros((n, maxL), dtype=np.int64)
    state = np.full(n, NL, dtype=np.int64)
    alive = np.ones(n, dtype=bool)
    for k in range(maxL):
        r = rng.random(n)
        nxt = (C[state] < r[:, None]).sum(1)
        np.clip(nxt, 0, NL - 1, out=nxt)
        out[:, k] = np.where(alive, nxt, -1)
        state = nxt
        alive &= (lens > k + 1)
    m = out >= 0
    return (VAL[np.where(m, out, 0)] * m).sum(1)

def run(rule):
    seq, lens, port = build(rule)
    real = metrics(sums_from(seq, lens), port)
    rng = np.random.default_rng(SEED)
    res = {'rule': rule, 'words': int(len(lens)), 'letters': int(len(seq)), 'real': real}

    for name, reps in (('M1', REPS_M1), ('M2', REPS_M2), ('M3', REPS_M1)):
        acc = []
        for _ in range(reps):
            if name == 'M1':
                s = sums_from(rng.permutation(seq), lens); pp = port
            elif name == 'M2':
                s = markov(seq, lens, rng); pp = port
            else:
                s = sums_from(seq, lens); pp = rng.permutation(port)
            acc.append(metrics(s, pp))
        a = np.array([[x[0], x[1], x[2], int(x[3])] for x in acc], dtype=float)
        res[name] = {'reps': reps,
                     'mean': a.mean(0).tolist(), 'sd': a.std(0, ddof=1).tolist(),
                     'min': a.min(0).tolist(), 'max': a.max(0).tolist(),
                     'ge_real': [(a[:, i] >= real[i]).sum() / reps for i in range(3)],
                     'p861_empty': float((a[:, 3] == 0).sum()) / reps}
    return res

def main():
  out = {}
  for rule in ('strict', 'loose'):
      out[rule] = run(rule)
      print(json.dumps(out[rule], ensure_ascii=False, indent=1))
  json.dump(out, io.open('nullmodel_results.json', 'w', encoding='utf-8'),
            ensure_ascii=False, indent=1)

if __name__ == '__main__':
    main()

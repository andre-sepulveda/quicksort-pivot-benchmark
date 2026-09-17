"""
Benchmark: quicksort com pivo fixo vs. pivo aleatorio.

Cenarios:
  - entrada aleatoria (mesma para os dois algoritmos, gerada com seed fixa)
  - entrada ja ordenada (pior caso do pivo fixo)

Metodologia:
  - 5 tamanhos, dobrando a cada passo: 1000, 2000, 4000, 8000, 16000
  - por ponto: 1 execucao de aquecimento (descartada) + 3 execucoes medidas
  - reporta a mediana das 3 execucoes medidas
  - seed fixa (42) no gerador da entrada aleatoria

Uso:
    python3 bench.py
Gera:
    ../dados/resultados.csv
"""

import csv
import os
import random
import signal
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))

from quicksort_fixo import quicksort_fixo
from quicksort_aleatorio import quicksort_aleatorio

SEED = 42
# Tamanhos deslocados para cima (em vez de comecar em 1.000) para que ate o
# ponto mais rapido (pivo aleatorio, n=2.000) fique bem acima do ruido de
# medicao (agendamento do SO, variacao do clock, etc). O que importa na
# analise nao e o tempo absoluto, e a razao entre tempos consecutivos.
TAMANHOS = [2000, 4000, 8000, 16000, 32000]
AQUECIMENTO = 1
EXECUCOES = 3
TIMEOUT_SEGUNDOS = 120

sys.setrecursionlimit(100000)


class TempoExcedido(Exception):
    pass


def _handler(signum, frame):
    raise TempoExcedido()


signal.signal(signal.SIGALRM, _handler)


def gerar_entrada_aleatoria(n, seed=SEED):
    rnd = random.Random(seed)
    arr = list(range(n))
    rnd.shuffle(arr)
    return arr


def gerar_entrada_ordenada(n):
    return list(range(n))


def mediana(valores):
    s = sorted(valores)
    m = len(s)
    if m % 2 == 1:
        return s[m // 2]
    return (s[m // 2 - 1] + s[m // 2]) / 2


def medir_uma_execucao(func, arr, timeout=TIMEOUT_SEGUNDOS):
    signal.alarm(timeout)
    try:
        t0 = time.perf_counter()
        func(arr)
        t1 = time.perf_counter()
        return t1 - t0
    except TempoExcedido:
        return None
    finally:
        signal.alarm(0)


def medir_ponto(func, gerar_entrada, n):
    tempos = []
    for k in range(AQUECIMENTO + EXECUCOES):
        arr = gerar_entrada(n)
        t = medir_uma_execucao(func, arr)
        if t is None:
            return None  # excedeu o tempo limite -> ponto descartado
        if k >= AQUECIMENTO:
            tempos.append(t)
    return mediana(tempos)


def main():
    random.seed(SEED)

    combinacoes = [
        ("pivo_fixo", "aleatoria", quicksort_fixo, gerar_entrada_aleatoria),
        ("pivo_aleatorio", "aleatoria", quicksort_aleatorio, gerar_entrada_aleatoria),
        ("pivo_fixo", "ordenada", quicksort_fixo, gerar_entrada_ordenada),
        ("pivo_aleatorio", "ordenada", quicksort_aleatorio, gerar_entrada_ordenada),
    ]

    linhas = []
    for algoritmo, cenario, func, gerador in combinacoes:
        print(f"Medindo {algoritmo} / entrada {cenario}...")
        parar = False
        for n in TAMANHOS:
            if parar:
                linhas.append([algoritmo, cenario, n, ""])
                continue
            t = medir_ponto(func, gerador, n)
            if t is None:
                print(f"  n={n}: excedeu {TIMEOUT_SEGUNDOS}s, descartando pontos maiores")
                linhas.append([algoritmo, cenario, n, ""])
                parar = True
            else:
                print(f"  n={n}: {t:.6f}s")
                linhas.append([algoritmo, cenario, n, f"{t:.6f}"])

    saida = os.path.join(os.path.dirname(__file__), "..", "dados", "resultados.csv")
    with open(saida, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["algoritmo", "cenario", "n", "tempo_segundos"])
        w.writerows(linhas)

    print(f"\nResultados salvos em {os.path.abspath(saida)}")


if __name__ == "__main__":
    main()

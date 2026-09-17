"""
Le ../dados/resultados.csv e imprime, para cada combinacao
algoritmo/cenario, a razao entre o tempo em n e o tempo em n/2.

Uso:
    python3 analise_razoes.py
"""

import csv
import os

BASE = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE, "..", "dados", "resultados.csv")


def main():
    dados = {}
    with open(CSV_PATH) as f:
        for row in csv.DictReader(f):
            chave = (row["algoritmo"], row["cenario"])
            n = int(row["n"])
            t = float(row["tempo_segundos"]) if row["tempo_segundos"] else None
            dados.setdefault(chave, {})[n] = t

    for chave, pontos in dados.items():
        print(f"\n{chave[0]} / entrada {chave[1]}")
        tamanhos = sorted(pontos)
        anterior = None
        for n in tamanhos:
            t = pontos[n]
            if t is None:
                print(f"  n={n:>6}: (nao medido - excedeu o tempo limite)")
                continue
            if anterior is None:
                print(f"  n={n:>6}: {t:.6f}s")
            else:
                razao = t / anterior
                print(f"  n={n:>6}: {t:.6f}s   razao vs n/2 = {razao:.2f}x")
            anterior = t


if __name__ == "__main__":
    main()

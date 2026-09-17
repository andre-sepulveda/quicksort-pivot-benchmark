"""
Le ../dados/resultados.csv e gera ../graficos/comparacao.png
com os 4 tempos (2 algoritmos x 2 cenarios) em escala log no eixo Y.

Uso:
    python3 gerar_grafico.py
"""

import csv
import os

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

BASE = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE, "..", "dados", "resultados.csv")
PNG_PATH = os.path.join(BASE, "..", "graficos", "comparacao.png")

ROTULOS = {
    ("pivo_fixo", "aleatoria"): "Pivô fixo — entrada aleatória",
    ("pivo_aleatorio", "aleatoria"): "Pivô aleatório — entrada aleatória",
    ("pivo_fixo", "ordenada"): "Pivô fixo — entrada ordenada (pior caso)",
    ("pivo_aleatorio", "ordenada"): "Pivô aleatório — entrada ordenada",
}

ESTILOS = {
    ("pivo_fixo", "aleatoria"): dict(color="#1f77b4", linestyle="-", marker="o"),
    ("pivo_aleatorio", "aleatoria"): dict(color="#ff7f0e", linestyle="-", marker="s"),
    ("pivo_fixo", "ordenada"): dict(color="#d62728", linestyle="--", marker="^"),
    ("pivo_aleatorio", "ordenada"): dict(color="#2ca02c", linestyle="--", marker="v"),
}


def carregar_dados():
    series = {}
    with open(CSV_PATH) as f:
        r = csv.DictReader(f)
        for row in r:
            chave = (row["algoritmo"], row["cenario"])
            n = int(row["n"])
            t = float(row["tempo_segundos"]) if row["tempo_segundos"] else None
            series.setdefault(chave, {})[n] = t
    return series


def main():
    series = carregar_dados()
    tamanhos = sorted({n for pontos in series.values() for n in pontos})

    plt.figure(figsize=(8, 5.5))
    for chave, pontos in series.items():
        xs = [n for n in tamanhos if pontos.get(n) is not None]
        ys = [pontos[n] for n in xs]
        plt.plot(xs, ys, label=ROTULOS[chave], **ESTILOS[chave])

    plt.xscale("log", base=2)
    plt.yscale("log")
    plt.xticks(tamanhos, [str(n) for n in tamanhos])

    # mostra os valores do eixo Y em segundos "normais" (0.001, 0.01, 1, 10...)
    # em vez da notacao cientifica padrao do matplotlib (10^-3, 10^0...)
    def formatar_segundos(valor, _pos):
        return f"{valor:g}s"

    eixo = plt.gca()
    eixo.yaxis.set_major_formatter(mticker.FuncFormatter(formatar_segundos))
    eixo.yaxis.set_minor_formatter(mticker.NullFormatter())

    plt.xlabel("Tamanho da entrada (n)")
    plt.ylabel("Tempo (s) — escala log")
    plt.title("Quicksort: pivô fixo vs. pivô aleatório")
    plt.legend()
    plt.grid(True, which="both", linestyle=":", linewidth=0.5)
    plt.tight_layout()

    os.makedirs(os.path.dirname(PNG_PATH), exist_ok=True)
    plt.savefig(PNG_PATH, dpi=150)
    print(f"Grafico salvo em {os.path.abspath(PNG_PATH)}")


if __name__ == "__main__":
    main()

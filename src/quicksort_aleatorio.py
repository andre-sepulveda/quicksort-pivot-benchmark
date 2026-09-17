"""
Quicksort com pivo aleatorio (sorteado a cada particao).

Mesma estrutura iterativa do quicksort_fixo.py; a unica diferenca real
e a linha que sorteia o pivo e o troca para a primeira posicao antes
de particionar.
"""

import random


def quicksort_aleatorio(arr):
    a = arr[:]
    pilha = [(0, len(a) - 1)]
    while pilha:
        lo, hi = pilha.pop()
        while lo < hi:
            r = random.randint(lo, hi)
            a[lo], a[r] = a[r], a[lo]
            pivot = a[lo]

            i, j = lo + 1, hi
            while True:
                while i <= j and a[i] <= pivot:
                    i += 1
                while i <= j and a[j] > pivot:
                    j -= 1
                if i > j:
                    break
                a[i], a[j] = a[j], a[i]
            a[lo], a[j] = a[j], a[lo]

            esquerda = (lo, j - 1)
            direita = (j + 1, hi)
            if (esquerda[1] - esquerda[0]) < (direita[1] - direita[0]):
                if direita[0] < direita[1]:
                    pilha.append(direita)
                lo, hi = esquerda
            else:
                if esquerda[0] < esquerda[1]:
                    pilha.append(esquerda)
                lo, hi = direita
    return a

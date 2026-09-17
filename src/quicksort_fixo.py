"""
Quicksort com pivo fixo (sempre o primeiro elemento da particao).

Implementacao iterativa (pilha explicita) para nao esbarrar no limite
de recursao do Python quando o pior caso (entrada ja ordenada) gera
profundidade O(n).
"""


def quicksort_fixo(arr):
    a = arr[:]
    pilha = [(0, len(a) - 1)]
    while pilha:
        lo, hi = pilha.pop()
        while lo < hi:
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

            # empilha o lado maior, continua no menor (limita a pilha,
            # nao muda a complexidade do pior caso do pivo fixo)
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

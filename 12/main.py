#!/usr/bin/python
# -*- coding: utf-8 -*-
# Maciej Wieloch, 303080

import time


def naive_method(text, pattern):
    start_time = time.time()
    comparation_counter = 0

    result = []
    for m in range(len(text)):
        comparation_counter = comparation_counter + 1
        if text[m] == pattern[0]:
            match = True

            result_index = m
            for i in range(1, len(pattern)):
                comparation_counter = comparation_counter + 1
                if text[m + i] == pattern[i]:
                    continue
                else:
                    match = False
                    break

            if match:
                result.append(result_index)

    print("--- method: naive ---")
    print("--- pattern: %s ---" % pattern)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("--- %s comparations ---" % comparation_counter)
    print("--- %s repetitions ---\n" % len(result))

    return result


def rolling_hash(pattern, text, is_pattern=True, hS=None, m=None):
    pattern = pattern.lower()

    d = 256
    # q = 7919
    q = 101

    N = len(pattern)

    if is_pattern:
        hW = 0
        for i in range(N):
            hW = (d * hW + ord(pattern[i])) % q

        return hW

    else:
        h = 1
        for i in range(N - 1):
            h = (h * d) % q

        hS = (d * (hS - ord(text[m]) * h) + ord(text[m + N])) % q

        if hS < 0:
            hS = hS + q

        return hS


def RabinKarp(text, pattern):
    start_time = time.time()
    comparation_counter = 0
    wrong_hash_counter = 0

    M = len(text)
    N = len(pattern)

    hW = rolling_hash(pattern, text)
    hS = 0

    result = []
    for m in range(M - N + 1):
        if m == 0:
            hS = rolling_hash(text[0:N], text)
        else:
            hS = rolling_hash(pattern, text, False, hS, m - 1)

        if hS == hW:
            comparation_counter = comparation_counter + 1
            if text[m: m + N] == pattern:
                result.append(m)
            else:
                wrong_hash_counter = wrong_hash_counter + 1

    print("--- method: Robin-Karp ---")
    print("--- pattern: %s ---" % pattern)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("--- %s comparations ---" % comparation_counter)
    print("--- %s wrong hashes ---" % wrong_hash_counter)
    print("--- %s repetitions ---\n" % len(result))

    return result


def kmp_search(text, pattern):
    start_time = time.time()
    comparation_counter = 0

    P = []
    T = kmp_table(pattern)

    m, i = 0, 0
    while m < len(text):
        comparation_counter = comparation_counter + 1

        if pattern[i] == text[m]:
            m = m + 1
            i = i + 1

            if i == len(pattern):
                P.append(m - i)
                i = T[i]
        else:
            i = T[i]
            if i < 0:
                m = m + 1
                i = i + 1

    print("--- method: Knuth-Morris-Pratt ---")
    print("--- pattern: %s ---" % pattern)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("--- %s comparations ---" % comparation_counter)
    print("--- %s repetitions ---\n" % len(P))

    return P


def kmp_table(W):
    T = [0 for _ in range(len(W) + 1)]

    pos = 1
    cnd = 0

    T[0] = -1
    while pos < len(W):
        if W[pos] == W[cnd]:
            T[pos] = T[cnd]

        else:
            T[pos] = cnd

            while cnd >= 0 and W[pos] != W[cnd]:
                cnd = T[cnd]

        pos = pos + 1
        cnd = cnd + 1

    T[pos] = cnd

    return T


if __name__ == "__main__":
    with open('lotr.txt', encoding='utf-8') as f:
        sample = f.readlines()

    S = ' '.join(sample).lower()
    W = 'bilbo'

    naive_method(S, W)
    RabinKarp(S, W)

    # Dla algorytmu Robina-Karpa:
    # Funkcja czasowo wykonuje się dłużej dla danego tekstu (prawie 9 razy) w przypadku
    # mojego kodu, przy mniejszej liczbie porównań tekstu wybranego do wzorca.
    # Spowodowane jest to haszowaniem, które ma większą złożoność czasową niż porównywanie
    # dla tego tekstu i krótkich wyrazów. Im większa jest liczba pierwsza q, tym mniej haszy
    # jest niezgodnych ze wzorcem i tym dłużej operacja haszowania trwa. Dla q=101 - 862 haszy
    # było błędnych, a dla q = 7919 tylko 4 hasze okazały się błędne dla wzorca 'bilbo'.

    kmp_search(S, W)

    W = 'may '
    naive_method(S, W)
    RabinKarp(S, W)
    kmp_search(S, W)

    W = 'the '
    naive_method(S, W)
    RabinKarp(S, W)
    kmp_search(S, W)

    W = 'wizard'
    naive_method(S, W)
    RabinKarp(S, W)
    kmp_search(S, W)

    W = 'gandalf'
    naive_method(S, W)
    RabinKarp(S, W)
    kmp_search(S, W)


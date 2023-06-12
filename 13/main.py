#!/usr/bin/python
# -*- coding: utf-8 -*-
# Maciej Wieloch, 303080

from timeit import default_timer


def fib_r(n):
    if n == 0:
        return 0
    if n == 1:
        return 1

    return fib_r(n - 1) + fib_r(n - 2)


# Parametry do funkcji fib_c oraz fib_pd
MAXN = 45
UNKNOWN = -1


def fib_c(n):
    global MAXN
    global UNKNOWN
    global fib_c_res

    if fib_c_res[n] == UNKNOWN:
        fib_c_res[n] = fib_c(n - 1) + fib_c(n - 2)

    return fib_c_res[n]


def fib_c_driver(n):
    fib_c_res[0] = 0
    fib_c_res[1] = 1

    for i in range(2, n):
        fib_c_res[i] = UNKNOWN

    return fib_c(n)


def fib_pd(n):
    result = [0 for _ in range(MAXN + 1)]
    result[0] = 0
    result[1] = 1

    for i in range(2, n + 1):
        result[i] = result[i - 1] + result[i - 2]

    return result[n]


def fib_pd_v2(n):
    a = 0
    b = 1

    for i in range(2, n + 1):
        c = a + b
        a = b
        b = c

    return b


# Parametry do funkcji string_compare
MATCH = 0
INSERT = 1
DELETE = 2


def match(c, d):
    if c == d:
        return 0
    else:
        return 1


def indel(c):
    return 1


def string_compare(s, t, i, j):
    global MATCH
    global INSERT
    global DELETE

    opt = [0 for _ in range(3)]

    if i == 0:
        return j * indel(' ')

    if j == 0:
        return i * indel(' ')

    opt[MATCH] = string_compare(s, t, i - 1, j - 1) + match(s[i], t[j])
    opt[INSERT] = string_compare(s, t, i, j - 1) + indel(t[j])
    opt[DELETE] = string_compare(s, t, i - 1, j) + indel(s[i])

    lowest_cost = opt[MATCH]

    for k in range(INSERT, DELETE + 1):
        if opt[k] < lowest_cost:
            lowest_cost = opt[k]

    return lowest_cost


# Parametry do funkcji string_compare_v2
MAXLEN = 20


class Cell:
    def __init__(self):
        self.cost = 0
        self.parent = 1


# Pregeneracja macierzy m do funkcji string_compare_v2
m = [[Cell() for x in range(MAXLEN + 1)] for y in range(MAXLEN + 1)]


def row_init(i):
    global m
    m[0][i].cost = i
    if i > 0:
        m[0][i].parent = INSERT
    else:
        m[0][i].parent = -1


def column_init(i):
    global m
    m[i][0].cost = i
    if i > 0:
        m[i][0].parent = DELETE
    else:
        m[i][0].parent = -1


def goal_cell(s, t):
    return len(s) - 1, len(t) - 1


def string_compare_v2(s, t):
    global MATCH
    global INSERT
    global DELETE
    global MAXLEN
    global m

    opt = [0 for _ in range(3)]

    for i in range(0, MAXLEN):
        row_init(i)
        column_init(i)

    for i in range(1, len(s)):
        for j in range(1, len(t)):
            opt[MATCH] = m[i - 1][j - 1].cost + match(s[i], t[j])
            opt[INSERT] = m[i][j - 1].cost + indel(t[j])
            opt[DELETE] = m[i - 1][j].cost + indel(s[i])

            m[i][j].cost = opt[MATCH]
            m[i][j].parent = MATCH

            for k in range(INSERT, DELETE + 1):
                if opt[k] < m[i][j].cost:
                    m[i][j].cost = opt[k]
                    m[i][j].parent = k

    i, j = goal_cell(s, t)
    lowest_cost = m[i][j].cost

    return lowest_cost


def match_out(s, t, i, j):
    if s[i] == t[j]:
        print('M', end='')
    else:
        print('S', end='')


def insert_out(t, j):
    print("I", end='')


def delete_out(s, i):
    print("D", end='')


def reconstruct_path(s, t, i, j):
    global m

    if m[i][j].parent == -1:
        return ''

    if m[i][j].parent == MATCH:
        reconstruct_path(s, t, i - 1, j - 1)
        match_out(s, t, i, j)
        return ''

    if m[i][j].parent == INSERT:
        reconstruct_path(s, t, i, j - 1)
        insert_out(t, j)
        return ''

    if m[i][j].parent == DELETE:
        reconstruct_path(s, t, i - 1, j)
        delete_out(s, i)
        return ''


def row_init_v2(i):
    global m
    m[0][i].cost = 0
    m[0][i].parent = -1


def goal_cell_v2(s, t):
    global m
    i = len(s) - 1
    j = 0
    for k in range(1, len(t)):
        if m[i][k].cost < m[i][j].cost:
            j = k

    return i, j


def string_compare_v3(s, t):
    global MATCH
    global INSERT
    global DELETE
    global MAXLEN
    global m

    opt = [0 for _ in range(3)]

    for i in range(0, MAXLEN):
        row_init_v2(i)
        column_init(i)

    for i in range(1, len(s)):
        for j in range(1, len(t)):
            opt[MATCH] = m[i - 1][j - 1].cost + match(s[i], t[j])
            opt[INSERT] = m[i][j - 1].cost + indel(t[j])
            opt[DELETE] = m[i - 1][j].cost + indel(s[i])

            m[i][j].cost = opt[MATCH]
            m[i][j].parent = MATCH

            for k in range(INSERT, DELETE + 1):
                if opt[k] < m[i][j].cost:
                    m[i][j].cost = opt[k]
                    m[i][j].parent = k

    i, j = goal_cell_v2(s, t)

    return j, t[j]


def match_v3(c, d):
    if c == d:
        return 0
    else:
        return MAXLEN


def string_compare_v3_pd(s, t):
    global MATCH
    global INSERT
    global DELETE
    global MAXLEN
    global m

    opt = [0 for _ in range(3)]
    result = ''

    for i in range(0, MAXLEN):
        row_init(i)
        column_init(i)

    for i in range(1, len(s)):
        for j in range(1, len(t)):
            opt[MATCH] = m[i - 1][j - 1].cost + match(s[i], t[j])

            if match_v3(s[i], t[j]) == 0 and j >= i:
                result = result + str(t[j])

            opt[INSERT] = m[i][j - 1].cost + indel(t[j])
            opt[DELETE] = m[i - 1][j].cost + indel(s[i])

            m[i][j].cost = opt[MATCH]
            m[i][j].parent = MATCH

            for k in range(INSERT, DELETE + 1):
                if opt[k] < m[i][j].cost:
                    m[i][j].cost = opt[k]
                    m[i][j].parent = k

    return result


if __name__ == "__main__":
    # =============== REKURENCJA ====================
    # start_time = default_timer()
    # print(f'Wynik funkcji fib_r: {fib_r(40)}')
    # print(f'Czas wykonania: {default_timer() - start_time}')

    # =============== PAMIĘCIOWA ====================
    start_time = default_timer()
    fib_c_res = [-1 for _ in range(MAXN + 1)]
    print(f'\nWynik funkcji fib_c: {fib_c_driver(40)}')
    print(f'Czas wykonania: {default_timer() - start_time}')

    # ===================== PD ==========================
    start_time = default_timer()
    print(f'\nWynik funkcji fib_pd: {fib_pd(40)}')
    print(f'Czas wykonania: {default_timer() - start_time}')

    # =================== PD 2.0 =========================
    start_time = default_timer()
    print(f'\nWynik funkcji fib_pd_v2: {fib_pd_v2(40)}')
    print(f'Czas wykonania: {default_timer() - start_time}')

    # =============== string_compare =====================
    print('\n=====================================================================')
    print('Aproksymowane dopasowanie ciągu znakowego\n')

    S = 'kot'
    T = 'kon'
    start_time = default_timer()
    print(f'a) Dla s = {S}, t = {T}, wynik funkcji string_compare: {string_compare(S, T, len(S) - 1, len(T) - 1)}')
    print(f'Czas wykonania: {default_timer() - start_time}')

    # =============== string_compare_v2 =====================
    S = 'kot'
    T = 'kon'
    start_time = default_timer()

    m = [[Cell() for x in range(MAXLEN + 1)] for y in range(MAXLEN + 1)]

    print(f'\nb) Dla s = {S}, t = {T}, wynik funkcji string_compare_v2: {string_compare_v2(S, T)}')
    print(f'Czas wykonania: {default_timer() - start_time}')

    # =============== reconstruct_path =====================
    S = ' thou shalt not'
    T = ' you should not'
    start_time = default_timer()

    m = [[Cell() for x in range(MAXLEN + 1)] for y in range(MAXLEN + 1)]
    string_compare_v2(S, T)
    i, j = goal_cell(S, T)

    print(f'\nc) Dla s = {S}, t = {T}, wynik funkcji reconstruct_path: ', end='')
    reconstruct_path(S, T, i, j)
    print(f'\nCzas wykonania: {default_timer() - start_time}')

    # =============== string_compare_v3 =====================
    S = ' ban'
    T = ' mokeyssbanana'
    start_time = default_timer()

    m = [[Cell() for x in range(MAXLEN + 1)] for y in range(MAXLEN + 1)]

    print(f'\nd) Dla s = {S}, t = {T}, wynik funkcji string_compare_v3: {string_compare_v3(S, T)}')
    print(f'Czas wykonania: {default_timer() - start_time}')

    # =============== string_compare_v3_pd =====================
    S = ' democrat'
    T = ' republican'
    start_time = default_timer()

    m = [[Cell() for x in range(MAXLEN + 1)] for y in range(MAXLEN + 1)]

    print(f'\ne) Dla s = {S}, t = {T}, wynik funkcji string_compare_v3_pd: {string_compare_v3_pd(S, T)}')
    print(f'Czas wykonania: {default_timer() - start_time}')

    T = ' 243517698'
    S = sorted(T)

    start_time = default_timer()

    m = [[Cell() for x in range(MAXLEN + 1)] for y in range(MAXLEN + 1)]

    print(f'\nf) Dla s =  123456789, t = {T}, wynik funkcji string_compare_v3_pd: {string_compare_v3_pd(S, T)}')
    print(f'Czas wykonania: {default_timer() - start_time}')

    S = ' programowanie'
    T = ' chillowanie'

    start_time = default_timer()

    m = [[Cell() for x in range(MAXLEN + 1)] for y in range(MAXLEN + 1)]

    print(f'\nf) Dla s = {S}, t = {T}, wynik funkcji string_compare_v3_pd: {string_compare_v3_pd(S, T)}')
    print(f'Czas wykonania: {default_timer() - start_time}')

    print("HW")

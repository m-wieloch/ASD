#!/usr/bin/python
# -*- coding: utf-8 -*-
# Maciej Wieloch, 303080

from typing import List, Tuple


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'


def jarvis(points: List[Point]):
    n = len(points)

    if n < 3:
        raise ValueError(f'There must be at least 3 points to mark surround, current = {n}')

    else:
        left_extremity = 0
        for i in range(1, n):
            if points[left_extremity].x > points[i].x:
                left_extremity = i
            if points[left_extremity].x == points[i].x:
                if points[left_extremity].y > points[i].y:
                    left_extremity = i

    p = left_extremity

    result = [p]
    while points:
        q = (p + 1) % n

        for r in range(n):
            sig_c = points[r].y - points[p].y
            sig_d = points[r].x - points[p].x

            tau_c = points[q].y - points[r].y
            tau_d = points[q].x - points[r].x

            direction = (sig_c * tau_d) - (tau_c * sig_d)

            if direction < 0:
                q = r

        p = q
        result.append(p)
        if p == left_extremity:
            break

    result_p = []
    for i in result:
        result_p.append((points[i].x, points[i].y))

    return result_p


def jarvis_v2(points: List[Point]):
    n = len(points)

    if n < 3:
        raise ValueError(f'There must be at least 3 points to mark surround, current = {n}')

    else:
        left_extremity = 0
        for i in range(1, n):
            if points[left_extremity].x > points[i].x:
                left_extremity = i
            if points[left_extremity].x == points[i].x:
                if points[left_extremity].y > points[i].y:
                    left_extremity = i

    p = left_extremity

    result = [p]
    while points:
        q = (p + 1) % n

        for r in range(n):
            sig_c = points[r].y - points[p].y
            sig_d = points[r].x - points[p].x

            tau_c = points[q].y - points[r].y
            tau_d = points[q].x - points[r].x

            direction = (sig_c * tau_d) - (tau_c * sig_d)

            if direction < 0:
                q = r

            if direction == 0:
                if points[p].x > points[q].x > points[r].x or points[p].x < points[q].x < points[r].x or points[p].y > points[q].y > points[r].y or points[p].y < points[q].y < points[r].y:
                    q = r
        p = q
        result.append(p)
        if p == left_extremity:
            break

    result_p = []
    for i in result:
        result_p.append((points[i].x, points[i].y))

    return result_p


def dir(p, r, q):
    sig_c = r.y - p.y
    sig_d = r.x - p.x
    tau_c = q.y - r.y
    tau_d = q.x - r.x

    direction = (sig_c * tau_d) - (tau_c * sig_d)

    return direction


def _sorting(points):
    n = len(points)

    down_extremity = 0
    for i in range(1, n):
        if points[down_extremity].y > points[i].y:
            down_extremity = i
        if points[down_extremity].x == points[i].x:
            if points[down_extremity].x > points[i].x:
                down_extremity = i

    p0 = points.pop(down_extremity)

    points.insert(0, p0)

    i = 1
    while i < n - 1:
        s = i
        direction = dir(points[0], points[i], points[i + 1])

        if direction < 0:
            i = i + 1
        else:
            points[i], points[i + 1] = points[i + 1], points[i]

            if direction > 0:
                s = s - 1

                while s > 0:
                    direction = dir(points[0], points[s], points[s + 1])

                    if direction > 0:
                        points[s], points[s + 1] = points[s + 1], points[s]
                        s = s - 1
                    else:
                        if direction == 0:
                            if points[s].x > points[s + 1].x:
                                points[s], points[s + 1] = points[s + 1], points[s]
                        break
            i = i + 1

    return points


def graham(points: List[Point]):
    n = len(points)

    points = _sorting(points)

    i = 1
    while i < len(points) - 1:
        direction = dir(points[0], points[i], points[i + 1])

        if direction == 0:
            points.pop(i)
        else:
            i = i + 1

    if n < 3:
        raise ValueError(f'There must be at least 3 points to mark surround, current = {n}')

    else:
        S = points[0:3]
        Q = points[3:]

        for i in range(len(Q)):
            S.append(Q.pop(0))

            direction = dir(S[-3], S[-2], S[-1])
            if direction >= 0:
                S.pop(-2)

    result_p = []
    for i in range(len(S)):
        result_p.append((S[i].x, S[i].y))

    return result_p


if __name__ == "__main__":
    # =============== jarvis ====================
    set1 = [Point(0, 3), Point(0, 0), Point(0, 1), Point(3, 0), Point(3, 3)]
    set2 = [Point(0, 3), Point(0, 1), Point(0, 0), Point(3, 0), Point(3, 3)]

    print('Dla:', end=' ')
    for el in set1:
        print(el, end=' ')
    print(f'\nWynik funkcji jarvis: {jarvis(set1)}')

    print('\nDla:', end=' ')
    for el in set1:
        print(el, end=' ')
    print(f'\nWynik funkcji jarvis: {jarvis(set2)}')

    # =============== jarvis_v2 ====================
    print('\nDla:', end=' ')
    for el in set1:
        print(el, end=' ')
    print(f'\nWynik funkcji jarvis_v2: {jarvis_v2(set1)}')

    print('\nDla:', end=' ')
    for el in set1:
        print(el, end=' ')
    print(f'\nWynik funkcji jarvis_v2: {jarvis_v2(set2)}')

    # =============== graham ====================
    set3 = [Point(0, 3), Point(1, 1), Point(2, 2), Point(4, 4), Point(0, 0), Point(1, 2), Point(3, 1), Point(3, 3)]

    print('\nDla:', end=' ')
    for el in set3:
        print(el, end=' ')
    print(f'\nWynik funkcji graham: {graham(set3)}')

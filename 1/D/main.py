#!/usr/bin/python
# -*- coding: utf-8 -*-
# Maciej Wieloch, 303080

from typing import Tuple, Union


class Matrix:
    def __init__(self, matrix, ing=0):
        if isinstance(matrix, Tuple):
            self.rows = matrix[0]
            self.cols = matrix[1]
            self.M = [[ing] * self.cols for _ in range(self.rows)]
        else:
            self.rows = len(matrix)
            self.cols = len(matrix[0])
            self.M = matrix

    def __str__(self):
        output = ''
        for i in range(len(self.M)):
            output += '{}'.format(self.M[i]) + '\n'

        return output


# Funkcja liczaca wyznacznik macierzy 2x2
def det(m: Matrix) -> Union[int, float]:
    if isinstance(m, Matrix) and len(m.M) == 2:
        result = (m.M[0][0] * m.M[1][1]) - (m.M[1][0] * m.M[0][1])
        return result


# Funkcja liczaca wyznacznik macierzy metoda Chio
def chio(m: Matrix, frac=1):  # frac = znak oraz ułamek
    shape = len(m.M)

    while 2 < shape:
        # Aby obliczyc wyznacznik macierzy, ktora w lewym gornym rogu posiada liczbe 0, nalezy
        # po prostu wykonac operacje zamiany wierszy
        if m.M[0][0] == 0:
            for i in range(shape):
                if m.M[i][0] != 0:
                    temp = m.M[0]
                    m.M[0] = m.M[i]
                    m.M[i] = temp

        frac = frac * (1/m.M[0][0]) ** (shape - 2)
        new_m = Matrix((shape-1, shape-1), 0)

        for i in range(1, shape):
            for j in range(1, shape):
                minor = Matrix([[m.M[0][0], m.M[0][j]], [m.M[i][0], m.M[i][j]]])
                new_m.M[i - 1][j - 1] = det(minor)

        for i in range(shape - 1):
            for j in range(shape - 1):
                m.M[i][j] = new_m.M[i][j]

        shape = shape - 1

    m2x2 = Matrix([[m.M[0][0], m.M[0][1]], [m.M[1][0], m.M[1][1]]])
    result = int(frac * det(m2x2))

    return result


if __name__ == '__main__':
    M = Matrix([[5, 1, 1, 2, 3], [4, 2, 1, 7, 3], [2, 1, 2, 4, 7], [9, 1, 0, 7, 0], [1, 4, 7, 2, 2]])
    M2 = Matrix([[0, 1, 1, 2, 3], [4, 2, 1, 7, 3], [2, 1, 2, 4, 7], [9, 1, 0, 7, 0], [1, 4, 7, 2, 2]])

    print('Pierwsza zadana macierz:')
    print(M)
    print('Wyznacznik obliczony metoda Chio: {}\n'.format(chio(M)))
    print('Druga zadana macierz:')
    print(M2)
    print('Wyznacznik obliczony metoda Chio: {}\n'.format(chio(M2)))
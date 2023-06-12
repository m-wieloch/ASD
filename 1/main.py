#!/usr/bin/python
# -*- coding: utf-8 -*-
# Maciej Wieloch, 303080

from typing import Tuple


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

    def __add__(self, other):
        result = Matrix(matrix=(self.rows, self.cols))

        if isinstance(other, Matrix) and (other.rows == self.rows and other.cols == self.cols):
            for r in range(self.rows):
                for c in range(self.cols):
                    result.M[r][c] = self.M[r][c] + other.M[r][c]

            return result
        else:
            return 'Element is not a matrix or dimensions doesnt agree'

    def __mul__(self, other):
        result = Matrix(matrix=(self.rows, other.cols))

        if isinstance(other, Matrix):
            if self.rows == other.cols:
                for r in range(self.rows):
                    for c in range(other.cols):
                        for ro in range(other.rows):
                            result.M[r][c] += self.M[r][ro] * other.M[ro][c]

            return result
        else:
            return 'Element is not a matrix or dimensions doesnt agree'

    def __str__(self):
        output = ''
        for i in range(len(self.M)):
            output += '{}'.format(self.M[i]) + '\n'

        return output

    def __getitem__(self, item):  # by wywolac trzeba wpisywac w formie [r, c] a nie [r][c]
        if isinstance(item, Tuple):
            r, c = item
            return self.M[r][c]


def transpose(m: Matrix) -> Matrix:
    result = Matrix((m.cols, m.rows))

    for i in range(m.rows):
        for j in range(m.cols):
            result.M[j][i] = m.M[i][j]

    return result


if __name__ == '__main__':
    M1 = Matrix(([[1, 0, 2], [-1, 3, 1]]))
    M2 = Matrix(([[-1, 3, 1], [1, 0, 2]]))
    M3 = Matrix([[3, 1], [2, 1], [1, 0]])

    print('Macierz M1:')
    print(M1)
    print('Macierz transponowana:')
    print(transpose(M1))
    print('Macierz M2:')
    print(M2)
    print('Suma macierzy M1 i M2')
    print(M1 + M2)
    print('Macierz M3:')
    print(M3)
    print('Iloczyn macierzy M1 i M3')
    print(M1 * M3)

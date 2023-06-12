#!/usr/bin/python
# -*- coding: utf-8 -*-
# Maciej Wieloch, 303080

import numpy as np


class MatrixGraph:
    def __init__(self, graph=None):
        self.graph = []
        self.vertex_count = 0
        self.edges_count = 0
        self.vertexes = []

    def insertVertex(self, data, vertex_id):
        zeros = vertex_id * [0]

        if not self.graph:
            while vertex_id > len(self.graph):
                self.graph.append(zeros[:])

        elif len(self.graph) is not vertex_id:
            diff = vertex_id - len(self.graph)
            for i in range(len(self.graph)):
                for _ in range(diff):
                    self.graph[i].append(0)

            while vertex_id > len(self.graph):
                self.graph.append(zeros[:])

        # Dodawanie danych???
        if data is None:
            self.vertex_count = self.vertex_count - 1
            data = self.graph[vertex_id - 1][vertex_id - 1]

        # self.graph[vertex_id - 1][vertex_id - 1] = data
        self.vertexes.append(data)
        self.vertex_count = self.vertex_count + 1

    def insertEdge(self, vertex1_id, vertex2_id):
        if len(self.graph) < vertex1_id:
            print('There is no vertex_id: {}. Create vertex first.'.format(vertex1_id))

        elif len(self.graph) < vertex2_id:
            print('There is no vertex_id: {}. Create vertex first.'.format(vertex2_id))

        else:
            if not self.graph[vertex1_id - 1][vertex2_id - 1] == 1:
                self.graph[vertex1_id - 1][vertex2_id - 1] = 1
                self.edges_count = self.edges_count + 1
            else:
                print('Edge between {} -> {} already exists.'.format(vertex1_id, vertex2_id))

    def deleteVertex(self, vertex_id):
        if len(self.graph) >= vertex_id:
            for i in range(len(self.graph)):
                if self.graph[vertex_id - 1][i] == 1 or self.graph[i][vertex_id - 1] == 1:
                    self.edges_count = self.edges_count - 1
                self.graph[vertex_id - 1][i] = 0
                self.graph[i][vertex_id - 1] = 0

            self.vertex_count = self.vertex_count - 1
        else:
            print('There is no vertex_id = {}'.format(vertex_id))

    def deleteEdge(self, vertex1_id, vertex2_id):
        if len(self.graph) >= vertex1_id and len(self.graph) >= vertex2_id:
            if not self.graph[vertex1_id - 1][vertex2_id - 1] == 0:
                if not vertex1_id == vertex2_id:
                    self.graph[vertex1_id - 1][vertex2_id - 1] = 0
                    self.edges_count = self.edges_count - 1
                else:
                    print('Cant delete vertex {}. Use deleteVertex instead.'.format(vertex1_id))
            else:
                print('Edge between {} -> {} is already deleted.'.format(vertex1_id, vertex2_id))
        else:
            if len(self.graph) < vertex1_id:
                print('There is no vertex_id = {}'.format(vertex1_id))
            if len(self.graph) < vertex2_id:
                print('There is no vertex_id = {}'.format(vertex2_id))

    def getVertexIdx(self, key):
        for i in range(len(self.vertexes)):
            if self.vertexes[i] == key:
                return i + 1
        return None

    def getVertex(self, vertex_id):
        if len(self.graph) < vertex_id:
            print('There is no vertex_id = {}'.format(vertex_id))
        else:
            return self.graph[vertex_id - 1][vertex_id - 1]

    def neighbours(self, vertex_id):
        if len(self.graph) < vertex_id:
            print('There is no vertex_id = {}'.format(vertex_id))
        else:
            neighbours = []
            vertex = self.graph[vertex_id - 1]

            for edge in range(len(vertex)):
                if vertex[edge] == 1:
                    # lista id węzłów przyległych do węzła o podanym id
                    neighbours.append(edge + 1)

            return neighbours

    def order(self):
        return self.vertex_count

    def size(self):
        return self.edges_count

    def edges(self):
        edges = []
        for i in range(len(self.graph)):
            for j in range(len(self.graph)):
                if self.graph[i][j] == 1:
                    edges.append((self.graph[i][i], self.graph[j][j]))
        return edges


def isomorphism(G, P, M):
    for i in range(len(M)):
        if sum(M[i]) == 1:
            continue
        else:
            return False

    array_M = np.array(M)

    for j in range(len(M[0])):
        if sum(array_M.T[j]) <= 1:
            continue
        else:
            return False

    array_G = np.array(G.graph)
    array_P = np.array(P.graph)

    if (np.matmul(array_M, np.matmul(array_M, array_G).T) == array_P).all():
        return True

    return False


def ullman_v1(used_columns, current_row, G, P, M):
    global no_recursion
    no_recursion = no_recursion + 1

    if current_row == len(M):
        if isomorphism(G, P, M):
            print(f'M:\n{np.array(M)}')
            return M
        else:
            return M

    _M = M.copy()
    columns = [i for i in range(len(M[0]))]

    if used_columns is None:
        used_columns = list()

    for col in used_columns:
        if col in columns:
            columns.remove(col)

    if columns:
        for unused_col in columns:
            used_columns.append(unused_col)
            _M[current_row] = [0 for _ in _M[current_row]]
            _M[current_row][unused_col] = 1

            ullman_v1(used_columns, current_row + 1, G, P, _M)

            used_columns.remove(unused_col)
    else:
        _M[current_row] = [0 for _ in _M[current_row]]
        ullman_v1(used_columns, current_row + 1, G, P, _M)


def create_M0(G, P):
    M = []
    for r in range(len(P.graph)):
        M.append([])
        for c in range(len(G.graph)):
            M[r].append(0)

    for r in range(len(M)):
        for c in range(len(M[r])):
            vi = sum(P.graph[r])
            vj = sum(G.graph[c])

            if vi <= vj:
                M[r][c] = 1

    return M


def ullman_v2(used_columns, current_row, G, P, M=None):
    global no_recursion
    no_recursion = no_recursion + 1

    if M is None:
        M = create_M0(G, P)
        print(f'M_0:\n{np.array(M)}')

    if current_row == len(M):
        if isomorphism(G, P, M):
            print(f'M:\n{np.array(M)}')
            return M
        else:
            return M

    _M = M.copy()
    columns = [i for i in range(len(M[0]))]

    if used_columns is None:
        used_columns = list()

    for col in used_columns:
        if col in columns:
            columns.remove(col)

    modified = True
    if columns:
        for unused_col in columns:
            if M[current_row][unused_col] == 1:
                used_columns.append(unused_col)
                _M[current_row] = [0 for _ in _M[current_row]]
                _M[current_row][unused_col] = 1

                ullman_v2(used_columns, current_row + 1, G, P, _M)

                used_columns.remove(unused_col)

                modified = True
            else:
                modified = False
                continue

    if not modified or not columns:
        _M[current_row] = [0 for _ in _M[current_row]]
        ullman_v2(used_columns, current_row + 1, G, P, _M)


def prune(G, P, M):
    changed = True
    while changed:
        changed = False
        for r in range(len(M)):
            for c in range(len(M[r])):
                if M[r][c] == 1:
                    neighbour = True
                    for x in range(len(M)):
                        if P.graph[r][x] == 1:
                            for y in range(len(M[r])):
                                if G.graph[c][y] == 1:
                                    if M[x][y] == 1:
                                        neighbour = False
                    if neighbour:
                        M[r][c] = 0
                        changed = True
                else:
                    continue
    return M


def ullman_v3(used_columns, current_row, G, P, M=None):
    global no_recursion
    no_recursion = no_recursion + 1

    if M is None:
        M = create_M0(G, P)
        print(f'M_0:\n{np.array(M)}')

    if current_row == len(M):
        if isomorphism(G, P, M):
            print(f'M:\n{np.array(M)}')
            return M
        else:
            return M

    M = prune(G, P, M)
    # print(f'MPRUNE:\n{np.array(M)}')
    _M = M.copy()
    columns = [i for i in range(len(M[0]))]

    if used_columns is None:
        used_columns = list()

    for col in used_columns:
        if col in columns:
            columns.remove(col)

    modified = True
    if columns:
        for unused_col in columns:
            if M[current_row][unused_col] == 1:
                used_columns.append(unused_col)
                _M[current_row] = [0 for _ in _M[current_row]]
                _M[current_row][unused_col] = 1

                ullman_v3(used_columns, current_row + 1, G, P, _M)

                used_columns.remove(unused_col)

                modified = True
            else:
                modified = False
                continue

    if not modified or not columns:
        _M[current_row] = [0 for _ in _M[current_row]]
        ullman_v3(used_columns, current_row + 1, G, P, _M)


if __name__ == "__main__":
    # Inicjalizacja
    graph_G = [('A', 'B', 1), ('B', 'F', 1), ('B', 'C', 1), ('C', 'D', 1), ('C', 'E', 1), ('D', 'E', 1)]
    graph_P = [('A', 'B', 1), ('B', 'C', 1), ('A', 'C', 1)]

    testG = MatrixGraph()
    G_vertexes = ['A', 'B', 'C', 'D', 'E', 'F']

    # Macierz G
    for vertex in range(len(G_vertexes)):
        testG.insertVertex(G_vertexes[vertex], vertex + 1)

    for edges in graph_G:
        testG.insertEdge(testG.getVertexIdx(edges[0]), testG.getVertexIdx(edges[1]))
        testG.insertEdge(testG.getVertexIdx(edges[1]), testG.getVertexIdx(edges[0]))

    testP = MatrixGraph()
    P_vertexes = ['A', 'B', 'C']

    # Macierz P
    for vertex in range(len(P_vertexes)):
        testP.insertVertex(P_vertexes[vertex], vertex + 1)

    for edges in graph_P:
        testP.insertEdge(testP.getVertexIdx(edges[0]), testP.getVertexIdx(edges[1]))
        testP.insertEdge(testP.getVertexIdx(edges[1]), testP.getVertexIdx(edges[0]))

    # Macierz M jedynek
    testM = []
    for r in range(len(P_vertexes)):
        testM.append([])
        for c in range(len(G_vertexes)):
            testM[r].append(1)

    # Ullman v1
    no_recursion = 0
    print(f'G:\n{np.array(testG.graph)}')
    print(f'P:\n{np.array(testP.graph)}')
    print(f'M_0:\n{np.array(testM)}')
    result1 = ullman_v1(None, 0, testG, testP, testM)
    print(f'\nNo. recursions: {no_recursion}')

    # Ullman v2
    no_recursion = 0
    print(f'G:\n{np.array(testG.graph)}')
    print(f'P:\n{np.array(testP.graph)}')
    result2 = ullman_v2(None, 0, testG, testP)
    print(f'\nNo. recursions: {no_recursion}')

    # Ullman v3
    no_recursion = 0
    print(f'G:\n{np.array(testG.graph)}')
    print(f'P:\n{np.array(testP.graph)}')
    result3 = ullman_v3(None, 0, testG, testP)
    print(f'\nNo. recursions: {no_recursion}')

#!/usr/bin/python
# -*- coding: utf-8 -*-
# Maciej Wieloch, 303080

import polska

"""
    insertVertex(data, vertex_id)           - wstawia do grafu węzeł z podaną daną  (vertex_id - dla implementacji, gdzie id
                                            jest kluczem a nie numerem węzła)
    insertEdge(vertex1_id, vertex2_id)  - wstawia do grafu krawędź pomiędzy węzły o podanych id
    deleteVertex(vertex_id)             - usuwa węzeł o podanym id
    deleteEdge(vertex1_id, vertex2_id)  - usuwa krawędź pomiędzy z węzłami o podanych id        
    getVertexIdx(key)                   - zwraca id węzła zawierającego daną z podanym kluczem  (dla implementacji, 
                                            gdzie id jest numerem węzła a nie kluczem)
    getVertex(vertex_id)                - zwraca węzeł o podanym id
    neighbours(vertex_id)               - zwraca listę id węzłów przyległych do węzła o podanym id (połączenia 
                                            wyjściowe)
    order()                             - zwraca rząd grafu (liczbę węzłów)
    size()                              - zwraca rozmiar grafu (liczbę krawędzi)

Dodatkowo potrzeba będzie metoda:
    edges() -   zwracająca wszystkie krawędzie grafu w postaci listy par: (klucz_węzła_początkowego, 
                klucz_węzła_końcowego) - taka implementacja nie jest standardowa, ale będzie dla nas 
                bardziej przydatna do wyrysowania grafu.
"""


class MatrixGraph:
    def __init__(self, graph=None):
        self.graph = []
        self.vertex_count = 0
        self.edges_count = 0

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

        self.graph[vertex_id - 1][vertex_id - 1] = data
        self.vertex_count = self.vertex_count + 1

    def insertEdge(self, vertex1_id, vertex2_id):
        if len(self.graph) < vertex1_id:
            print('There is no vertex_id: {}. Create vertex first.'.format(vertex1_id))

        elif len(self.graph) < vertex2_id:
            print('There is no vertex_id: {}. Create vertex first.'.format(vertex2_id))

        elif self.graph[vertex1_id - 1][vertex1_id - 1] == 0:
            print('{} vertex has no data. Create vertex first.'.format(vertex1_id))

        elif self.graph[vertex2_id - 1][vertex2_id - 1] == 0:
            print('{} vertex has no data. Create vertex first.'.format(vertex2_id))

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
        for i in range(len(self.graph)):
            if self.graph[i][i] == key:
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
                    neighbours.append(edge+1)

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


class ListGraph:
    def __init__(self):
        self.graph = []
        self.data = []
        self.vertex_count = 0
        self.edges_count = 0

    def insertVertex(self, data, vertex_id):
        while len(self.graph) < vertex_id:
            self.graph.append([])
            self.data.append([])

        self.data[vertex_id - 1] = data
        self.vertex_count = self.vertex_count + 1

    def insertEdge(self, vertex1_id, vertex2_id):
        if len(self.graph) < vertex1_id:
            print('There is no vertex_id: {}. Create vertex first.'.format(vertex1_id))

        elif len(self.graph) < vertex2_id:
            print('There is no vertex_id: {}. Create vertex first.'.format(vertex2_id))

        elif not self.data[vertex1_id - 1]:
            print('{} vertex has no data. Create vertex first.'.format(vertex1_id))

        elif not self.data[vertex2_id - 1]:
            print('{} vertex has no data. Create vertex first.'.format(vertex2_id))

        else:
            self.graph[vertex1_id - 1].append(vertex2_id)
            self.edges_count = self.edges_count + 1

    def deleteVertex(self, vertex_id):
        if len(self.graph) >= vertex_id:
            for vertex in self.graph:
                for edge in range(len(vertex)):
                    if vertex[edge] == vertex_id:
                        vertex.pop(edge)
                        self.edges_count = self.edges_count - 1
                        break
            self.graph[vertex_id - 1] = []
            self.data[vertex_id - 1] = []
            self.vertex_count = self.vertex_count - 1
        else:
            print('There is no vertex_id = {}'.format(vertex_id))

    def deleteEdge(self, vertex1_id, vertex2_id):
        if len(self.graph) >= vertex1_id and len(self.graph) >= vertex2_id:
            for edge in range(len(self.graph[vertex1_id - 1])):
                if self.graph[vertex1_id - 1][edge] == vertex2_id:
                    self.graph[vertex1_id - 1].pop(edge)
                    self.edges_count = self.edges_count - 1
                    break
        else:
            if len(self.graph) < vertex1_id:
                print('There is no vertex_id = {}'.format(vertex1_id))
            if len(self.graph) < vertex2_id:
                print('There is no vertex_id = {}'.format(vertex2_id))

    def getVertexIdx(self, key):
        for vertex_id in range(len(self.data)):
            if self.data[vertex_id] == key:
                return vertex_id + 1

        return None

    def neighbours(self, vertex_id):
        if len(self.graph) < vertex_id:
            print('There is no vertex_id: {}. Create vertex first.'.format(vertex_id))
        elif not self.data[vertex_id - 1]:
            print('There is no vertex_id: {}. Create vertex first.'.format(vertex_id))
        else:
            return self.graph[vertex_id - 1]

    def order(self):
        return self.vertex_count

    def size(self):
        return self.edges_count

    def edges(self):
        edges = []
        for i in range(len(self.graph)):
            for j in self.graph[i]:
                edges.append((self.data[i], self.data[j - 1]))
        return edges


if __name__ == '__main__':

    graph_m = MatrixGraph()
    graph_l = ListGraph()

    idx = 1
    for i in polska.slownik.keys():
        graph_l.insertVertex(i, idx)
        graph_m.insertVertex(i, idx)
        idx = idx + 1

    for i in range(len(polska.graf)):
        graph_l.insertEdge(graph_l.getVertexIdx(polska.graf[i][0]), graph_l.getVertexIdx(polska.graf[i][1]))
        graph_m.insertEdge(graph_l.getVertexIdx(polska.graf[i][0]), graph_l.getVertexIdx(polska.graf[i][1]))

    graph_l.deleteVertex(graph_l.getVertexIdx('K'))

    graph_m.deleteVertex(graph_m.getVertexIdx('K'))

    graph_l.deleteEdge(graph_l.getVertexIdx('W'), graph_l.getVertexIdx('E'))
    graph_l.deleteEdge(graph_l.getVertexIdx('E'), graph_l.getVertexIdx('W'))

    graph_m.deleteEdge(graph_m.getVertexIdx('W'), graph_m.getVertexIdx('E'))
    graph_m.deleteEdge(graph_m.getVertexIdx('E'), graph_m.getVertexIdx('W'))

    print(graph_l.edges())
    print(graph_m.edges())

    polska.draw_map(graph_l.edges())
    polska.draw_map(graph_m.edges())

    print('HW')

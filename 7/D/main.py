#!/usr/bin/python
# -*- coding: utf-8 -*-
# Maciej Wieloch, 303080

import polska

"""
    insertVertex(data, vertex_id)         - wstawia do grafu węzeł z podaną daną  (vertex_id - dla implementacji, gdzie id jest kluczem a nie numerem węzła)
    insertEdge(vertex1_id, vertex2_id) - wstawia do grafu krawędź pomiędzy węzły o podanych id
    deleteVertex(vertex_id) - usuwa węzeł o podanym id
    deleteEdge(vertex1_id, vertex2_id) - usuwa krawędź pomiędzy z węzłami o podanych id
    getVertexIdx(key)          - zwraca id węzła zawierającego daną z podanym kluczem  (dla implementacji, gdzie id jest numerem węzła a nie kluczem)
    getVertex(vertex_id)    - zwraca węzeł o podanym id
    neighbours(vertex_id)    - zwraca listę id węzłów przyległych do węzła o podanym id (połączenia wyjściowe)
    order()                    - zwraca rząd grafu (liczbę węzłów)
    size()                    - zwraca rozmiar grafu (liczbę krawędzi)
Dodatkowo potrzeba będzie metoda:
    edges() - zwracająca wszystkie krawędzie grafu w postaci listy par: (klucz_węzła_początkowego, klucz_węzła_końcowego) - taka implementacja nie jest standardowa, ale będzie dla nas bardziej przydatna do wyrysowania grafu.
"""


class ForwardStar:
    def __init__(self):
        self.vertex_list = []
        self.edge_list = []

    def insertVertex(self, data):
        is_inserted = False

        for vertex in self.vertex_list:
            if vertex[0] is data:
                is_inserted = True
                break

        if not is_inserted:
            self.vertex_list.append([data, None])

    def insertEdge(self, vertex1_id, vertex2_id):
        self.edge_list.append([vertex1_id, vertex2_id])
        self.edge_list.sort(key=self._sorting_edges_function)

        for vertex in self.vertex_list:
            edge_to_vertex = vertex[0]
            for edge in range(len(self.edge_list)):
                if edge is (len(self.edge_list) - 1):
                    vertex[1] = None

                if self.edge_list[edge][0] is edge_to_vertex:
                    vertex[1] = edge
                    break

    def deleteVertex(self, vertex_id):
        data = self.getVertex(vertex_id)

        edges_to_delete = []
        for i in range(len(self.edge_list)):
            if data in self.edge_list[i]:
                if self.edge_list[i][0] is data:
                    edges_to_delete.append([vertex_id, self.getVertexIdx(self.edge_list[i][1])])
                if self.edge_list[i][1] is data:
                    edges_to_delete.append([self.getVertexIdx(self.edge_list[i][0]), vertex_id])

        for i in reversed(edges_to_delete):
            self.deleteEdge(i[0], i[1])

        self.vertex_list.pop(vertex_id)

    def deleteEdge(self, vertex1_id, vertex2_id):
        for i in range(len(self.edge_list)):
            if self.edge_list[i][0] == self.getVertex(vertex1_id) and self.edge_list[i][1] == self.getVertex(vertex2_id):
                self.edge_list.pop(i)
                break

        for vertex in self.vertex_list:
            edge_to_vertex = vertex[0]
            for edge in range(len(self.edge_list)):
                if edge is (len(self.edge_list) - 1):
                    vertex[1] = None

                if self.edge_list[edge][0] is edge_to_vertex:
                    vertex[1] = edge
                    break

    def getVertexIdx(self, key):
        for vertex in range(len(self.vertex_list)):
            if self.vertex_list[vertex][0] is key:
                return vertex

    def getVertex(self, vertex_id):
        if vertex_id is None:
            return None
        else:
            return self.vertex_list[vertex_id][0]

    def neighbours(self, vertex_id):
        neighbours_list = []

        for edge in range(len(self.edge_list)):
            if self.edge_list[edge][0] == self.getVertex(vertex_id):
                neighbours_list.append(self.edge_list[edge][1])

        return neighbours_list


    def order(self):
        return len(self.vertex_list)

    def size(self):
        return len(self.edge_list)

    def edges(self):
        result = []
        for edge in self.edge_list:
            result.append((edge[0], edge[1]))

        return result

    def _sorting_edges_function(self, edge):
        return self.getVertexIdx(edge[0])


if __name__ == '__main__':
    test = ForwardStar()

    for i in polska.graf:
        test.insertVertex(i[0])
        test.insertVertex(i[1])
        test.insertEdge(i[0], i[1])

    test.deleteVertex(test.getVertexIdx('K'))
    test.deleteEdge(test.getVertexIdx('W'), test.getVertexIdx('E'))
    test.deleteEdge(test.getVertexIdx('E'), test.getVertexIdx('W'))

    print(test.edge_list)

    polska.draw_map(test.edges())

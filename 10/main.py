#!/usr/bin/python
# -*- coding: utf-8 -*-
# Maciej Wieloch, 303080

import sys


class ListGraph:
    def __init__(self):
        self.vertex_list = []
        self.edges = []
        self.graph_dict = {}

    def insertVertex(self, vertex_id):
        if vertex_id not in self.graph_dict:
            self.graph_dict[vertex_id] = []
            self.vertex_list.append(vertex_id)

    def insertEdge(self, vertex1_id, vertex2_id, weight):
        if vertex1_id not in self.graph_dict:
            self.insertVertex(vertex1_id)

        if vertex2_id not in self.graph_dict:
            self.insertVertex(vertex2_id)

        self.graph_dict[vertex1_id].append((vertex2_id, weight))
        self.edges.append((vertex1_id, vertex2_id, weight))

    def deleteVertex(self, vertex_id):
        del self.graph_dict[vertex_id]

        for vertex in range(len(self.vertex_list)):
            if self.vertex_list[vertex][0] == vertex_id:
                self.vertex_list.pop(vertex)

        for d_key, d_val in self.graph_dict.items():
            elements = []
            for vertex in range(len(self.graph_dict[d_key])):
                if self.graph_dict[d_key][vertex][0] == vertex_id:
                    elements.append(vertex)

            for vertex in range(len(elements)):
                self.graph_dict[d_key].pop(elements[vertex])

        elements = []
        for edge in range(len(self.edges)):
            if self.edges[edge][0] == vertex_id or self.edges[edge][1] == vertex_id:
                elements.append(edge)

        for edge in reversed(range(0, len(elements))):
            self.edges.pop(elements[edge])

    def deleteEdge(self, vertex1_id, vertex2_id):
        element = None

        for edge in range(len(self.graph_dict[vertex1_id])):
            if self.graph_dict[vertex1_id][edge][0] == vertex2_id:
                element = edge

        if element is not None:
            self.graph_dict[vertex1_id].pop(element)

        element = None
        for edge in range(len(self.graph_dict[vertex2_id])):
            if self.graph_dict[vertex2_id][edge][0] == vertex1_id:
                element = edge

        if element is not None:
            self.graph_dict[vertex2_id].pop(element)

        elements = []
        for edge in range(len(self.edges)):
            if self.edges[edge][0] == vertex1_id and self.edges[edge][1] == vertex2_id:
                elements.append(edge)
            if self.edges[edge][0] == vertex2_id and self.edges[edge][1] == vertex1_id:
                elements.append(edge)

        for edge in reversed(range(0, len(elements))):
            self.edges.pop(elements[edge])

    def neighbours(self, vertex_id):
        neighbours = []
        for vertex in range(len(self.graph_dict[vertex_id])):
            neighbours.append(self.graph_dict[vertex_id][vertex][0])

        return neighbours

    def order(self):
        return len(self.vertex_list)

    def size(self):
        return len(self.edges)

    def edges(self):
        edges = []
        for edge in range(len(self.edges)):
            edges.append((self.edges[edge][0], self.edges[edge][1]))

        return edges

    def updateEdge(self, vertex1_id, vertex2_id, new_weight):
        element = None
        for edge in range(len(self.graph_dict[vertex1_id])):
            if self.graph_dict[vertex1_id][edge][0] == vertex2_id:
                element = edge

        if element is not None:
            self.graph_dict[vertex1_id].pop(element)

        elements = []
        for edge in range(len(self.edges)):
            if self.edges[edge][0] == vertex1_id and self.edges[edge][1] == vertex2_id:
                elements.append(edge)

        for edge in reversed(range(0, len(elements))):
            self.edges.pop(elements[edge])

        if new_weight != 0:
            self.graph_dict[vertex1_id].append((vertex2_id, new_weight))
            self.edges.append((vertex1_id, vertex2_id, new_weight))

    def dict2list(self, key):
        temp_key = 0
        temp_dict = {}

        for d_key, d_val in self.graph_dict.items():
            temp_dict[d_key] = temp_key
            temp_key = temp_key + 1

        return temp_dict[key]

    def list2dict(self, index):
        temp_key = 0
        temp_dict = {}

        for d_key, d_val in self.graph_dict.items():
            temp_dict[temp_key] = d_key
            temp_key = temp_key + 1

        return temp_dict[index]

    def weights(self, vertex_id1, vertex_id2):
        weight = 0
        for edge in range(len(self.edges)):
            if self.edges[edge][0] == vertex_id1 and self.edges[edge][1] == vertex_id2:
                weight = self.edges[edge][2]

        return weight

    def BFS(self, start, end, parent):
        visited = [False for _ in range(self.order())]
        queue = [self.dict2list(start)]
        visited[self.dict2list(start)] = True

        while queue:
            element = queue.pop(0)
            neighbours = self.neighbours(self.list2dict(element))

            for index in range(len(neighbours)):
                v = self.dict2list(neighbours[index])
                if not visited[v]:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = element

        if not visited[self.dict2list(end)]:
            return False
        else:
            return True

    def max_flow(self, source, sink):
        parent = [-1 for _ in range(self.order())]
        flow = 0

        while self.BFS(source, sink, parent):
            flow_path = sys.maxsize
            vertex = self.dict2list(sink)

            while vertex != self.dict2list(source):
                flow_path = min(flow_path, self.weights(self.list2dict(parent[vertex]), self.list2dict(vertex)))
                vertex = parent[vertex]

            flow = flow + flow_path
            v = self.dict2list(sink)
            while v != self.dict2list(source):
                u = parent[v]

                u_weight = self.weights(self.list2dict(u), self.list2dict(v))
                self.updateEdge(self.list2dict(u), self.list2dict(v), (u_weight - flow_path))

                v_weight = self.weights(self.list2dict(v), self.list2dict(u))
                self.updateEdge(self.list2dict(v), self.list2dict(u), (v_weight + flow_path))

                v = parent[v]

        return flow


if __name__ == "__main__":
    # Wynik 3
    graf_0 = [('s', 'u', 2), ('u', 't', 1), ('u', 'v', 3), ('s', 'v', 1), ('v', 't', 2)]
    G0 = ListGraph()
    for i in range(len(graf_0)):
        G0.insertEdge(graf_0[i][0], graf_0[i][1], graf_0[i][2])
    print('Maksymalny przepływ dla grafu: \n{},\nwynosi: {}'.format(G0.graph_dict, G0.max_flow('s', 't')))

    # Wynik 23
    graf_1 = [('s', 'a', 16), ('s', 'c', 13), ('a', 'c', 10), ('c', 'a', 4), ('a', 'b', 12), ('b', 'c', 9),
              ('b', 't', 20), ('c', 'd', 14), ('d', 'b', 7), ('d', 't', 4)]
    G1 = ListGraph()
    for i in range(len(graf_1)):
        G1.insertEdge(graf_1[i][0], graf_1[i][1], graf_1[i][2])
    print('\nMaksymalny przepływ dla grafu: \n{},\nwynosi: {}'.format(G1.graph_dict, G1.max_flow('s', 't')))

    # Wynik 5
    graf_2 = [('s', 'a', 3), ('s', 'c', 3), ('a', 'b', 4), ('b', 's', 3), ('b', 'c', 1), ('b', 'd', 2), ('c', 'e', 6),
              ('c', 'd', 2), ('d', 't', 1), ('e', 't', 9)]
    G2 = ListGraph()
    for i in range(len(graf_2)):
        G2.insertEdge(graf_2[i][0], graf_2[i][1], graf_2[i][2])
    print('\nMaksymalny przepływ dla grafu: \n{},\nwynosi: {}'.format(G2.graph_dict, G2.max_flow('s', 't')))

    # Wynik 6
    graf_3 = [('s', 'a', 8), ('s', 'd', 3), ('a', 'b', 9), ('b', 'd', 7), ('b', 't', 2), ('c', 't', 5), ('d', 'b', 7),
              ('d', 'c', 4)]
    G3 = ListGraph()
    for i in range(len(graf_3)):
        G3.insertEdge(graf_3[i][0], graf_3[i][1], graf_3[i][2])
    print('\nMaksymalny przepływ dla grafu: \n{},\nwynosi: {}'.format(G3.graph_dict, G3.max_flow('s', 't')))

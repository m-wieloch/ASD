#!/usr/bin/python
# -*- coding: utf-8 -*-
# Maciej Wieloch, 303080

import graf_mst
import sys


class ListGraph:
    def __init__(self):
        self.graph = []
        self.data = []
        self.color = []
        self.vertex_count = 0
        self.edges_count = 0

    def insertVertex(self, data, vertex_id, color=None):
        while len(self.graph) < vertex_id:
            self.graph.append([])
            self.data.append([])
            self.color.append([])

        self.data[vertex_id - 1] = data
        self.vertex_count = self.vertex_count + 1
        self.color[vertex_id - 1] = color

    def insertEdge(self, vertex1_id, vertex2_id, weight=1):
        if len(self.graph) < vertex1_id:
            print('There is no vertex_id: {}. Create vertex first.'.format(vertex1_id))

        elif len(self.graph) < vertex2_id:
            print('There is no vertex_id: {}. Create vertex first.'.format(vertex2_id))

        elif not self.data[vertex1_id - 1]:
            print('{} vertex has no data. Create vertex first.'.format(vertex1_id))

        elif not self.data[vertex2_id - 1]:
            print('{} vertex has no data. Create vertex first.'.format(vertex2_id))

        else:
            self.graph[vertex1_id - 1].append((vertex2_id, weight))     # self.graph[vertex1_id - 1].append(vertex2_id)
            self.edges_count = self.edges_count + 1

    def deleteVertex(self, vertex_id):
        if len(self.graph) >= vertex_id:
            for vertex in self.graph:
                for edge in range(len(vertex)):
                    if vertex[edge][0] == vertex_id:    # if vertex[edge] == vertex_id:
                        vertex.pop(edge)
                        self.edges_count = self.edges_count - 1
                        break

            self.graph.pop(vertex_id - 1)   # self.graph[vertex_id - 1] = []
            self.data.pop(vertex_id - 1)    # self.data[vertex_id - 1] = []
            self.color.pop(vertex_id - 1)
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
        if vertex_id is None:
            return []
        if len(self.graph) < vertex_id:
            print('There is no vertex_id: {}. Create vertex first.'.format(vertex_id))
        elif not self.data[vertex_id - 1]:
            print('There is no vertex_id: {}. Create vertex first.'.format(vertex_id))
        else:
            result = []
            for i in self.graph[vertex_id - 1]:
                result.append(i[0])
            return result

    def order(self):
        return self.vertex_count

    def size(self):
        return self.edges_count

    def edges(self):
        edges = []
        for i in range(len(self.graph)):
            for j in self.graph[i][0]:  # self.graph[i]
                edges.append((self.data[i], self.data[j - 1]))
        return edges

    def weight(self, vertex1_id, vertex2_id):
        for i in self.graph[vertex1_id - 1]:
            if i[0] == vertex2_id:
                return i[1]
        return None


def mst(g, s):
    e_sum = 0
    edges = []
    alpha = {}
    beta = {}

    queue = []
    for i in range(g.vertex_count):
        alpha[g.getVertexIdx(g.data[i])] = 0
        beta[g.getVertexIdx(g.data[i])] = sys.maxsize
        queue.append(g.getVertexIdx(g.data[i]))

    del alpha[s]
    del beta[s]

    queue.remove(s)
    u_ = s

    while queue:
        for u in queue:
            neighbours = g.neighbours(u_)
            if u in neighbours:
                weight = g.weight(u, u_)
                if weight < beta[u]:
                    alpha[u] = u_
                    beta[u] = weight

        u_ = min(beta.items(), key=lambda x: x[1])[0]

        queue.remove(u_)
        edges.append(((g.data[alpha[u_] - 1], g.data[u_ - 1]), beta[u_]))
        e_sum = e_sum + g.weight(alpha[u_], u_)

        del alpha[u_]
        del beta[u_]

    result = edges, e_sum
    return result


if __name__ == '__main__':
    test = ListGraph()

    id = 1
    for v1, v2, w in graf_mst.graf:
        if v1 not in test.data:
            test.insertVertex(v1, id)
            id = id + 1
        if v2 not in test.data:
            test.insertVertex(v2, id)
            id = id + 1

        test.insertEdge(test.getVertexIdx(v1), test.getVertexIdx(v2), w)
        test.insertEdge(test.getVertexIdx(v2), test.getVertexIdx(v1), w)

    start = 'A'
    test_mst = mst(test, test.getVertexIdx(start))
    print('Dla grafu graf_mst, punktu startowego = {}, MST: \n{}\n'.format(start, test_mst[0]))
    print('Calkowity koszt przejścia: {}'.format(test_mst[1]))

#!/usr/bin/python
# -*- coding: utf-8 -*-
# Maciej Wieloch, 303080
import sys

import graf_mst


class UnionFind:
    def __init__(self, n):
        self.parent = [i for i in range(n)]
        self.size = [0 for _ in range(n)]

    def find(self, v):
        if self.parent[v] == v:
            return v
        else:
            return self.find(self.parent[v])

    def union_sets(self, s1, s2):
        s1 = self.find(s1)
        s2 = self.find(s2)

        if not self.same_component(s1, s2):
            if self.size[s1] > self.size[s2]:
                self.parent[s2] = s1
                if self.size[s2] + 1 >= self.size[s1]:
                    self.size[s1] = self.size[s2] + 1

            else:
                self.parent[s1] = s2
                if self.size[s1] + 1 >= self.size[s2]:
                    self.size[s2] = self.size[s1] + 1

    def same_component(self, s1, s2):
        if not self.find(s1) == self.find(s2):
            return False
        else:
            return True


class Graph:
    def __init__(self):
        self.graph = []
        self.vertex_list = []
        self.vertex_count = 0

    def __str__(self):
        result = ''
        for i in range(len(self.graph)):
            result = result + '[' + self.vertex_list[self.graph[i][0]] + ', ' + self.vertex_list[self.graph[i][1]] + ', ' + str(self.graph[i][2]) + ']'
            result = result + '\n'
        return result

    def insertEdge(self, vertex1_id, vertex2_id, weight):
        existing_edge = False

        if vertex1_id not in self.vertex_list:
            self.vertex_list.append(vertex1_id)
            vertex1_id = self.vertex_count
            self.vertex_count = self.vertex_count + 1

        if vertex2_id not in self.vertex_list:
            self.vertex_list.append(vertex2_id)
            vertex2_id = self.vertex_count
            self.vertex_count = self.vertex_count + 1

        index = 0
        for i in self.vertex_list:
            if i == vertex1_id:
                vertex1_id = index
            if i == vertex2_id:
                vertex2_id = index
            index = index + 1

        edge = [vertex1_id, vertex2_id, weight]
        for i in self.graph:
            if i == edge:
                existing_edge = True

        if not existing_edge:
            self.graph.append(edge)

    def order(self):
        return len(self.vertex_list)

    def weight(self, vertex1_id, vertex2_id):
        for i in self.graph:
            if i[0] == vertex1_id and i[1] == vertex2_id:
                return i[2]
        return sys.maxsize

    # def weight(self, vertex1_id, vertex2_id):
    #     for i in self.graph:
    #         if self.vertex_list[i[0]] == vertex1_id and self.vertex_list[i[1]] == vertex2_id:
    #             return i[2]
    #     return sys.maxsize

    def neighbours(self, vertex):
        result = []
        for i in self.graph:
            # if self.vertex_list[i[0]] == vertex:
            if i[0] == vertex:
                result.append(i[1])
                # result.append(self.vertex_list[i[1]])
        return result

def mst(g, s):
    result_mst = Graph()
    e_sum = 0
    alpha = {}
    beta = {}

    queue = []
    for i in range(g.vertex_count):
        alpha[g.vertex_list[i]] = 0
        beta[g.vertex_list[i]] = sys.maxsize
        queue.append(g.vertex_list[i])

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
        result_mst.insertEdge(alpha[u_], u_, beta[u_])
        e_sum = e_sum + g.weight(alpha[u_], u_)

        del alpha[u_]
        del beta[u_]

    result = result_mst, e_sum
    return result


if __name__ == '__main__':
    test = Graph()

    for edges in graf_mst.graf:
        test.insertEdge(edges[0], edges[1], edges[2])
        test.insertEdge(edges[1], edges[0], edges[2])

    test_mst = mst(test, 'D')

    print('MST grafu:')
    print(test_mst[0])
    print('Koszt: {}'.format(test_mst[1]))

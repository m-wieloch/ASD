#!/usr/bin/python
# -*- coding: utf-8 -*-
# Maciej Wieloch, 303080

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


def MST(graph):
    result = Graph()
    cost = 0
    count = 0
    graph_union = UnionFind(graph.order())

    graph_edges = graph.graph
    graph_edges = sorted(graph_edges, key=lambda index: index[2])

    while count < graph.order() - 1:
        edge = graph_edges.pop(0)

        if not graph_union.same_component(edge[0], edge[1]):
            result.insertEdge(graph.vertex_list[edge[0]], graph.vertex_list[edge[1]], edge[2])
            graph_union.union_sets(edge[0], edge[1])
            count = count + 1
            cost = cost + edge[2]

    return result, cost


if __name__ == '__main__':
    test = Graph()

    for edges in graf_mst.graf:
        test.insertEdge(edges[0], edges[1], edges[2])
        test.insertEdge(edges[1], edges[0], edges[2])

    test_mst = MST(test)

    print('MST grafu:')
    print(test_mst[0])
    print('Koszt: {}'.format(test_mst[1]))

#!/usr/bin/python
# -*- coding: utf-8 -*-
# Maciej Wieloch, 303080

import sys
import cv2
import numpy as np
from matplotlib import pyplot as plt


class Graph:
    def __init__(self):
        self.graph = []
        self.vertex_list = []
        self.vertex_count = 0

    def __str__(self):
        result = ''
        for i in range(len(self.graph)):
            result = result + '[' + self.vertex_list[self.graph[i][0]] + ', ' + self.vertex_list[
                self.graph[i][1]] + ', ' + str(self.graph[i][2]) + ']'
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
    I = cv2.imread('sample.png', cv2.IMREAD_GRAYSCALE)
    I = I.astype('float32')

    test = Graph()

    (X, Y) = I.shape
    for i in range(0, X):
        for j in range(0, Y):
            if (i + 1) < (Y - 1):
                test.insertEdge((X * (i + 1) + j), X * i + j, abs(I[i + 1][j] - I[i][j]))
                test.insertEdge(X * i + j, (X * (i + 1) + j), abs(I[i + 1][j] - I[i][j]))
            if (i + 1) < (Y - 1) and (j - 1) > 0:
                test.insertEdge((X * (i + 1) + (j - 1)), X * i + j, abs(I[i + 1][j - 1] - I[i][j]))
                test.insertEdge(X * i + j, (X * (i + 1) + (j - 1)), abs(I[i + 1][j - 1] - I[i][j]))
            if (i - 1) > 0 and (j + 1) < (Y - 1):
                test.insertEdge((X * (i - 1) + (j + 1)), X * i + j, abs(I[i - 1][j + 1] - I[i][j]))
                test.insertEdge(X * i + j, (X * (i - 1) + (j + 1)), abs(I[i - 1][j + 1] - I[i][j]))
            if (j + 1) < (Y - 1):
                test.insertEdge((X * i + (j + 1)), X * i + j, abs(I[i][j + 1] - I[i][j]))
                test.insertEdge(X * i + j, (X * i + (j + 1)), abs(I[i][j + 1] - I[i][j]))
            if (j - 1) > 0:
                test.insertEdge((X * i + (j - 1)), X * i + j, abs(I[i][j - 1] - I[i][j]))
                test.insertEdge(X * i + j, (X * i + (j - 1)), abs(I[i][j - 1] - I[i][j]))
            if (i - 1) > 0 and (j - 1) > 0:
                test.insertEdge((X * (i - 1) + (j - 1)), X * i + j, abs(I[i - 1][j - 1] - I[i][j]))
                test.insertEdge(X * i + j, (X * (i - 1) + (j - 1)), abs(I[i - 1][j - 1] - I[i][j]))
            if (i - 1) > 0:
                test.insertEdge((X * (i - 1) + j), X * i + j, abs(I[i - 1][j] - I[i][j]))
                test.insertEdge(X * i + j, (X * (i - 1) + j), abs(I[i - 1][j] - I[i][j]))
            if (i + 1) < (Y - 1) and (j + 1) < (Y - 1):
                test.insertEdge((X * (i + 1) + (j + 1)), X * i + j, abs(I[i + 1][j + 1] - I[i][j]))
                test.insertEdge(X * i + j, (X * (i + 1) + (j + 1)), abs(I[i + 1][j + 1] - I[i][j]))

    prim_r, prim_c = mst(test, 99)
    prim_edges = prim_r.graph
    prim_edges_costs = []

    for i in prim_edges:
        prim_edges_costs.append(test.weight(i[0], i[1]))

    max_val = max(prim_edges_costs)
    max_id = 0

    for i in range(len(prim_edges_costs)):
        if prim_edges_costs[i] == max_val:
            max_id = i

    edge_begin = prim_edges[max_id][0]
    edge_end = prim_edges[max_id][1]
    prim_r.graph.pop(max_id)

    I_result = np.zeros((X, Y))
    I_result = I_result.astype('uint8')

    visit_status = {}
    for i in range(len(prim_r.vertex_list)):
        visit_status[prim_r.vertex_list[i]] = False

    for i in [edge_begin, edge_end]:
        stack = []
        stack.append(i)
        visit_status[i] = True

        if i == edge_begin:
            vertex_colour = 0
        else:
            vertex_colour = 255

        while stack:
            vertex = stack.pop()
            neighbours = prim_r.neighbours(vertex)
            for j in range(len(neighbours)):
                if j in visit_status.keys():
                    if not visit_status[j]:
                        stack.append(j)
                        visit_status[j] = True
                        prim_r.change_colour(j, vertex_colour)

    for i in range(1, X):
        for j in range(1, Y):
            for k in prim_r.vertex_list:
                if k[0] == X * j + i:
                    I_result[i][j] = k[1]

    fig, axs = plt.subplots(1, 2)
    fig.set_size_inches(8, 4)
    axs[0].imshow(I, cmap=plt.get_cmap('gray'))
    axs[0].axis('off')
    axs[0].set_title(f'Obrazek oryginalny')
    axs[1].imshow(I_result, cmap=plt.get_cmap('gray'))
    axs[1].axis('off')
    axs[1].set_title(f'Obrazek po segmentacji')
    plt.show()

    print('HW')

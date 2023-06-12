import pprint
import sys
import cv2
import numpy as np
from matplotlib import pyplot as plt

class Graph:
    def __init__(self):
        self.list = {}
        self.vertexes_tab = []
        self.edges_tab = []
        
    def insert_vertex(self, vertex_id, color=None):
        if vertex_id not in self.list:
            self.list[vertex_id] = []
            self.vertexes_tab.append((vertex_id, color))

    def insert_edge(self, vertex_id1, vertex_id2, cost):
        if vertex_id1 not in self.list:
            self.insert_vertex(vertex_id1)
        if vertex_id2 not in self.list:
            self.insert_vertex(vertex_id2)
        self.list[vertex_id1].append((vertex_id2, cost))
        self.list[vertex_id2].append((vertex_id1, cost))
        self.edges_tab.append((vertex_id1, vertex_id2, cost))
        self.edges_tab.append((vertex_id2, vertex_id1, cost))

    def delete_vertex(self, vertex_id):
        del self.list[vertex_id]
        for i in range(len(self.vertexes_tab)):
            if self.vertexes_tab[i][0] == vertex_id:
                del_id = i
        self.vertexes_tab.pop(del_id)
        for key, value in self.list.items():
            del_list = []
            for i in range(len(self.list[key])):
                if self.list[key][i][0] == vertex_id:
                    del_list.append(i)
            for j in range(len(del_list)):
                self.list[key].pop(del_list[j])
        del_list = []
        for i in range(len(self.edges_tab)):
            if self.edges_tab[i][0] == vertex_id or self.edges_tab[i][1] == vertex_id:
                del_list.append(i)
        for i in reversed(range(0, len(del_list))):
            self.edges_tab.pop(del_list[i])


    def delete_edge(self, vertex_id1, vertex_id2):
        for i in range(len(self.list[vertex_id1])):
            if self.list[vertex_id1][i][0] == vertex_id2:
                del_id = i
        self.list[vertex_id1].pop(del_id)
        for i in range(len(self.list[vertex_id2])):
            if self.list[vertex_id2][i][0] == vertex_id1:
                del_id = i
        self.list[vertex_id2].pop(del_id)
        del_list = []
        for i in range(len(self.edges_tab)):
            if self.edges_tab[i][0] == vertex_id1 and self.edges_tab[i][1] == vertex_id2:
                del_list.append(i)
            if self.edges_tab[i][0] == vertex_id2 and self.edges_tab[i][1] == vertex_id1:
                del_list.append(i)
        for i in reversed(range(0, len(del_list))):
            self.edges_tab.pop(del_list[i])

    def neighbours(self, vertex_id):
        neighbours = []
        for i in range(len(self.list[vertex_id])):
            neighbours.append(self.list[vertex_id][i][0])
        return neighbours

    def order(self):
        return len(self.vertexes_tab)

    def size(self):
        return len(self.edges_tab)

    def edges(self):
        edges = []
        for i in range(len(self.edges_tab)):
            edges.append((self.edges_tab[i][0],self.edges_tab[i][1]))
        return edges

    def weights(self, vertex_id1, vertex_id2):
        for i in range(len(self.edges_tab)):
            if self.edges_tab[i][0] == vertex_id1 and self.edges_tab[i][1] == vertex_id2:
                weight = self.edges_tab[i][2]
        return weight

    def Prim(self, s):
        suma = 0
        A = []
        alfa = {}
        beta = {}
        for u in range(len(self.vertexes_tab)):
            alfa[self.vertexes_tab[u][0]] = 0
            beta[self.vertexes_tab[u][0]] = sys.maxsize
        Q = []
        for u in range(len(self.vertexes_tab)):
            Q.append(self.vertexes_tab[u][0])
        del alfa[s]
        del beta[s]
        Q.remove(s)
        u_star = s
        while Q:
            for u in Q:
                if u in self.neighbours(u_star):
                    if self.weights(u, u_star) < beta[u]:
                        alfa[u] = u_star
                        beta[u] = self.weights(u, u_star)
            min_val = min(beta.values())
            for key in beta:
                if beta[key] == min_val:
                    u_star = key
            Q.remove(u_star)
            A.append((alfa[u_star], u_star))
            suma += self.weights(alfa[u_star], u_star)
            del alfa[u_star]
            del beta[u_star]
        return (A, suma)

    def change_colour(self, vertexid, new_colour):
        id_to_remove = None
        for i in range(len(self.vertexes_tab)):
            if self.vertexes_tab[i][0] == vertexid:
                id_to_remove = i
        self.vertexes_tab.pop(id_to_remove)
        self.vertexes_tab.append((vertexid, new_colour))

    def __str__(self):
        return pprint.pformat(self.list)


def Prim_out_of_class(G, s):
    MST = Graph()
    suma = 0
    alfa = {}
    beta = {}
    for u in range(len(G.vertexes_tab)):
        MST.insert_vertex(G.vertexes_tab[u][0],G.vertexes_tab[u][1])
        alfa[G.vertexes_tab[u][0]] = 0
        beta[G.vertexes_tab[u][0]] = sys.maxsize
    Q = []
    for u in range(len(G.vertexes_tab)):
        Q.append(G.vertexes_tab[u][0])
    del alfa[s]
    del beta[s]
    Q.remove(s)
    u_star = s
    while Q:
        for u in Q:
            if u in G.neighbours(u_star):
                if G.weights(u, u_star) < beta[u]:
                    alfa[u] = u_star
                    beta[u] = G.weights(u, u_star)
        min_val = min(beta.values())
        for key in beta:
            if beta[key] == min_val:
                u_star = key
        Q.remove(u_star)
        MST.insert_edge(alfa[u_star], u_star, G.weights(alfa[u_star], u_star))
        suma += G.weights(alfa[u_star], u_star)
        del alfa[u_star]
        del beta[u_star]
    return MST, suma

if __name__ == "__main__":
    # SEGMENTACJA
    g = Graph()
    I = cv2.imread('sample.png', cv2.IMREAD_GRAYSCALE)
    I = I.astype('float32')
    (X,Y) = I.shape
    for i in range(0, X):
        for j in range(0, Y):
            g.insert_vertex(X*j+i,I[i][j])
    for i in range(0, X):
        for j in range(0, Y):
            if (i+1) < (Y-1):
                g.insert_edge((X*(i+1)+j), X*i+j, abs(I[i+1][j]-I[i][j]))
            if (i+1) < (Y-1) and (j-1) > 0:
                g.insert_edge((X*(i+1)+(j-1)), X*i+j, abs(I[i+1][j-1]-I[i][j]))
            if (i-1) > 0 and (j+1) < (Y-1):
                g.insert_edge((X*(i-1)+(j+1)), X*i+j, abs(I[i-1][j+1]-I[i][j]))
            if (j+1) < (Y-1):
                g.insert_edge((X*i+(j+1)), X*i+j, abs(I[i][j+1]-I[i][j]))
            if (j-1) > 0:
                g.insert_edge((X*i+(j-1)), X*i+j, abs(I[i][j-1]-I[i][j]))
            if (i-1) > 0 and (j-1) > 0:
                g.insert_edge((X*(i-1)+(j-1)), X*i+j, abs(I[i-1][j-1]-I[i][j]))
            if (i-1) > 0:
                g.insert_edge((X*(i-1)+j), X*i+j, abs(I[i-1][j]-I[i][j]))
            if (i+1) < (Y-1) and (j+1) < (Y-1):
                g.insert_edge((X*(i+1)+(j+1)), X*i+j, abs(I[i+1][j+1]-I[i][j]))
    prim_result, prim_cost = Prim_out_of_class(g,99)
    prim_result_edges = prim_result.edges()
    prim_result_edges_costs = []
    for i in prim_result_edges:
        prim_result_edges_costs.append(g.weights(i[0],i[1]))
    max_val = max(prim_result_edges_costs)
    max_id = 0
    for i in range(len(prim_result_edges_costs)):
        if prim_result_edges_costs[i] == max_val:
            max_id = i
    edge_begin = prim_result_edges[max_id][0]
    edge_end = prim_result_edges[max_id][1]
    prim_result.delete_edge(edge_begin, edge_end)
    I_result = np.zeros((X,Y))
    I_result = I_result.astype('uint8')
    visit_status = {}
    for i in range(len(prim_result.vertexes_tab)):
        visit_status[prim_result.vertexes_tab[i][0]] = False
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
            neighbours = prim_result.neighbours(vertex)
            for j in range(len(neighbours)):
                if j in visit_status.keys():
                    if visit_status[j] == False:
                        stack.append(j)
                        visit_status[j] = True
                        prim_result.change_colour(j,vertex_colour)
    for i in range(1,X):
        for j in range(1,Y):
            for k in prim_result.vertexes_tab:
                if k[0] == X*j+i:
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







    


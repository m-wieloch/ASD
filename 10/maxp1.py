import pprint
import sys

class Graph:
    def __init__(self):
        self.list = {}
        self.vertexes_tab = []
        self.edges_tab = []

    def insert_vertex(self, vertex_id, color=None):
        if vertex_id not in self.list:
            self.list[vertex_id] = []
            self.vertexes_tab.append((vertex_id, color))

    def insert_edge(self, vertex_id1, vertex_id2, cost, is_directed):
        if vertex_id1 not in self.list:
            self.insert_vertex(vertex_id1)
        if vertex_id2 not in self.list:
            self.insert_vertex(vertex_id2)
        self.list[vertex_id1].append((vertex_id2, cost))
        self.edges_tab.append((vertex_id1, vertex_id2, cost))
        if is_directed == False:
            self.list[vertex_id2].append((vertex_id1, cost))
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
        weight = 0
        for i in range(len(self.edges_tab)):
            if self.edges_tab[i][0] == vertex_id1 and self.edges_tab[i][1] == vertex_id2:
                weight = self.edges_tab[i][2]
        return weight

    def key_to_num(self, key_for_num):
        key_to_num_dict = {}
        key_id = 0
        for key, value in self.list.items():
            key_to_num_dict[key] = key_id
            key_id += 1
        return key_to_num_dict[key_for_num]

    def num_to_key(self, num_for_key):
        key_to_num_dict = {}
        key_id = 0
        for key, value in self.list.items():
            key_to_num_dict[key_id] = key
            key_id += 1
        return key_to_num_dict[num_for_key]

    def update_edge(self, vertex_id1, vertex_id2, new_capacity):
        del_id = None
        for i in range(len(self.list[vertex_id1])):
            if self.list[vertex_id1][i][0] == vertex_id2:
                del_id = i
        if del_id != None:
            self.list[vertex_id1].pop(del_id)
        del_list = []
        for i in range(len(self.edges_tab)):
            if self.edges_tab[i][0] == vertex_id1 and self.edges_tab[i][1] == vertex_id2:
                del_list.append(i)
        for i in reversed(range(0, len(del_list))):
            self.edges_tab.pop(del_list[i])
        if new_capacity != 0:
            self.list[vertex_id1].append((vertex_id2, new_capacity))
            self.edges_tab.append((vertex_id1, vertex_id2, new_capacity))

    def BFS(self, s, t, alfa):
        visited = []
        for i in range(self.order()):
            visited.append(False)
        queue = [self.key_to_num(s)]
        visited[self.key_to_num(s)] = True
        while queue:
            u = queue.pop(0)
            u_list = self.neighbours(self.num_to_key(u))
            for i in range(len(u_list)):
                v = self.key_to_num(u_list[i])
                if visited[v] == False:
                    queue.append(v)
                    visited[v] = True
                    alfa[v] = u
        if visited[self.key_to_num(t)] == True:
            return True
        else:
            return False

    def FF(self, source, sink):
        parent = []
        for i in range(self.order()):
            parent.append(-1)
        max_flow_value = 0
        while self.BFS(source, sink, parent):
            temp_path_flow = sys.maxsize
            vertex = self.key_to_num(sink)
            while vertex != self.key_to_num(source):
                temp_path_flow = min(temp_path_flow, self.weights(self.num_to_key(parent[vertex]),self.num_to_key(vertex)))
                vertex = parent[vertex]
            max_flow_value += temp_path_flow
            temp = self.key_to_num(sink)
            while temp != self.key_to_num(source):
                u = parent[temp]
                old_capacity_utemp = self.weights(self.num_to_key(u), self.num_to_key(temp))
                self.update_edge(self.num_to_key(u), self.num_to_key(temp), (old_capacity_utemp - temp_path_flow))
                old_capacity_tempu = self.weights(self.num_to_key(temp), self.num_to_key(u))
                self.update_edge(self.num_to_key(temp), self.num_to_key(u), (old_capacity_tempu + temp_path_flow))
                temp = parent[temp]
        return max_flow_value

    def __str__(self):
        return pprint.pformat(self.list)

if __name__ == "__main__":
    graf_0 = [('s', 'u', 2), ('u', 't', 1), ('u', 'v', 3), ('s', 'v', 1), ('v', 't', 2)]
    g0 = Graph()
    for i in range(len(graf_0)):
        g0.insert_edge(graf_0[i][0], graf_0[i][1], graf_0[i][2], True)
    print(f"Maksymalny przepływ dla grafu_0 z upla wynosi {g0.FF('s', 't')}")
    # graf_1 = [('s', 'a', 16), ('s', 'c', 13), ('a', 'c', 10), ('c', 'a', 4), ('a', 'b', 12), ('b', 'c', 9),
    #           ('b', 't', 20), ('c', 'd', 14), ('d', 'b', 7), ('d', 't', 4)]
    # g1 = Graph()
    # for i in range(len(graf_1)):
    #     g1.insert_edge(graf_1[i][0], graf_1[i][1], graf_1[i][2], True)
    # print(f"Maksymalny przepływ dla grafu_1 z upla wynosi {g1.FF('s', 't')}")
    # graf_2 = [('s', 'a', 3), ('s', 'c', 3), ('a', 'b', 4), ('b', 's', 3), ('b', 'c', 1), ('b', 'd', 2), ('c', 'e', 6),
    #           ('c', 'd', 2), ('d', 't', 1), ('e', 't', 9)]
    # g2 = Graph()
    # for i in range(len(graf_2)):
    #     g2.insert_edge(graf_2[i][0], graf_2[i][1], graf_2[i][2], True)
    # print(f"Maksymalny przepływ dla grafu_2 z upla wynosi {g2.FF('s', 't')}")
    # graf_3 = [('s', 'a', 8), ('s', 'd', 3), ('a', 'b', 9), ('b', 'd', 7), ('b', 't', 2), ('c', 't', 5), ('d', 'b', 7),
    #           ('d', 'c', 4)]
    # g3 = Graph()
    # for i in range(len(graf_3)):
    #     g3.insert_edge(graf_3[i][0], graf_3[i][1], graf_3[i][2], True)
    # print(f"Maksymalny przepływ dla grafu_3 z upla wynosi {g3.FF('s','t')}")
#!/usr/bin/python
# CSE6140 HW2
# This is an example of how your experiments should look like.
# Feel free to use and modify the code below, or write your own experimental code, as long as it produces the desired output.
import time
import sys
import os
import numpy as np
from sets import *
from collections import defaultdict


class RunExperiments:

    def __init__(self):
        self.MST = []
        self.mstweight = 0
        self.adjacent = defaultdict(list)
        self.G = {}

    def parse_edges(self, filename):
        # Write this function to parse edges from graph file to create your graph object
        if os.path.exists(filename):
            with open(filename, "r") as file:
                content = file.readlines()
            reader = [np.asarray(x.split(" "), dtype="int") for x in content]
            N = reader[0][0]  # node numbers
            E = reader[0][1]  # edge numbers
            edges = np.asarray(reader[1:], dtype="int")  # edge array
            nodes = np.unique(edges[:, 0:2])  # node array
            self.G = {"nodes": nodes, "edges": edges, "nodes_num": N, "edges_num": E}
            return self.G
        else:
            filename = input("Enter filename: ")
            return self.parse_edges(filename)

    def find_parent(self, parent, node):
        if parent[node] == node:
            return node
        else:
            return self.find_parent(parent, parent[node])

    def computeMST(self, G):
        nodes = G["nodes"]
        edges = G["edges"]
        N = G["nodes_num"]
        E = G["edges_num"]
        # initialization
        rank = np.zeros(N, dtype="int")
        parent = list(range(N))

        # sort the edges in an increasing order
        sedges = edges[edges[:, 2].argsort()]
        for edge in sedges:
            u = self.find_parent(parent, edge[0])
            v = self.find_parent(parent, edge[1])
            if u != v:
                self.MST.append(edge.tolist())
                self.mstweight += edge[2]
                if rank[u] < rank[v]:
                    parent[u] = v
                elif rank[u] > rank[v]:
                    parent[v] = u
                else:
                    parent[v] = u
                    rank[u] += 1
        return self.mstweight

    def _BFS_SP(self, start, goal):
        edge = defaultdict(list)
        for e in self.MST:
            edge[e[0]].append(e[1])
            edge[e[1]].append(e[0])

        marked = np.zeros(self.G["nodes_num"])
        queue = []
        queue.append([start])
        while queue:
            path = queue.pop(0)
            q = path[-1]
            if q == goal:
                break
            elif marked[q] == 0:
                marked[q] = 1
                for next_node in edge[q]:
                    new_path = list(path)
                    new_path.append(next_node)
                    queue.append(new_path)
        sub_MST = []
        for q in range(len(path)-1):
            sub_MST.append((path[q], path[q+1]))
        return sub_MST

    def recomputeMST(self, u, v, weight, G): # Assume u and v are in nodes
        self.G["edges_num"] += 1
        sub_MST = self._BFS_SP(u, v)
        sub_edges = []
        for edge in self.MST:
            if (edge[0], edge[1]) in sub_MST or (edge[1], edge[0]) in sub_MST:
                sub_edges.append(edge)
        m_edge = sub_edges[int(np.argmax(np.asarray(sub_edges)[:, 2]))]
        if weight < m_edge[2]:
            # print(sub_edges)
            # print(self.MST.index(m_edge))
            self.MST.pop(self.MST.index(m_edge))
            self.MST.append([u, v, weight])
            self.mstweight = self.mstweight + weight - m_edge[2]
        return self.mstweight

    def main(self):

        num_args = len(sys.argv)

        if num_args < 4:
            print("error: not enough input arguments")
            exit(1)

        graph_file = sys.argv[1]
        change_file = sys.argv[2]
        output_file = sys.argv[3]

        # Construct graph
        G = self.parse_edges(graph_file)

        start_MST = time.time()  # time in seconds
        # call MST function to return total weight of MST
        MSTweight = self.computeMST(G)
        total_time = (time.time() - start_MST) * \
                     1000  # to convert to milliseconds

        # Write initial MST weight and time to file
        output = open(output_file, 'w')
        output.write(str(MSTweight) + " " + str(total_time) + "\n")

        # Changes file
        with open(change_file, 'r') as changes:
            num_changes = changes.readline()

            for line in changes:
                # parse edge and weight
                edge_data = list(map(lambda x: int(x), line.split()))
                assert (len(edge_data) == 3)

                u, v, weight = edge_data[0], edge_data[1], edge_data[2]

                # call recomputeMST function
                start_recompute = time.time()
                new_weight = self.recomputeMST(u, v, weight, G)
                # to convert to milliseconds
                total_recompute = (time.time() - start_recompute) * 1000

                # write new weight and time to output file
                output.write(str(new_weight) + " " + str(total_recompute) + "\n")


if __name__ == '__main__':
    # run the experiments
    runexp = RunExperiments()
    runexp.main()

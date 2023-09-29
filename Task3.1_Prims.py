"""Task 3.1: Prim's algorithm for displaying the minimum spanning tree"""

# Importing the libraries required
from collections import defaultdict
import heapq
import Task1_Dijkstra as Task1_File
import matplotlib.pyplot as plt
import networkx as nx

# Create object of the class Graph to use loading_data() method, Wood Green and Bank are used only for crating object,
# they don't affect the result of the program.
object1 = Task1_File.Graph('wood green', 'bank')
train_map1 = object1.underground_map


# Prims algorithm
def prims(graph, starting_vertex):
    mst = defaultdict(set)
    visited = {starting_vertex}
    edges = [
        (cost, starting_vertex, to)
        for to, cost in graph[starting_vertex].items()]
    heapq.heapify(edges)
    while edges:
        cost, frm, to = heapq.heappop(edges)
        if to not in visited:
            visited.add(to)
            mst[frm].add(to)
            for to_next, cost in graph[to].items():
                if to_next not in visited:
                    heapq.heappush(edges, (cost, to, to_next))
    return mst


# Plotting map from train_map1 dictionary
def plot_map():
    plt.figure("Task:2(Minimum Spanning tree using Prim's algorithm", figsize=(15, 8))
    G = nx.Graph()
    for node in train_map1:
        G.add_node(node)
        for neighbour in train_map1[node]:
            G.add_edge(node, neighbour)
    nx.draw(G, with_labels=True, node_size=4, node_color='blue', width=0.5, font_size=6, font_family='sans-serif')
    plt.show()


if __name__ == '__main__':
    a = prims(train_map1, 'WOOD GREEN')
    plot_map()

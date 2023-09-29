"""Task 1: Finding the shortest path between two stations using Dijkstra's algorithm"""

# Importing the libraries required
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx



class Graph:
    def __init__(self, start, end):
        self.between = None
        self.final_list = None
        self.shortest_path = None
        self.st_a = None
        self.st_b = None
        self.minutes = None
        self.costs = None
        self.start = start.upper()
        self.end = end.upper()
        self.underground_map = {}
        self.loading_data()
        self.dijkstra()



    def loading_data(self):
        # global line
        underground_df = pd.read_excel('Stations_Data.xlsx')
        underground_df.columns = ['Line', 'Station from (A)', 'Station from (B)', 'Time Between Stations (Minutes)']
        underground_df = underground_df.dropna()
        underground_df = underground_df.reset_index(drop=True)

        # Read Stations_data.xlsx drop fist column and first row
        histogram_df = pd.read_excel('Stations_Data.xlsx')
        histogram_df = histogram_df.dropna()
        histogram_df = histogram_df.reset_index(drop=True)
        histogram_df = histogram_df.drop(columns=histogram_df.columns[0])
        self.st_b = histogram_df['Station to (B)']
        self.st_a = histogram_df['Station from (A)']
        self.minutes = histogram_df['Time Between Stations (Minutes)']

        # Combine st_b and st_a to display them in st_a-axis
        self.st_b = self.st_b.tolist()
        self.st_a = self.st_a.tolist()
        self.st_a = [self.st_a[i] + ' -> ' + self.st_b[i] for i in range(len(self.st_a))]

        # Dictionary with station_a as key and station_b as value and time as value
        for i in range(0, len(underground_df)):
            station_a = underground_df.loc[i, 'Station from (A)']
            station_b = underground_df.loc[i, 'Station from (B)']
            time = underground_df.loc[i, 'Time Between Stations (Minutes)']
            if station_a not in self.underground_map.keys():
                self.underground_map[station_a] = {}
            if station_b not in self.underground_map.keys():
                self.underground_map[station_b] = {}
            self.underground_map[station_a][station_b] = time
            self.underground_map[station_b][station_a] = time
        return self.underground_map

    def node_lowest_cost(self, costs, processed):
        # Go through each node.
        # If it's the lowest cost so far and hasn't been processed yet, set it as new lowest-cost node.
        lowest_cost = float('inf')
        lowest_cost_node = None
        for node in costs:
            cost = costs[node]
            if cost < lowest_cost and node not in processed:
                lowest_cost = cost
                lowest_cost_node = node
        return lowest_cost_node

    def dijkstra(self):
        # Finding the shortest route between the two stations
        # 1. Finding the lowest cost node that you haven't processed yet.
        # 2. Updating the costs for its neighbors
        # 3. Repeating until you've done this for every node in the graph.
        # 4. Calculating the final_path.

        # The cost to reach each node
        self.costs = {}
        # The parents of each node
        parents = {}
        # Keep track of the nodes that have already been processed
        processed = []
        # The node we're currently processing
        # the start point
        node = self.start

        # Initialize the costs to infinity and the parents to None
        for station in self.underground_map.keys():
            self.costs[station] = float('inf')
            parents[station] = None

        # The cost to reach the start node is 0
        self.costs[self.start] = 0

        # Find the lowest cost node that you haven't processed yet
        while node is not None:
            cost = self.costs[node]
            neighbors = self.underground_map[node]
            # Go through all the neighbors of this node
            for n in neighbors.keys():
                new_cost = cost + neighbors[n]
                # If it's cheaper to get to this neighbor by going through this node...
                if self.costs[n] > new_cost:
                    # ... update the cost for this node
                    self.costs[n] = new_cost
                    # This node becomes the new parent for this neighbor
                    parents[n] = node
            # Mark the node as processed
            processed.append(node)
            # Find the next node to process, and loop
            node = self.node_lowest_cost(self.costs, processed)

        # At this point, all the costs have been calculated
        # Find the shortest path from the end to the start
        # by following the parents
        node = self.end
        self.shortest_path = [self.end]

        while parents[node] is not self.start:
            self.shortest_path.append(parents[node])
            node = parents[node]

        self.shortest_path.append(self.start)
        self.shortest_path.reverse()

        # List storing the minutes between each station of the route
        self.between = []
        for i in range(len(self.shortest_path) - 1):
            self.between.append(self.underground_map[self.shortest_path[i]][self.shortest_path[i + 1]])

        # Using list comprehension to create final_list with the pairs of stations
        first_list = [x + '->' + y for x, y in zip(self.shortest_path[0::2], self.shortest_path[1::2])]
        second_list = [x + '->' + y for x, y in zip(self.shortest_path[1::2], self.shortest_path[2::2])]
        self.final_list = []
        biggestList = len(first_list) if len(first_list) > len(second_list) else len(second_list)
        for i in range(biggestList):
            if i < len(first_list):
                self.final_list.append(first_list[i])
            if i < len(second_list):
                self.final_list.append(second_list[i])

    # Plot histogram for all station times
    def total_histogram(self):
        plt.rcParams['font.size'] = 12
        plt.figure('Task:1(B) Histogram for all pairs', figsize=(15, 8))
        plt.margins(x=0.01)
        plt.title('Journey times between each pair of stations')
        plt.xlabel('Pairs of Stations')
        plt.ylabel('Time Between Stations (Minutes)')
        plt.bar(self.st_a, self.minutes)
        plt.xticks([])
        plt.show()

    # Plot bar chart for times between pairs of stations
    def bar_chart_route(self):
        plt.figure('Route Histogram-Extra', figsize=(15, 8))
        plt.rcParams['font.size'] = 8
        plt.bar(self.final_list, self.between)
        plt.title('Time between stations')
        plt.xlabel('Stations')
        plt.ylabel('Time (Minutes)')
        plt.xticks(rotation=15, ha='right')
        plt.show()

    # Plot directed graph for shortest_path
    def plot_dgraph_route(self):
        plt.figure('Task:1(Directed Graph)', figsize=(15, 8))
        G = nx.DiGraph()
        G.add_nodes_from(self.shortest_path)
        G.add_edges_from(zip(self.shortest_path, self.shortest_path[1:]))
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color='grey')
        nx.draw_networkx_edges(G, pos, width=2, edge_color='b', arrowsize=30)
        nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
        plt.title('Shortest Path Graph')
        plt.axis('off')
        plt.show()

    # Function to print all data:
    def print_data(self):
        print('Shortest path: {}'.format(' -> '.join(self.shortest_path)))
        for i in range(len(self.shortest_path) - 1):
            print('Time between {} and {} is {} minutes'.format(self.shortest_path[i], self.shortest_path[i + 1],
                                                                self.underground_map[self.shortest_path[i]][
                                                                    self.shortest_path[i + 1]]))
        print('Total number of stations: {}'.format(len(self.shortest_path)))
        print('Total time: {} minutes'.format(self.costs[self.end]))


# Creating object of class Graph
if __name__ == '__main__':
    print('---> Route planner using Dijkstra\'s algorithm <---')
    first_object = Graph(input('Enter Starting Station(A): '), input('Enter Ending Station(B): '))
    if first_object.start not in first_object.underground_map.keys():
        print('Invalid starting station')
    elif first_object.end not in first_object.underground_map.keys():
        print('Invalid ending station')
    else:
        first_object.print_data()
    a = input('Do you want to see the histogram/bar chart for all pairs? (y/n): ')
    if a == 'y':
        first_object.total_histogram()
    b = input('Do you want to see the histogram/bar chart for pairs in the route? (y/n): ')
    if b == 'y':
        first_object.bar_chart_route()
    c = input('Do you want to see the directed graph for the route? (y/n): ')
    if c == 'y':
        first_object.plot_dgraph_route()



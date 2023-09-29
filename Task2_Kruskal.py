"""Task 2: Displaying immediate neighbour that can be closed in line"""

# importing the libraries required
import pandas as pd
from pathlib import Path
from Task1_Dijkstra import Graph


# class to run the program
class Close_stations:
    def __init__(self):
        self.run()

    def run(self):
        lines = ["Bakerloo", "Central", "Jubilee", "Circle", "District", "Piccadilly", "Hammersmith & City",
                 "Metropolitan",
                 "Northern", "Victoria", "Waterloo & City"]
        for line in lines:
            ImmediateNeighbourCLoser(line)


# class where kruskal algorithm is used and comparison is performed to find line between immediate stations that can
# be closed.
class ImmediateNeighbourCLoser:
    def __init__(self, line):
        #store data
        self.new_underground_map = {}
        self.line = line

        # for edge
        self.graph = []
        # storing all data from stations with time
        self.underground_map = {}

        # data structure used to store data
        self.parent = dict()
        self.position = dict()
        self.minimumweight = {}
        self.neighbour_dict = {}
        self.closing_pair = {}

        # method to performs various task required
        self.load_data()
        self.Kruskal_Immediate_neighbour()
        self.possible_closing_station()

    # function to extract file from excel and store it in dictionary
    def load_data(self):
        underground_file = Path('.').absolute()
        underground_file = str(underground_file.joinpath('Stations_Data.xlsx'))
        Main_underground_data = pd.read_excel(underground_file)
        Main_underground_data.columns = ['Line', 'Station from (A)', 'Station to (B)',
                                         'Time Between Stations (Minutes)']
        underground_data = Main_underground_data[Main_underground_data["Line"] == self.line]
        underground_data = underground_data.dropna()
        underground_data = underground_data.reset_index(drop=True)

        # running loop to extract the data from the Excel file
        for data in range(0, len(underground_data)):
            # line = underground_data.loc[data, 'Line']
            station_a = underground_data.loc[data, 'Station from (A)']
            station_b = underground_data.loc[data, 'Station to (B)']
            t = underground_data.loc[data, 'Time Between Stations (Minutes)']

            if station_a not in self.underground_map.keys():
                self.underground_map[station_a] = {}
            if station_b not in self.underground_map.keys():
                self.underground_map[station_b] = {}

            self.underground_map[station_a][station_b] = t
            self.underground_map[station_b][station_a] = t

        train_df = Main_underground_data[Main_underground_data["Line"] != self.line]

        for i in range(0, len(train_df)):
            station_a = underground_data.loc[data, 'Station from (A)']
            station_b = underground_data.loc[data, 'Station to (B)']
            t = underground_data.loc[data, 'Time Between Stations (Minutes)']

            if station_a not in self.new_underground_map.keys():
                self.new_underground_map[station_a] = {}
            if station_b not in self.new_underground_map.keys():
                self.new_underground_map[station_b] = {}

            self.new_underground_map[station_a][station_b] = t
            self.new_underground_map[station_b][station_a] = t

        # adding item in edge
        for src, values in self.underground_map.items():
            for des, t in values.items():
                self.add_edge(src, des, t)

    # function for adding edges
    def add_edge(self, src, des, t):
        self.graph.append([src, des, t])

    # function to make set
    def make_set(self, ver):
        self.parent[ver] = ver
        self.position[ver] = 0

    # A utility function to find set of an element i
    def find(self, val):
        if self.parent[val] != val:
            # Reassignment of node's parent to root node as
            # path compression requires
            self.parent[val] = self.find(self.parent[val])

        return self.parent[val]

    # A function that does union of two sets of x and y
    # (uses union by rank)
    def union(self, a, b):
        # Attach smaller rank tree under root of
        # high rank tree (Union by Rank)
        if self.position[a] < self.position[b]:
            self.parent[a] = b
        elif self.position[a] > self.position[b]:
            self.parent[b] = a

        # If ranks are same, then make one as root and increment its rank by one
        else:
            self.parent[b] = a
            self.position[a] += 1

    # function to find immediate neighbour
    def Kruskal_Immediate_neighbour(self):
        output = []  # place to store value

        # Step 1: Sort all the edges in
        # non-decreasing order of their
        # weight. If we are not allowed to change the
        # given graph, we can create a copy of graph
        # step 2 : managing the clustering

        # sorting the data and storing it in self.graph
        self.graph = sorted(self.graph, key=lambda item: item[2])

        # calling the function self.make_set
        for ver in self.underground_map.keys():
            self.make_set(ver)

        # finding the element
        for container in self.graph:
            src, des, t = container
            a = self.find(src)
            b = self.find(des)
            if a != b:
                output.append([src, des, t])
                self.union(a, b)

        minimumCost = 0
        for stn_a, stn_b, time in output:
            minimumCost += time
            # storing the value in dictionary named self.neighbour
            self.neighbour_dict[stn_a] = {stn_b: time}

    # function  to print the suggested close station per line::::
    def possible_closing_station(self):
        for station_A, station_B_dict in self.neighbour_dict.items():
            for station_B, time in station_B_dict.items():
                # making comparison to show the final output
                # this comparison check whether the given algorithm is present or not in other tine lines
                if station_A in self.new_underground_map.keys() and station_B in self.new_underground_map.keys():
                    self.closing_pair[station_A] = station_B

                    # ** Code to find time taken between the pair statin after shown down
                    # Graph(self.new_underground_map, station_A, station_B)

        print(f"* The pair of station that can be closed on {self.line} are:")
        for stnA, stnB in (self.closing_pair.items()):
            print("~", stnA, ">>>>", stnB)
        print("")


Close_stations()

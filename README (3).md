
# London Underground Path Finder & Analysis

This project provides tools and scripts to analyze and determine optimal paths within the London Underground system. It incorporates several algorithms and data visualization techniques.

## Features:

1. **Shortest Path Finder (Dijkstra's Algorithm)**: Find the shortest path between two stations using Dijkstra's algorithm.
2. **Histogram Generator**: Visualize station data using histograms.
3. **Closable Stations Analysis (Kruskal's Algorithm)**: Identify the immediate neighbor that can be closed in a line.
4. **Minimum Spanning Tree (Prim's Algorithm)**: Display the minimum spanning tree of the London Underground system.
5. **Real-time TFL Service CLI**: A command-line interface that displays real-time TFL service data.

## Dependencies:

To run the scripts, you will need the following Python packages:
```
certifi==2022.9.24
charset-normalizer==2.1.1
contourpy==1.0.6
...
(xmltodict~=0.13.0)
(termcolor~=2.1.1)
```
(Note: Refer to `requirements.txt` for the complete list.)

## Usage:

To execute a specific task, run the corresponding Python script:
```
python Task1_Dijkstra.py
python Task2 (histogram).py
...
```

## Data:

The project uses data from the following Excel files:
- `Closure_record.xlsx`: Contains data related to station closures.
- `Stations_Data.xlsx`: Contains data about different stations.

## License:

This project is licensed under the MIT License. (Refer to `LICENSE` for more details.)

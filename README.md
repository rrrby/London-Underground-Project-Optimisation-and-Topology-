# London Underground Routing Engine 

An object-oriented Python application designed to calculate the absolute shortest travel time between any two stations in the London Underground network. This project implements a robust Graph Data Structure and an optimized Dijkstra's Algorithm, specifically handling the complexities of multi-line stations and transfer penalties.

## Key Features

* **Optimised Pathfinding:** Utilizes Dijkstra's algorithm implemented with a Priority Queue (`heapq`) to achieve $O((V+E)\log V)$ time complexity, ensuring instantaneous routing across the entire network.
* **Realistic Transfer Modeling:** Accurately accounts for line-change penalties. The graph topology splits multi-line stations (e.g., Victoria) into distinct nodes connected by weighted transfer edges, avoiding hardcoded penalties within the traversal algorithm itself.
* **Resilient Tie-breaking:** Features a custom `__lt__` magic method within the `Station` class to handle distance-tie scenarios in the priority queue, preventing `TypeError` exceptions during graph traversal.
* **Defensive Architecture:** Employs strict encapsulation (protecting adjacency lists) and custom exception handling (`StationNotFoundError`) to gracefully manage invalid commuter data without system failure.
* **Dynamic Network Disruption Analysis:** Includes functionality to simulate station closures (dynamically loaded from external files) and recalculate the network-wide average commuter delay, demonstrating the system's analytical capabilities.

## Architecture & Data Structures

The system is built on a highly decoupled Object-Oriented architecture:

1.  **Bottom Layer (Graph Primitives):** `Vertex`, `Edge`, `Network`, and `SymmetricNetwork` classes establish the foundational graph theory structures using sets for unique nodes and dictionaries ($O(1)$ lookups) for adjacency lists.
2.  **Domain Layer (Tube Map):** The `Station` and `TubeNetwork` classes inherit from the primitives, adding London Underground-specific logic, including node registry based on `(station_id, line)` keys to correctly instantiate multi-line hubs.
3.  **Application Layer (Routing):** The `Commuter` class acts as the interface, taking a start and end station, handling multi-node matching, and requesting the shortest path from the network object.

## Project Structure

```text
├── London Underground.ipynb # Execution script combining data parsing and routing
├── network_utils.py      # Core Graph & Dijkstra implementation
├── tube_utils.py         # (Given)TubeNetwork, Station, and Commuter domain classes
├── commuters.csv         # Sample dataset containing commuter journeys
├── stations.csv          # Edges/connections defining the Tube map topology
├── UG_xxx.csv            # Vertices/stations metadata
├── station_closed.txt    # Dynamic input file for simulating network disruptions


└── README.md             # Project documentation
```

## How to Run
1. Clone this repository:
```bash
git clone https://github.com/rrrby/London-Underground-Project-Optimisation-and-Topology-.git
```
2. Ensure you have Python 3.7+ installed. No external dependencies (like Pandas or NetworkX) are required; the engine is built entirely using standard Python libraries to maximize performance and portability.

3. Run the main script (or open the provided Jupyter Notebook if applicable) to parse the CSVs, build the graph, and simulate the commuter journeys.

## Future Extensions
The system's loose coupling facilitates easy extensions. For example, to implement variable walking speeds for individual commuters, a speed_factor attribute can be added to the Commuter object and passed into the routing function to dynamically scale transfer edge weights, all without altering the underlying graph topology.

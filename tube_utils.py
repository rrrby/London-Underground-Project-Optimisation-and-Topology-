from network_utils import Edge
from network_utils import Vertex
from network_utils import SymmetricNetwork
from heapq import heapify, heappop, heappush

# ==========================================
# Part 1: Station classified by name and line
# ==========================================
class Station(Vertex):
    """
    Represents a station in the London Underground network.
    
    This class inherits from the Vertex class. It treats the same physical 
    station on different lines as distinct vertices (e.g., Oxford Circus 
    on the Bakerloo line is a different Station object than Oxford Circus 
    on the Central line).

    Args:
        vertex_id (int or str): The unique identifier for the vertex.
        name (str): The physical name of the station (e.g., 'Oxford Circus').
        line (str): The specific underground line the station is on (e.g., 'Bakerloo').
    
    Attributes:
        name (str): The physical name of the station.
        line (str): The line the station is on.
    """
    def __init__(self, vertex_id, name, line):
        super().__init__(vertex_id)
        self.name = name
        self.line = line
        
    def __lt__(self, other: 'Station') -> bool:
        """
        Tie-breaker for priority queue (heapq). 
        When distances are equal, compares stations by their unique ID.
        """
        return self._id < other._id

# ==========================================
# Part 2: TubeNetwork Class and Shortest Distance
# ==========================================

class TubeNetwork(SymmetricNetwork):
    """
    Represents the London Underground tube network.
    
    Inherits from SymmetricNetwork to allow bidirectional travel between stations.
    """
    
    def add_connection(self, station_1, station_2, time):
        """
        Adds a bidirectional connection between two stations in the network.
        
        If the stations are not already in the network, they will be added.
        
        Args:
            station_1 (Station): The first station.
            station_2 (Station): The second station.
            time (float): The travel time between the two stations.
        """
        edge_obj = Edge(time)
        
        if station_1 not in self._vertices: #check whether stations are in the Network(vertices) already
            self.add_vertex(station_1)
        if station_2 not in self._vertices:
            self.add_vertex(station_2)
       
        self.add_edge(station_1, station_2, edge_obj) #Add edge



            
#Shortest Distance
#Use Dijkstra algorithm
#Reference: https://www.datacamp.com/tutorial/dijkstra-algorithm-in-python
    
    def shortest_distances(self, start_vertex):
        """
        Calculates the shortest distances from a start vertex to all other vertices.
        
        Uses an optimized Dijkstra's algorithm implemented with a priority queue (heapq)
        for O((V+E) log V) time complexity, which is the industry standard for graph traversal.
        
        Args:
            start_vertex (Station): The starting node in the network.
            
        Returns:
            dict: A dictionary mapping each vertex to its shortest distance (float) 
                  from the start_vertex.
        """
        # 1. Initialise the distance with infinity
        distances = {v: float("inf") for v in self._vertices}
        distances[start_vertex] = 0 
        
        # 2. Initialise Priority Queue
        # Begin with (distance, vertex)
        pq = [(0, start_vertex)] 
        
        # 3. Initialise with a set, in case it loops forever.
        visited = set()
        
        while pq:
            # Use heappop to get the automatic shortest distance
            current_distance, current_vertex = heappop(pq)

            #Skip if already visites
            if current_vertex in visited:
                continue 
            
            #If not visited, adding a new vertex
            visited.add(current_vertex)
            
            # Visit all neighbours of the vertex
            for neighbour, edge_obj in self._adjacencies[current_vertex]:
                if neighbour in visited:
                    continue
                    
                weight = float(edge_obj._length)
                new_distance = current_distance + weight
                
                #If there are nearer route, get the nearer one.
                if new_distance < distances[neighbour]:
                    distances[neighbour] = new_distance
                    # heappush will help to organise the queue
                    heappush(pq, (new_distance, neighbour))
                    
        return distances

#Check StationNotFoundError for part 3 and shortest distance for part 2
    def shortest_time(self, start_station, end_station):
        '''
    Get the shortest time from start_station to end_station
    
    Parameters
    ----------
    start_station: str
        start_station ID
    end_station: str
        end_station ID

    Returns
    -------
    integer
        the shortest time from the start_station to the end_station
    '''
        if start_station not in self._vertices:
            raise StationNotFoundError(f"{start_station} not found.")
        if end_station not in self._vertices:
            raise StationNotFoundError(f"{end_station} not found.")
        distances = self.shortest_distances(start_station) 
        return distances[end_station]  #Get the end_station from the start_station dictionary: {[vertex_A, 0], [vertex_B, 1], [vertex_C,3]}, and further get the shortest_time


# ==========================================
# Part 3: Commuter Class and Error Definition
# ==========================================

class StationNotFoundError(Exception):
    """
    Exception raised when a requested station ID is not present in the network.
    """
    pass


class Commuter:
    """
    Represents a commuter travelling between a starting station and an ending station.
    
    The class automatically handles cases where the starting or ending physical 
    stations exist on multiple lines by calculating the absolute shortest route 
    across all possible combinations.
    """
    def __init__(self, start_station_ID, end_station_ID, tube_network):
        self.start_station_ID = start_station_ID
        self.end_station_ID = end_station_ID
        self.travel_time = None
        
        # When created, automatically calculate and store the time
        self.update_travel_time(tube_network)

    def update_travel_time(self, tube_network):
        """
        Updates the stored travel time by finding the shortest path across 
        all possible lines the start and end stations might belong to.
        
        Args:
            tube_network (TubeNetwork): The transportation network to calculate routes on.
            
        Raises:
            StationNotFoundError: If either the start or end station is missing.
        """
        # 1. In the Network, find all the connections to this start station
        start_nodes = [v for v in tube_network._vertices if v.name == self.start_station_ID]
        
        # 2. In the Network, find all the connections to this end station
        end_nodes = [v for v in tube_network._vertices if v.name == self.end_station_ID]
        
        # 3. If cannot find it, raise Error
        if not start_nodes:
            raise StationNotFoundError(f"Start station '{self.start_station_ID}' is missing from the network.")
        if not end_nodes:
            raise StationNotFoundError(f"End station '{self.end_station_ID}' is missing from the network.")
            
        # 4. Calculate the shortest time
        min_time = float("inf")
        
        for start_node in start_nodes:
            # Get a dictionary of the distances from one station such as Victoria Station, Line A to all the 
            distances = tube_network.shortest_distances(start_node)
            
            for end_node in end_nodes:
                # Keep checking in the dictionary to update the shortest time
                if distances[end_node] < min_time:
                    min_time = distances[end_node]
                    
        self.travel_time = min_time

    def get_travel_time(self):
        """
        Returns the stored time taken for the shortest route.
        """
        return self.travel_time

        




        

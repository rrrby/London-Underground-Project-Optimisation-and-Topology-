class Edge:
    def __init__(self, length):
        self._length = length

class Vertex:
    def __init__(self, vertex_id):
        self._id = vertex_id

class Network:
    def __init__(self):
        self._vertices = set()
        self._adjacencies = dict()
        
    def add_vertex(self, vertex):
        self._vertices.add(vertex)
        self._adjacencies[vertex] = []
        
    def add_edge(self, vertex_1, vertex_2, edge):
        self._adjacencies[vertex_1].append((vertex_2, edge))

    def remove_edge(self, vertex_1, vertex_2):
        if vertex_1 not in self._adjacencies:
            return
        self._adjacencies[vertex_1] = [
            (v, e) for (v, e) in self._adjacencies[vertex_1] if v != vertex_2
        ]
        
class SymmetricNetwork(Network):
    def add_edge(self, vertex_1, vertex_2, edge):
        super().add_edge(vertex_1, vertex_2, edge)
        super().add_edge(vertex_2, vertex_1, edge)

    def remove_edge(self, vertex_1, vertex_2):
        super().remove_edge(vertex_1, vertex_2)
        super().remove_edge(vertex_2, vertex_1)
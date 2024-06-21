import functools
import math

class Edge():
    length : str = None
    vertex = None

    def __init__(self, vertex):
        self.length = length
        self.edges = edges

class OVertex:
    name : str = None
    visited : bool = False
    previous_vertex = None
    shortest_length_to : int = math.inf
    edges : list[Edge] = None

    def __init__(self, name: str):
        self.name = name



def compare_vertices_by_degree(vertex1: OVertex, vertex2: OVertex) -> int:
    return -1 if vertex1.shortest_length_to < vertex2.shortest_length_to else 1

def compare_edges_by_length(edge1: Edge, edge2: Edge) -> int:
    return -1 if edge1.length < edge2.length else 1

class Graph():
    oriented = True
    vertices_names : list[str] = None
    representation : list[bool] = None
    vertices : list[OVertex] = None
    non_visited : list[OVertex] = None
    visited : list[OVertex] = None
    visited : list[OVertex] = None
    source_name : str = None
    
    

    def __init__(self, vertices_names: list[str], representation: list[int], source_name: str):
        self.vertices_names = vertices_names
        self.representation = representation
        self.source_name = source_name
        self.check_data()
        self.source = self.get_source()
        self.non_visited : list[OVertex] = [source]
        self.visited = []

    def run(self):
        self.order_non_visited_by_degree()
        for current_vertex in self.non_visited:
            current_vertex.edges = sorted(current_vertex.edges, key=functools.cmp_to_key(compare_edges_by_length))
            current_vertex.visited = True
            for edge in current_vertex.edges:
                if edge.length+current_vertex.shortest_length_to < edge.vertex.shortest_length_to:
                    # replacement of the soure and the length
                    edge.vertex.shortest_length_to = current_vertex.shortest_length_to+edge.length
                    edge.vertex.previous_vertex = current_vertex
                
                if not edge.vertex.visited:
                    self.non_visited.append(edge.vertex)
                
            self.visited.append(self.non_visited.pop(0))
            self.order_non_visited_by_degree()
                


    def order_non_visited_by_degree(self):
        self.vertices = sorted(self.vertices, key=functools.cmp_to_key(compare_vertices_by_degree))
                

    def get_source(self) -> OVertex:
        for vertex in self.vertices:
            if vertex.name == self.source_name:
                return vertex
        raise Exception(f'Source : {self.source_name} not found')

        
    def check_data(self):
        vertices_count = len(self.vertices_names)
        if len(self.representation) != vertices_count:
            raise Exception(f'len(self.representation : {len(self.representation)}) != vertices_count : {vertices_count}')
        for row in self.representation:
            if len(row) != vertices_count:
                raise Exception(f'len(row : {len(self.representation)}) != vertices_count : {vertices_count}')
            # TODO : check if the graph representation is unidirectionally oriented 


        
        

class Dikstra:
    def __init__(self):
        pass
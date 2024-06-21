import functools
import math

class Edge():
    length : str = None
    vertex = None

    def __init__(self, vertex, length):
        self.vertex = vertex
        self.length = length

class OVertex:
    name : str = None
    visited : bool = False
    previous_vertex = None
    shortest_length_to : int = math.inf
    edges : list[Edge] = None

    def __init__(self, name: str):
        self.name = name



def compare_vertices_by_degree(vertex1: OVertex, vertex2: OVertex) -> int:
    # print(f'comparing {vertex1.name} {vertex1.shortest_length_to} - {vertex2.name} {vertex2.shortest_length_to}')
    return -1 if vertex1.shortest_length_to < vertex2.shortest_length_to else 1

def compare_edges_by_length(edge1: Edge, edge2: Edge) -> int:
    # print(f'comparing {edge1.vertex.name} {edge1.length} - {edge2.vertex.name} {edge2.length}')
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
        self.vertices = self.create_vertices()
        self.source = self.get_source()
        self.source.shortest_length_to = 0
        self.non_visited : list[OVertex] = [self.source]
        self.visited = []

    def run(self):
        current_vertex = self.non_visited[0]
        self.do(current_vertex)

    def do(self, current_vertex):
        # print(f'current vertex {current_vertex.name} {current_vertex.shortest_length_to}' , [f'{s.name} {s.shortest_length_to}' for s in self.non_visited])
        current_vertex.edges = sorted(current_vertex.edges, key=functools.cmp_to_key(compare_edges_by_length))
        current_vertex.visited = True
        for edge in current_vertex.edges:
            if edge.length+current_vertex.shortest_length_to < edge.vertex.shortest_length_to:
                # replacement of the soure and the length
                edge.vertex.shortest_length_to = current_vertex.shortest_length_to+edge.length
                edge.vertex.previous_vertex = current_vertex
            
            if not edge.vertex.visited:
                self.non_visited.append(edge.vertex)
            
        self.visited.append(self.non_visited.pop(self.non_visited.index(current_vertex)))
        self.order_non_visited_by_degree()
        if len(self.non_visited)>0:
            self.do(self.non_visited[0])


    def order_non_visited_by_degree(self):
        new_non_visited = sorted(self.non_visited, key=functools.cmp_to_key(compare_vertices_by_degree))
        # for element in self.non_visited:
        #     self.non_visited.pop()
        
        # for element in new_non_visited:
        #     self.non_visited.append(element)
                

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

    def create_vertices(self) -> list[OVertex]:
        vertices = []
        for vertex_name in self.vertices_names:
            vertex = OVertex(vertex_name)
            vertices.append(vertex)
        y = 0
        size = len(self.vertices_names)
        while y < size:
            vertex = vertices[y]
            if vertex.edges == None:
                vertex.edges = []
            x = 0
            while x < size:
                edge_vertex = vertices[x]
                if x != y and self.representation[y][x] > 0:
                    edge = Edge(edge_vertex, self.representation[y][x])
                    vertex.edges.append(edge)
                x+=1
            y+=1        
        return vertices
        
        

class Dikstra:
    def __init__(self):
        pass
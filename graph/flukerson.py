from enum import Enum
class Direction(Enum):
    NORMAL = 'normal'
    REVERSED = 'reversed'

class FEdge():
    vertex = None
    flow : float = 0
    capacity : float = 0
    direction : Direction = None 

    def __init__(self, vertex, flow : float, capacity : float, direction: Direction):
        self.vertex = vertex
        self.flow = flow
        self.capacity = capacity
        self.direction = direction

class VertexStatus(Enum):
    POSITIVE = '+'
    NEGATIVE = '-'
    SATURATED = 'SATURATED'
    UNVISITED = 'UNVISITED'

class FVertex:
    name : str = None
    status : VertexStatus = VertexStatus.UNVISITED
    previous_vertex = None
    capacity : int = 0
    edges : list[FEdge] = None

    def __init__(self, name: str):
        self.name = name

class FGraph():
    oriented = True
    vertices_names : list[str] = None
    representation : list[bool] = None
    vertices : list[FVertex] = None
    non_visited : list[FVertex] = None
    visited : list[FVertex] = None
    visited : list[FVertex] = None
    source_name : str = None
    well_name : str = None
    
    

    def __init__(self, vertices_names: list[str], representation: list[int], source_name: str, well_name: str):
        self.vertices_names = vertices_names
        self.representation = representation
        self.get_flow_and_capacity()
        self.source_name = source_name
        self.well_name = well_name
        self.check_data()
        self.vertices = self.create_vertices()
        self.flow_array = None
        self.capacity_array = None
        # self.source = self.get_source()
        # self.source.shortest_length_to = 0
        # self.non_visited : list[FVertex] = [self.source]
        # self.visited = []

    def create_vertices(self) -> list[FVertex]:
        vertices = []
        for vertex_name in self.vertices_names:
            vertex = FVertex(vertex_name)
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
                if x != y and self.capacity_array[y][x] > 0:
                    edge = FEdge(edge_vertex, self.flow_array[y][x], self.capacity_array[y][x], Direction.NORMAL)
                    vertex.edges.append(edge)
                    if vertex not in [e.vertex for e in edge.vertex.edges]:
                        reverse_edge = FEdge(vertex, self.flow_array[y][x], self.capacity_array[y][x], Direction.REVERSED)
                        edge_vertex.edges.append(reverse_edge)
                x+=1
            y+=1        
        return vertices

    def get_flow_and_capacity(self):
        self.capacity_array = []     
        self.flow_array = []     
        for row in self.representation:
            capacity_row = []
            flow_row = []
            for element_str in row:
                splitted = element_str.split('/')
                capacity_row.append(float(splitted[0]))
                capacity_row.append(float(splitted[1]))
            self.capacity_array.append(capacity_row)
            self.flow_array.append(flow_row)
                
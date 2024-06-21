import functools

class Vertex:
    name : str = None
    edges = None
    color :  str = None

    def __init__(self, name: str, edges):
    # def __init__(self, name: str, edges: list[Vertex]):
        self.name = name        
        self.edges = edges

    def get_degree(self):
        return len(self.edges) if self.edges != None else 0

    def add_edge(self, edge):
        if self.edges == None:
            self.edges = []
        if edge.name == self.name:
            raise Exception(f'self appeding into edges for vertex : {self.name}')
        self.edges.append(edge)

def compare_vertices(vertex1: Vertex, vertex2: Vertex) -> int:
    return -1 if vertex1.name < vertex2.name else 1

class NonOrientedGraph:
    vertices_names : list[str] = None
    representation : list[bool] = None
    vertices : list[Vertex] = None
    oriented : bool = False


    def __init__(self, vertices_names: list[str], representation: list[int]):
        self.vertices_names = vertices_names
        self.representation = representation
        self.check_data()
        self.vertices = self.create_vertices()

    def color_graph(self):
        self.sort_vertices_by_degree()
        current_color_id = 1
        for vertex in self.vertices:
            if vertex.color != None:
                continue
            vertex.color = f'C-{current_color_id}'
            non_adjacent_vertices = self.get_non_adjacent_vertices(vertex)
            for edge in non_adjacent_vertices:
                edge.color = vertex.color
            current_color_id+=1

    def create_vertices(self) -> list[Vertex]:
        vertices = []
        for vertex_name in self.vertices_names:
            vertex = Vertex(vertex_name, [])
            vertices.append(vertex)
        y = 0
        size = len(self.vertices_names)
        while y < size:
            vertex = vertices[y]
            x = 0
            while x < size:
                edge = vertices[x]
                if x != y and self.representation[y][x] == 1:
                    if edge not in vertex.edges:
                        vertex.add_edge(edge)
                    if not self.oriented and vertex not in edge.edges:
                        edge.add_edge(vertex)
                x+=1
            y+=1        
        return vertices

    def sort_vertices_by_degree(self):
        self.vertices = sorted(self.vertices, key=functools.cmp_to_key(compare_vertices))


    def get_non_adjacent_vertices(self, vertex: Vertex) -> list[Vertex]:
        non_adjacent_vertices = [] 
        for edge in self.vertices:
            if vertex.name != edge.name and edge not in vertex.edges:
                non_adjacent_vertices.append(edge)
        return non_adjacent_vertices

    def check_data(self):
        vertices_count = len(self.vertices_names)
        if len(self.representation) != vertices_count:
            raise Exception(f'len(self.representation : {len(self.representation)}) != vertices_count : {vertices_count}')
        for row in self.representation:
            if len(row) != vertices_count:
                raise Exception(f'len(row : {len(self.representation)}) != vertices_count : {vertices_count}')


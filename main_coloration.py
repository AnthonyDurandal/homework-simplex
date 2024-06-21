# from ui.rootWindow import RootWindow

from simplex.problem import *
from simplex.simplex_method_2 import *
from graph.graph import *
from graph.dikstra import * 

if __name__ == "__main__":
    vertices_names = ['A','B', 'C', 'D', 'E']
    representation = [
        [0,1,1,0,1],
        [0,0,0,1,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
    ]
    graph = NonOrientedGraph(vertices_names, representation)
    graph.color_graph()
    print([f'{vertex.name}|{vertex.color}|{vertex.get_degree()}' for vertex in graph.vertices])
# from ui.rootWindow import RootWindow

from simplex.problem import *
from simplex.simplex_method_2 import *
from graph.graph import *
from graph.dikstra import * 

if __name__ == "__main__":
    vertices_names = ['A','B', 'C', 'D', 'E','F', 'G', 'H', 'I', 'J']
    representation = [
    #    A,B,C,D,E,F,G,H,I,J
        [0,4,6,0,0,0,0,0,0,0], #A
        [0,0,0,6,2,0,0,0,0,0], #B
        [0,0,0,0,2,3,0,0,0,0], #C
        [0,0,0,0,0,0,2,0,0,0], #D
        [0,0,0,4,0,0,0,6,1,0], #E
        [0,0,0,0,0,0,0,0,8,0], #F
        [0,0,0,0,0,0,0,0,0,7], #G
        [0,0,0,0,0,0,0,0,0,2], #H
        [0,0,0,0,0,0,0,0,0,3], #I
        [0,0,0,0,0,0,0,0,0,0], #J
    ]
    graph = Graph(vertices_names, representation, 'A')

    for vertex in graph.vertices:
        print(vertex.name,[f'{edge.vertex.name} ({edge.length})' for edge in vertex.edges])

    graph.run()

    print('----------------------')
    for vertex in graph.vertices:
        if vertex.previous_vertex != None:
            print(vertex.name,vertex.previous_vertex.name,vertex.shortest_length_to)
    # print([f'{vertex.name}|{vertex.color}|{vertex.get_degree()}' for vertex in graph.vertices])
    print('vita')
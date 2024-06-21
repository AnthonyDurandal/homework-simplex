# from ui.rootWindow import RootWindow

from simplex.problem import *
from simplex.simplex_method_2 import *
from graph.graph import *
from graph.dikstra import * 
from graph.flukerson import * 

if __name__ == "__main__":
    vertices_names = ['S','S1', 's2', 'S3', 'T1','T2', 'T3', 'T4', 'T5', 'R']
    representation = [
    #    S,     S1,   S2,   S3,   T1,   T2,   T3,   T4,   T5,   R
        ['0/0','3/5','2/4','3/3','0/0','0/0','0/0','0/0','0/0','0/0'], #S
        ['0/0','0/0','0/2','0/0','3/3','0/0','0/0','0/0','0/0','0/0'], #S1
        ['0/0','0/0','0/0','0/0','2/2','1/1','1/1','0/0','0/0','0/0'], #S2
        ['0/0','0/0','2/2','0/0','0/0','0/0','1/3','0/0','0/0','0/0'], #S3
        ['0/0','0/0','0/0','0/0','0/0','1/2','0/0','4/7','0/0','0/0'], #T1
        ['0/0','0/0','0/0','0/0','0/0','0/0','0/0','2/2','1/1.5','0/0'], #T2
        ['0/0','0/0','0/0','0/0','0/0','1/3','0/0','1/1','0/0','0/0'], #T3
        ['0/0','0/0','0/0','0/0','0/0','0/0','0/0','0/0','0/0','6/8'], #T4
        ['0/0','0/0','0/0','0/0','0/0','0/0','0/0','0/0','0/0','2/4'], #T5
        ['0/0','0/0','0/0','0/0','0/0','0/0','0/0','0/0','0/0','0/0'], #R
    ]
    graph = Graph(vertices_names, representation, 'S', 'R')

    # for vertex in graph.vertices:
    #     print(vertex.name,[f'{edge.vertex.name} ({edge.length})' for edge in vertex.edges])

    # graph.run()

    # print('----------------------')
    # for vertex in graph.vertices:
    #     if vertex.previous_vertex != None:
    #         print(vertex.name,vertex.previous_vertex.name,vertex.shortest_length_to)
    # # print([f'{vertex.name}|{vertex.color}|{vertex.get_degree()}' for vertex in graph.vertices])
    # print('vita')
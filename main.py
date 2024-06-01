from ui.rootWindow import RootWindow

from simplex.problem import *
from simplex.simplex_method import *

if __name__ == "__main__":
    # RootWindow()
    # x1 = Term('x1', None)
    # x2 = Term('x2', None)
    # x3 = Term('x3', None)

    # objective_function = ObjectiveFunction([Term('x1', 3), Term('x2', 2)])
    
    # c1 = Constraint([Term('x1', 2), Term('x2', 1)], Relationship.INF_OR_EQ, 100)
    # c2 = Constraint([Term('x1', 1), Term('x2', 1)], Relationship.INF_OR_EQ, 80)


    # pb = Problem(['x1', 'x2'], [c1, c2], objective_function)
    # simplex = SimplexMethod(pb)

    # print(pb.solution)

    # --------------------------------------------------------

    # x1 = Term('x1', None)
    # x2 = Term('x2', None)
    # x3 = Term('x3', None)

    # objective_function = ObjectiveFunction([Term('x1', 30), Term('x2', 22), Term('x3', 22)])
    
    # c1 = Constraint([Term('x1', 1), Term('x2', 4), Term('x3', 4)], Relationship.INF_OR_EQ, 50)
    # c2 = Constraint([Term('x1', 4), Term('x2', 4), Term('x3', 3)], Relationship.INF_OR_EQ, 40)
    # c3 = Constraint([Term('x1', 4), Term('x2', 10), Term('x3', 2)], Relationship.INF_OR_EQ, 20)


    # pb = Problem(ProblemType.MAX,['x1', 'x2', 'x3'], [c1, c2, c3], objective_function)
    # simplex = SimplexMethod(pb)

    x1 = Term('x1', None)
    x2 = Term('x2', None)
    x2 = Term('x3', None)

    objective_function = ObjectiveFunction([Term('x1', 30), Term('x2', 3), Term('x3', 10),])
    
    c1 = Constraint([Term('x1', 12), Term('x2', 1), Term('x3', 24),], Relationship.INF_OR_EQ, 3)
    c2 = Constraint([Term('x1', 12), Term('x2', 54), Term('x3', 65), ], Relationship.INF_OR_EQ, 90)
    c3 = Constraint([Term('x1', 6), Term('x2', 4), Term('x3', 23), ], Relationship.INF_OR_EQ, 45)


    pb = Problem(ProblemType.MAX,['x1', 'x2', 'x3'], [c1, c2, c3], objective_function)
    simplex = SimplexMethod(pb)

    print(pb.solution)
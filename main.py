from ui.rootWindow import RootWindow

from simplex.problem import *
from simplex.simplex_method import *

if __name__ == "__main__":
    # RootWindow()
    x1 = Term('x1', None)
    x2 = Term('x2', None)
    x3 = Term('x3', None)

    objective_function = ObjectiveFunction([Term('x1', 3), Term('x2', 2)])
    
    c1 = Constraint([Term('x1', 2), Term('x2', 1)], Relationship.INF_OR_EQ, 100)
    c2 = Constraint([Term('x1', 1), Term('x2', 1)], Relationship.INF_OR_EQ, 80)


    pb = Problem(['x1', 'x2'], [c1, c2], objective_function)
    simplex = SimplexMethod(pb)

    print(pb.solution)
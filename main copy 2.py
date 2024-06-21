# from ui.rootWindow import RootWindow

from simplex.problem import *
from simplex.simplex_method_2 import *

if __name__ == "__main__":
    objective_function = ObjectiveFunction([Term('x1', 3), Term('x2', 5)])
    
    c1 = Constraint([Term('x1', 2), Term('x2', 4), ], Relationship.INF_OR_EQ, 25)
    c2 = Constraint([Term('x1', 1) ], Relationship.INF_OR_EQ, 8)
    c3 = Constraint([Term('x2', 2) ], Relationship.INF_OR_EQ, 10)
    # c4 = Constraint([Term('x2', 1) ], Relationship.SUP_OR_EQ, 3)
    c5 = Constraint([Term('x2', 2) ], Relationship.SUP_OR_EQ, 3)
    c6 = Constraint([Term('x1', 1) ], Relationship.INF_OR_EQ, 6)
    c7 = Constraint([Term('x2', 1) ], Relationship.SUP_OR_EQ, 4)


    pb = Problem(ProblemType.MAX, [c1, c2, c3, c5, c6, c7], objective_function)
    # pb = Problem(ProblemType.MAX, [c1, c2, c3,], objective_function)
    solution = Solution([], None)
    simplex = SimplexMethod(pb, True, solution)
    print(solution.evaluation, [term.to_string() for term in solution.terms])
    # simplex = SimplexMethod(pb)
    # print([term.to_string() for term in simplex.solution.terms])
    # print(simplex.aux_problem.print_constraints())

    # print([v.name for v in simplex.variables])
    # for constraint in simplex.problem.constraints:
    #     print([f'{term.coeff}.{term.name}' for term in constraint.terms])

    # print([f'{s.name} {s.coeff}'for s in simplex.aux_simplex_tableau.solution])

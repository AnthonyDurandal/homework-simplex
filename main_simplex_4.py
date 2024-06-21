# from ui.rootWindow import RootWindow

from simplex.problem import *
from simplex.simplex_method_2 import *

if __name__ == "__main__":
    # objective_function = ObjectiveFunction([Term('x1', 3), Term('x2', 5), ])
    
    # c1 = Constraint([Term('x1', 2), Term('x2', 4), ], Relationship.INF_OR_EQ, 25)
    # c2 = Constraint([Term('x1', 1), ], Relationship.INF_OR_EQ, 8)
    # c3 = Constraint([Term('x1', 0), Term('x2', 2), ], Relationship.INF_OR_EQ, 10)


    # pb = Problem(ProblemType.MAX, [c1, c2, c3], objective_function)

    objective_function = ObjectiveFunction([Term('x1', 3), Term('x2', 4), Term('x3', 1) ])

    c1 = Constraint([Term('x1', 1), Term('x2', 2), Term('x3', 2), ], Relationship.INF_OR_EQ, 8/3)
    c2 = Constraint([Term('x1', 3), Term('x2', 2), Term('x3', 3), ], Relationship.SUP_OR_EQ, 7/3)
    c3 = Constraint([Term('x1', 1), Term('x2', 1), ], Relationship.SUP_OR_EQ, 1)


    pb = Problem(ProblemType.MAX, [c1, c2], objective_function)
    # pb = Problem(ProblemType.MAX, [c1, c2, c3,], objective_function)
    solution = Solution([], None)
    # simplex = SimplexMethod(pb, True, solution)
    # print(solution.evaluation, [term.to_string() for term in solution.terms])
    simplex = SimplexMethod(pb)
    print([term.to_string() for term in simplex.solution.terms], simplex.solution.evaluation)
    # print(simplex.aux_problem.print_constraints())

    # print([v.name for v in simplex.variables])
    # for constraint in simplex.problem.constraints:
    #     print([f'{term.coeff}.{term.name}' for term in constraint.terms])

    # print([f'{s.name} {s.coeff}'for s in simplex.aux_simplex_tableau.solution])

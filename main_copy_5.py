# from ui.rootWindow import RootWindow

from simplex.problem import *
from simplex.simplex_method_2 import *

if __name__ == "__main__":

    objective_function = ObjectiveFunction([Term('x1', 100), Term('x2', 80), ])

    c1 = Constraint([Term('x1', 2), Term('x2', 1), ], Relationship.SUP_OR_EQ, 3)
    c2 = Constraint([Term('x1', 1), Term('x2', 1), ], Relationship.SUP_OR_EQ, 2)


    pb = Problem(ProblemType.MIN, [c1, c2], objective_function)
    # pb = Problem(ProblemType.MAX, [c1, c2, c3,], objective_function)
    solution = Solution([], None)
    # simplex = SimplexMethod(pb, True, solution)
    # print(solution.evaluation, [term.to_string() for term in solution.terms])
    simplex = SimplexMethod(pb)
    for row in simplex.simplex_tableau.rows:
        print(row)
    print([term.to_string() for term in simplex.solution.terms], simplex.solution.evaluation, -simplex.problem.objective_function.evaluate(simplex.solution.terms))
    
    # print(simplex.aux_problem.print_constraints())

    # print([v.name for v in simplex.variables])
    # for constraint in simplex.problem.constraints:
    #     print([f'{term.coeff}.{term.name}' for term in constraint.terms])

    # print([f'{s.name} {s.coeff}'for s in simplex.aux_simplex_tableau.solution])

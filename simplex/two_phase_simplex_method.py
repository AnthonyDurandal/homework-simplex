from simplex.problem import *

class TwoPhaseSimplexMethod:
    def __init__(self, problem: Problem):
        requires_two_phase = False
        for constraint in problem.constraints:
            if constraint.relationship == Relationship.SUP_OR_EQ:
                requires_two_phase = True
                break 
        if requires_two_phase:
            new_problem = problem.problem_copy()
            new_problem.
            
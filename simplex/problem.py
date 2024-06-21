from enum import Enum

class ProblemType(Enum):
    MIN = 'Max'
    MAX = 'Min'
class Relationship(Enum):
    EQUALITY = '='
    INF_OR_EQ = '<='
    SUP_OR_EQ = '>='

class TermCategory(Enum):
    DESCISION = 'descision'
    SLACK = 'slack'
    SURPLUS = 'surplus'
    ARTIFICIAL = 'artificial'

class Term:
    name = None
    coeff = None
    category = None

    def __init__(self, name: str, coeff: float, category: TermCategory = TermCategory.DESCISION):
        self.name = name
        self.coeff = coeff
        self.category = category

    def to_string(self):
        return f'{self.coeff}*{self.name}   '

    def copy(self):
        return Term(self.name, self.coeff, self.category)

class Constraint:
    terms: list[Term] = None
    added_variable: Term = None
    relationship: Relationship = None
    right_hand_constant: float = None

    def __init__(self, terms: list[Term], relationship: Relationship, right_hand_constant: float):
        self.terms = terms
        self.relationship = relationship
        self.right_hand_constant = right_hand_constant

    def to_string(self) -> str:
        return f'{[term.to_string() for term in self.terms]} {self.relationship} {self.right_hand_constant}'

    def get_artificial_variable(self) -> Term | None:
        for term in self.terms:
            if term.category == TermCategory.ARTIFICIAL:
                return term
        return None

    def has_slack_or_artificial_variable(self) -> bool:
        for term in self.terms:
            if term.category == TermCategory.SLACK or term.category == TermCategory.ARTIFICIAL:
                return True
        return False

class ObjectiveFunction(Constraint):
    def __init__(self, terms: list[Term]):
        super().__init__(terms, Relationship.EQUALITY, 0)

    def evaluate(self, solution_terms: list[Term]) -> float:
        total = 0
        for term in self.terms:
            for solution_term in solution_terms:
                if term.name == solution_term.name:
                    total += term.coeff * solution_term.coeff
                    break
        return total

    def to_string(self):
        return f'{[term.to_string() for term in self.terms]} = {self.right_hand_constant}'
    

class Problem:
    problem_type : ProblemType = ProblemType.MAX
    # descision_variables = None
    constraints: list[Constraint] = None
    objective_function = None
    added_variables: list[str] = []
    # variables: list[str] = []
    solution: list[Term] = []
    # artificial_variables : list[str] = []

    def __init__(self, problem_type, constraints: list[Constraint], objective_function: ObjectiveFunction):
        self.problem_type = problem_type
        # self.descision_variables = descision_variables
        # self.variables = descision_variables.copy()
        self.constraints = constraints
        self.objective_function = objective_function

    def problem_copy(self):
        constraints = []
        for constraint in self.constraints:
            new_constraint = Constraint([term.copy() for term in constraint.terms],constraint.relationship, constraint.right_hand_constant)
            constraints.append(new_constraint)

        objective_function_terms = []
        for term in self.objective_function.terms:
            objective_function_terms.append(Term(term.name, term.coeff, term.category))
        objective_function = ObjectiveFunction(objective_function_terms)
        return Problem(self.problem_type, constraints, objective_function)

    def print_constraints(self):
        for constraint in self.constraints:
            print(constraint.to_string())
    

        
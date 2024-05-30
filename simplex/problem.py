from enum import Enum
class Relationship(Enum):
    EQUALITY = '='
    INF = '<'
    SUP = '>'
    INF_OR_EQ = '<='
    SUP_OR_EQ = '>='

class Term:
    variable = None
    coeff = None
    added_variable = None
    artificial_variable = None

    def __init__(self, variable: str, coeff: float):
        self.variable = variable
        self.coeff = coeff

class Constraint:
    terms: list[Term] = None
    added_variable: Term = None
    relationship: Relationship = None
    right_hand_constant: float = None

    def __init__(self, terms: list[Term], relationship: Relationship, right_hand_constant: float):
        self.terms = terms
        self.relationship = relationship
        self.right_hand_constant = right_hand_constant

class ObjectiveFunction(Constraint):
    def __init__(self, terms: list[Term]):
        super().__init__(terms, Relationship.EQUALITY, 0)
    

class Problem:
    descision_variables = None
    constraints: list[Constraint] = None
    objective_function = None
    added_variables: list[Term] = []
    variables: list[Term] = []
    solution: list[Term] = []

    def __init__(self, descision_variables: list[str], constraints: list[Constraint], objective_function):
        self.descision_variables = descision_variables
        self.variables = descision_variables.copy()
        self.constraints = constraints
        self.objective_function = objective_function
        
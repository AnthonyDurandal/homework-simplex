import math
import functools

from simplex.problem import Problem, Relationship, Term, ProblemType, TermCategory, ObjectiveFunction, Constraint
from simplex.simplex_tableau import SimplexTableau


def compare_terms(term_a : Term, term_b : Term) -> int:
    if term_a.name[0] == term_b.name[0]:
        return -1 if term_a.name < term_b.name else 1
    elif term_a.name[0] == 'x':
        return -1
    elif term_a.name[0] == 'u' and term_b.name == 'a':
        return -1
    else:
        return 1


class NonBasicVariable :
    column_num : int = None
    row_num : int = None
    name: str = None

    def __init__(self, name: str, column_num : int, row_num : int):
        self.name = name
        self.column_num = column_num
        self.row_num = row_num
    
class Solution :
    terms : list[Term] = None 
    evaluation : float = None

    def __init__(self, terms: list[Term], evaluation: float):
        self.terms = terms
        self.evaluation = evaluation

class SimplexMethod:
    problem: Problem = None
    aux_problem: Problem = None
    aux_simplex = None
    simplex_tableau : SimplexTableau = None
    aux_simplex_tableau: SimplexTableau = None
    variables : list[Term] = []
    solution: Solution = None
    probable_solutions = []
    descision_variables : list[str] = None

    def __init__(self, problem: Problem, int_solution: bool = False, best_solution : Solution = None):
        self.problem = problem

        if self.problem.problem_type == ProblemType.MIN:
            self.problem.problem_type = ProblemType.MAX
            for term in self.problem.objective_function.terms:
                term.coeff = -term.coeff

        self.print()
        
        self.add_variables()
        self.problem.objective_function.terms = sorted(self.problem.objective_function.terms, key=functools.cmp_to_key(compare_terms))
        self.variables = sorted(self.variables, key=functools.cmp_to_key(compare_terms))

        if self.requires_two_phase():
            self.create_aux_problem()
            print(f'create aux for {self.aux_problem.problem_type} {[self.aux_problem.objective_function.to_string()]}')
            
            aux_simplex = SimplexMethod(self.aux_problem)
            self.aux_simplex = aux_simplex
            self.aux_simplex.simplex_tableau.resolve()

            evaluation = -self.aux_simplex.simplex_tableau.rows[-1][-1]

            if evaluation == 0:
                artificial_variables_columns = []
                simplex_last_row = []

                i = 0
                print(f'VARIABLEEEEEEEEEESSSSSS {[f"{term.name} {term.category}" for term in self.aux_simplex.variables]}')
                for term in self.aux_simplex.variables:
                    if term.category == TermCategory.ARTIFICIAL:
                        artificial_variables_columns.append(i)
                        
                    for obj_term in self.problem.objective_function.terms:
                        if obj_term.name == term.name:
                            simplex_last_row.append(obj_term.coeff)
                            break
                    
                    if len(simplex_last_row) == i:
                        simplex_last_row.append(0)
                    i+=1
                simplex_last_row.append(self.problem.objective_function.right_hand_constant)
                
                simplex_tableau_rows = self.aux_simplex.simplex_tableau.rows[:-1]
                
                simplex_tableau_rows.append(simplex_last_row)

                slack_variables = []
                print([term.name for term in self.aux_simplex.variables])
                x = 0
                while x<len(self.aux_simplex.variables):
                    term = self.aux_simplex.variables[x]
                    if term.category == TermCategory.SLACK:
                        slack_variables.append(term.name)
                    elif term.category == TermCategory.ARTIFICIAL:
                        del self.aux_simplex.variables[x]

                        for row in simplex_tableau_rows:
                            del row[x]
                        x-=1
                    x+=1

                variables_filtered = filter(lambda term : term.category != TermCategory.ARTIFICIAL ,self.aux_simplex.variables)
                # self.variables = filter(lambda term : term.category != TermCategory.ARTIFICIAL ,self.variables)
                s = SimplexTableau(simplex_tableau_rows, self.problem.problem_type, [term.name for term in variables_filtered], self.aux_simplex.simplex_tableau.slack_variables)
                s.resolve()

                self.simplex_tableau = s

        else:
            self.init_simplex_tableau()
            self.simplex_tableau.resolve()

        # print(f'soluce : {[term.to_string() for term in self.solution.terms]}')

        if self.requires_two_phase() and self.aux_simplex != None and self.aux_simplex.simplex_tableau.rows[-1][-1] != 0:
            raise Exception('infeasible ')
            return

        solution_terms = []
        for s_term in self.simplex_tableau.solution_terms:
            for term in self.variables:
                if s_term.name == term.name and term.category == TermCategory.DESCISION:
                    s_term.category = TermCategory.DESCISION
                    solution_terms.append(s_term)
                    break

        self.solution = Solution(solution_terms, -self.simplex_tableau.rows[-1][-1])

        non_integer_term_index = self.check_integer_solution()
       
        if int_solution and self.is_feasible():
            # print(f'{self.problem.objective_function.to_string()}, {self.is_feasible()}, {non_integer_term_index}, {[term.to_string() for term in self.solution.terms]}')
            
            # for constraint in self.problem.constraints:
                # print(constraint.to_string())
            # print('_-_-_-_-_-_-_-_-_-_-_-_-_-_-_')
            
            if best_solution == None : raise Error()

            if non_integer_term_index == None and len(self.solution.terms) > 0 and (best_solution.evaluation == None or self.solution.evaluation > best_solution.evaluation):
                best_solution.evaluation = self.solution.evaluation
                best_solution.terms = self.solution.terms
                print(f'found a mfking solution : {best_solution.evaluation} ; {[term.to_string() for term in self.solution.terms]}')

                # print(f'replacing bro : {best_solution.evaluation} {term.to_string() for term in best_solution.terms}')

            if non_integer_term_index != None and (best_solution.evaluation == None or (best_solution.evaluation != None and self.solution.evaluation > best_solution.evaluation)):
                print(f'non integer eh: {non_integer_term_index} ; {self.solution.terms[non_integer_term_index].to_string()}')
                non_integer_term = self.solution.terms[non_integer_term_index]
                
                integer_inf_coeff = math.floor(non_integer_term.coeff) 
                integer_sup_coeff = math.ceil(non_integer_term.coeff) 
                
                branch_pb_1 = self.problem.problem_copy()
                branch_pb_1.constraints.append(Constraint([Term(non_integer_term.name, 1)], Relationship.INF_OR_EQ, integer_inf_coeff ))

                branch_pb_2 = self.problem.problem_copy()
                branch_pb_2.constraints.append(Constraint([Term(non_integer_term.name, 1)], Relationship.SUP_OR_EQ, integer_sup_coeff ))
                
                # print(f'{branch_pb_1.constraints[-1].to_string()}')
                print('b1')
                SimplexMethod(branch_pb_1, True, best_solution)
                # print(f'{branch_pb_2.constraints[-1].to_string()}')
                print('b2')
                SimplexMethod(branch_pb_2, True, best_solution)

        print('done --------------------------------------------')            
    
    def requires_two_phase(self):
        for constraint in self.problem.constraints:
            if constraint.relationship == Relationship.SUP_OR_EQ:
                return True
        return False

    def add_variables(self):
        slack_count = 1+len(self.variables)
        surplus_count = 1+len(self.variables)
        artificial_count = 1+len(self.variables)
        for constraint in self.problem.constraints:
            if constraint.has_slack_or_artificial_variable():
                continue
            elif constraint.relationship == Relationship.INF_OR_EQ:
                slack_variable = Term(f's{slack_count}', +1, TermCategory.SLACK)
                constraint.terms.append(slack_variable)
                self.variables.append(slack_variable)
                slack_count+=1
            elif constraint.relationship == Relationship.SUP_OR_EQ:
                surplus_variable = Term(f'u{surplus_count}', -1, TermCategory.SURPLUS)
                constraint.terms.append(surplus_variable)
                self.variables.append(surplus_variable)
                surplus_count+=1

                artificial_variable = Term(f'a{artificial_count}', +1, TermCategory.ARTIFICIAL)
                constraint.terms.append(artificial_variable)
                self.variables.append(artificial_variable)
                artificial_count+=1

            for term in constraint.terms:
                if self.is_in_variables_array(term.name) == False:
                    self.variables.append(Term(term.name, None, term.category))

    def is_in_variables_array(self, term_name: str) -> bool:
        for term in self.variables:
            if term.name == term_name:
                return True
        return False



    def create_aux_problem(self):
        aux_problem = self.problem.problem_copy()
        # if self.problem.problem_type == ProblemType.MIN:
        #     aux_problem.problem_type = ProblemType.MAX
        # else:
        #     aux_problem.problem_type = ProblemType.MIN

        objective_function_terms : list[Term] = []
        
        for constraint in aux_problem.constraints:
            constraint.relationship = Relationship.EQUALITY

            artificial_variable = constraint.get_artificial_variable()
            if artificial_variable != None:
                aux_problem.objective_function.right_hand_constant -= constraint.right_hand_constant

                for term in constraint.terms:
                    if term == artificial_variable:
                        continue
                    found_term_in_obj_function = False
                    for obj_term in objective_function_terms:
                        if obj_term.name == term.name:
                            obj_term.coeff += term.coeff
                            found_term_in_obj_function = True
                            break
                    if not found_term_in_obj_function:
                        term_copy = term.copy()
                        term_copy.coeff = term_copy.coeff
                        objective_function_terms.append(term_copy)

        aux_problem.objective_function.terms = objective_function_terms

        print(f'HANAZEIPORUAZPEIRU {[term.name for term in self.variables]}')
        for term in self.variables:
            not_found = True
            for aux_term in aux_problem.objective_function.terms:
                if term.name == aux_term.name:
                    not_found = False
                    break
            if not_found:
                zero_coeff_term = term.copy()
                zero_coeff_term.coeff = 0
                aux_problem.objective_function.terms.append(zero_coeff_term)
            

        aux_problem.objective_function.terms = sorted(aux_problem.objective_function.terms, key=functools.cmp_to_key(compare_terms))

        self.aux_problem = aux_problem
                
            
        # artificial_variables = filter(lambda v: v.category == TermCategory.ARTIFICIAL, self.variables)
        # objective_function = ObjectiveFunction(artificial_variables)
        # constraints = []
        # for constraint in self.problem.constraints:
        #     new_constraint = Constraint([Term(term.name, term.coeff, term.category) for term in constraint.terms], Relationship.INF_OR_EQ, constraint.right_hand_constant)
        #     constraints.append(new_constraint)
        # # aux_problem = self.problem.problem_copy()
        # # for constraint in aux_problem.constraints:
        # #     constraint.relationship = Relationship.INF_OR_EQ
        # # aux_problem.problem_type = ProblemType.MIN
        # # aux_problem.objective_function = 
        # self.aux_problem = Problem(ProblemType.MIN, constraints, objective_function)

    def init_simplex_tableau(self):
        slack_variables = filter(lambda v : v.category == TermCategory.ARTIFICIAL or v.category == TermCategory.SLACK ,self.variables)
        
        simplex_tableau = []
        for constraint in self.problem.constraints:
            row = []
            for variable in self.variables:
                found_term = False
                for term in constraint.terms:
                    if term.name == variable.name:
                        row.append(term.coeff)
                        found_term = True
                        break
                if not found_term:
                    row.append(0)
            row.append(constraint.right_hand_constant)
            simplex_tableau.append(row)

        objective_function_row = []
        for variable in self.variables:
            found_term = False
            for term in self.problem.objective_function.terms:
                if term.name == variable.name:
                    objective_function_row.append(term.coeff)
                    found_term = True
                    break
            if found_term == False:
                objective_function_row.append(0)
        objective_function_row.append(-self.problem.objective_function.right_hand_constant)
        simplex_tableau.append(objective_function_row)

        self.simplex_tableau = SimplexTableau(simplex_tableau, self.problem.problem_type,[v.name for v in self.variables] , [v.name for v in slack_variables])


    def resolve_aux(self):
        pass

    def resolve_normal_simplex(self):
        SimplexTableau()

    def check_integer_solution(self) -> int:
        x = 0
        size = len(self.solution.terms)
        while x < size:
            if self.solution.terms[x].category == TermCategory.DESCISION and not float(self.solution.terms[x].coeff).is_integer():
                return x
            x+=1
        return None

    def is_feasible(self) -> bool:
        for term in self.solution.terms:
            if term.category == TermCategory.ARTIFICIAL and term.coeff > 0:
                return False
        return True



    def print(self):
        print('---------------')
        print(self.problem.objective_function.to_string())
        constraint_count = 0
        for constraint in self.problem.constraints:
            if constraint_count <= 7:
                print(constraint.to_string())
            constraint_count+=1
        print('---------------')
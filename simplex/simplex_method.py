from simplex.problem import Problem, Relationship, Term, ProblemType

class NonBasicVariable :
    column_num : int = None
    row_num : int = None
    name: str = None

    def __init__(self, name: str, column_num : int, row_num : int):
        self.name = name
        self.column_num = column_num
        self.row_num = row_num

class SimplexMethod:
    problem = None
    bv = None # basic variables
    nbv : list[NonBasicVariable] = None # non basic variables
    simplex_tableau = None
    pivot_x = 0
    pivot_y = 0
    additional_v = None # slack and surplus variables
    nb_added_v = 0
    nb_bv = 0
    nb_nbv = 0
    departing_variable: NonBasicVariable = None

    def __init__(self, problem: Problem) :
        self.problem = problem
        self.nb_added_v = len(problem.constraints)
        self.nb_bv = self.nb_added_v
        self.nb_nbv = self.nb_added_v + len(problem.descision_variables) - self.nb_bv

        self.check_normal_simplex_conditions()
        self.add_additional_variables()
        self.init_simplex_tableau()

        self.bv = self.problem.descision_variables
        self.nbv = [ NonBasicVariable(name, len(self.problem.added_variables) - row_num, row_num) for row_num, name in enumerate(self.problem.added_variables)]

        self.resolve()


    def resolve(self):
        self.pivot()
        objective_function = self.get_objective_function_row()
        self.print_simplex_tableau()
        for x in range(len(objective_function) - 1):
            if objective_function[x] > 0:
                self.resolve()
        self.problem.solution = []
        y = 0
        for non_basic_variable in self.nbv:
            self.problem.solution.append({non_basic_variable.name:self.simplex_tableau[y][-1]})
            y+=1
        return self.problem.solution

        

    def init_simplex_tableau(self):
        simplex_tableau = []
        for constraint in self.problem.constraints:
            row = []
            for term in constraint.terms:
                row.append(term.coeff)
            for added_variable in self.problem.added_variables:
                if added_variable == constraint.added_variable:
                    row.append(added_variable.coeff)
                else:
                    row.append(0)
            row.append(constraint.right_hand_constant)
            simplex_tableau.append(row)
        self.simplex_tableau = simplex_tableau
        self.bv = self.problem.variables
        # if len(self.bv) < self.nb_bv: # TODO: add condition when (nb of constraint)< nb of 
        # self.nbv = [constraint for constraint in self.problem.constraints]

        # last_line_terms = self.problem.variables
        # print(f'hehe {[el for el in last_line_terms]}')

        objective_function_coeffs = []
        for term in self.problem.objective_function.terms:
            objective_function_coeffs.append(term.coeff)
        for added_variable in self.problem.added_variables:
            objective_function_coeffs.append(0)
        objective_function_coeffs.append(0)
        simplex_tableau.append(objective_function_coeffs)

        self.simplex_tableau = simplex_tableau
        
    

    def normal_simplex(self):
        pass

    def check_normal_simplex_conditions(self):
        pass
        # for constraint in self.problem.constraints:
        #     if constraint.relationship != Relationship.INF_OR_EQ and constraint.relationship!= Relationship.EQUALITY:
        #         raise ValueError(f"constraint of inequality is not verified")

    def add_additional_variables(self):
        additional_v = []
        for x in range(len(self.problem.constraints)):
            constraint = self.problem.constraints[x]
            if constraint.relationship == Relationship.INF_OR_EQ:
                slack_variable = Term(f'a{x+1}', 1)
                constraint.added_variable = slack_variable
                additional_v.append(slack_variable.variable)
                # self.problem.added_variables.append(added_variable)
            # else:
            #     problem.added_variable = Term(f'a{x+1}', -1)
        self.problem.added_variables = additional_v
        self.problem.variables.extend([v for v in additional_v])

    def find_pivot_column(self):
        objective_function_row = self.get_objective_function_row()
        pivot_x = 0
        size = len(objective_function_row) - 1
        x = 0
        while x < size:
            if self.problem.problem_type == ProblemType.MAX and objective_function_row[x] > 0 and objective_function_row[x] > objective_function_row[pivot_x]:
                pivot_x = x
            elif self.problem.problem_type == ProblemType.MIN and objective_function_row[x] > 0 and objective_function_row[x] < objective_function_row[pivot_x]:
                pivot_x = x
            x+=1
        if objective_function_row[pivot_x] <= 0: # TODO: the problem is done when they are all <= 0
            pass
        self.pivot_x = pivot_x

    def find_pivot_row(self):
        length = len(self.simplex_tableau)
        y = 0
        pivot_y = 0 # supposing that the simplex_tableau is not empty
        pivot_line_ratio = self.simplex_tableau[pivot_y][-1]/self.simplex_tableau[pivot_y][self.pivot_x]
        while y < length - 1 :
            if self.simplex_tableau[y][self.pivot_x] < 0:
                continue
            ratio_y = self.simplex_tableau[y][-1]/self.simplex_tableau[y][self.pivot_x]
            if ratio_y < pivot_line_ratio:
                pivot_y = y
                pivot_line_ratio = self.simplex_tableau[pivot_y][-1]/self.simplex_tableau[pivot_y][self.pivot_x]
            y += 1
        self.pivot_y = pivot_y

    def find_departing_variable(self):
        print(f'non basic variables : {[el.name for el in self.nbv]}')
        for non_basic_variable in  self.nbv:
            if non_basic_variable.row_num == self.pivot_y:
                self.departing_variable = non_basic_variable
                return non_basic_variable
        return None

        # for non_basic_variable in self.nbv:
            
            

    def get_objective_function_row(self) -> list[float]:
        return self.simplex_tableau[-1]

    def pivot(self):
        self.find_pivot_column()
        self.find_pivot_row()
        self.find_departing_variable()

        entering_variable = self.problem.variables[self.pivot_x]
        departing_variable = self.departing_variable

        self.nbv = [NonBasicVariable(entering_variable, self.pivot_x, self.pivot_y) if el == departing_variable else el for el in self.nbv]
        self.bv = [departing_variable.name if el == entering_variable else el for el in self.nbv]

        print(f'{entering_variable} in , {departing_variable.name} out')
        
        i = 0
        pivot_coeff = self.simplex_tableau[self.pivot_y][self.pivot_x]
        while i < len(self.simplex_tableau[self.pivot_y]):
            self.simplex_tableau[self.pivot_y][i] /= pivot_coeff 
            i+=1

        y = 0
        width = len(self.simplex_tableau[0])
        length = len(self.simplex_tableau)
        while y < length:
            if y != self.pivot_y:
                gaussian_coeff = self.simplex_tableau[y][self.pivot_x]
                x = 0
                while x < width:
                    self.simplex_tableau[y][x] -= self.simplex_tableau[self.pivot_y][x] * gaussian_coeff
                    x+=1
            y += 1
    

    def print_simplex_tableau(self):
        print('------------')
        for el in self.simplex_tableau:
            print(el)
        print('------------')


    
    
from simplex.problem import *
class SimplexTableau:
    rows : list[list[float]] = None
    num_rows = 0
    num_cols = 0
    bv = []
    nbs = []
    # pivot : {'x' : int, 'y': int} = {'x':0, 'y':0}
    pivot_x = 0
    pivot_y = 0
    variables = None
    slack_variables = None
    solution_terms = None

    def __init__(self, rows, problem_type: ProblemType, variables: list[str],slack_variables: list[str]):
        # TODO : change the "num_rows" and "num_cols"
        # print('EEEEEEEEEEEEEEEEEEEEEEE', variables, len(rows), len(rows[-1]), len(slack_variables))
        print(problem_type, variables, slack_variables)
        self.problem_type = problem_type
        self.rows = rows
        self.num_rows = len(rows)
        self.num_cols = len(rows[-1])

        self.variables = variables
        self.slack_variables = slack_variables        

    def resolve(self):
        self.find_pivot()
        if self.rows[-1][self.pivot_x] > 0:
            self.pivot()
            self.resolve()
        else:
            solution_terms = []
            y = 0
            size = len(self.slack_variables)
            print(len(self.rows), size, 'he')
            print(self.slack_variables)
            while y < size:
                # this condition would've been util
                # if self.slack_variables[y] in self.descision_variables:
                # solution_terms.append(Term(self.variables[y], self.rows[y][-1]))
                solution_terms.append(Term(self.slack_variables[y], self.rows[y][-1]))
                y+=1
            # solution = [Term(name, coeff) for name,coeff in zip(self.variables, self.rows[-1])]
            self.solution_terms = solution_terms
        

    def find_pivot(self):
        count = 0
        self.pivot_x = 0
        while count < self.num_cols - 1:
            if self.problem_type == ProblemType.MAX:
                if (self.rows[-1][self.pivot_x] <= 0 and self.rows[-1][count] > 0) or (self.rows[-1][count] > 0 and self.rows[-1][count] > self.rows[-1][self.pivot_x]):
                    self.pivot_x = count
            elif self.problem_type == ProblemType.MIN:
                # print(f'comparing: {self.rows[-1][self.pivot_x]} and {self.rows[-1][count]}')
                if (self.rows[-1][self.pivot_x] <= 0 and self.rows[-1][count] > 0) or (self.rows[-1][count] > 0 and self.rows[-1][count] < self.rows[-1][self.pivot_x]):
                    self.pivot_x = count
            count+=1

        print(f'the pivot is : {self.pivot_x} = {self.rows[-1][self.pivot_x]}')
        
        self.pivot_y = None
        for row_num, row in enumerate(self.rows):
            if row_num == self.num_rows - 1:
                break
            if row[self.pivot_x] > 0:
                if self.pivot_y == None:
                    self.pivot_y = row_num
                elif row[-1]/row[self.pivot_x] < self.rows[self.pivot_y][-1]/self.rows[self.pivot_y][self.pivot_x]:
                    self.pivot_y = row_num

        if self.pivot_y == None:
            raise Exception("The problem is unbounded")
        # if self.rows[self.pivot_y][self.pivot_x] < 0:
        #     raise Exception('did not find a single pivot => done')

    def pivot(self):
        self.print_simplex_tableau()
        entering_variable = self.variables[self.pivot_x]
        self.slack_variables[self.pivot_y] = entering_variable

        pivot_value = self.get_pivot_value()

        x = 0
        while x < self.num_cols:
            self.rows[self.pivot_y][x] /= pivot_value 
            x+=1

        y = 0
        for row in self.rows:
            if y != self.pivot_y:
                x = 0
                coeff = row[self.pivot_x]
                while x < self.num_cols:
                    row[x] -= (self.rows[self.pivot_y][x] * coeff) 
                    x+=1
            y+=1

        self.print_simplex_tableau()


    def get_pivot_value(self) -> float:
        return self.rows[self.pivot_y][self.pivot_x]

    def print_simplex_tableau(self):
        print('----------')
        for row in self.rows:
            print(row)

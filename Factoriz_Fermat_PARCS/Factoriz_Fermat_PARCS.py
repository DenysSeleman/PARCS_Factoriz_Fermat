import math
from Pyro4 import expose

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
    
    def solve(self):
        arr = self.read_input()
        step = int(len(arr) / len(self.workers))
        mapped = []
        for i in range(0, len(self.workers)):
            mapped.append(self.workers[i].create_output([j for j in arr[i*step:i*step+step]]))
        self.write_output(mapped)

    def read_input(self):
        with open(self.input_file_name, 'r') as file:
            lines = file.readlines()
            random_numbers = [int(line.split()[0]) for line in lines]
            return random_numbers

    def write_output(self, output):
        with open(self.output_file_name, 'w') as file:
            for section in output:
                for el in section.value:
                    file.write(str(el[0]) + ": " + str(el[1]) + "\n")
    
    @staticmethod
    @expose   
    def create_output(random_numbers):
        output = []
        for number in random_numbers:
            factors = Solver.fermat_factorization(number)
            output.append((number, factors))
        return output

    @staticmethod
    @expose   
    def fermat_factorization(n):
        if n % 2 == 0:
            if n // 2 != 1:
                return [2] + Solver.fermat_factorization(n // 2)
            else:
                return [2]
    
        a = math.ceil(math.sqrt(n))
        b2 = a * a - n
        while not math.sqrt(b2).is_integer():
            a += 1
            b2 = a * a - n
    
        factor1 = a + int(math.sqrt(b2))
        factor2 = a - int(math.sqrt(b2))
    
        if factor1 == 1:
            return [factor2]
        elif factor2 == 1:
            return [factor1]
        else:
            return Solver.fermat_factorization(factor1) + Solver.fermat_factorization(factor2)
class PFunction():

    def __init__(self, params):
        self.params = params

    def calculate(self, w):
        return self.params[0] * w * (self.params[1] - w) 

    def tabulate(self, points, filename):
        with open("tabulated_functions/" + filename, 'w') as f:
            for x in points:
                f.write("{} {}\n".format(x, self.calculate(x)))
import numpy as np

class SFunction():

    def __init__(self, params):
        self.params = params

    def calculate(self, t):
        return self.params[0] * t + np.sin(t)

    def tabulate(self, points, filename):
        with open("tabulated_functions/" + filename, 'w') as f:
            for x in points:
                f.write("{} {}\n".format(x, self.calculate(x)))
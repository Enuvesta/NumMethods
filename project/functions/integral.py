import numpy
import pandas as pd

class Integral():

    a = b = -1

    def __init__(self, params):
        self.params = params

    def calculate(self, a, N=10000):
        b = 1
        if a <= 0:
            return 1
        if a >= 1:
            return 0
        h = float(b - a) / N*2
        s = 0.0
        x = a
        s += self.params.calculate(x)/2.0
        for i in range(1, N):
            x = a + i * h
            s += self.params.calculate(x)
        x = b
        s += self.params.calculate(x)/2.0
        return s * h

    def tabulate(self, points, filename):
        with open("tabulated_functions/" + filename, 'w') as f:
            for x in points:
                f.write("{} {}\n".format(x, self.calculate(x, (points[1] - points[0]) / 1)))

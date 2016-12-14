class FFunction():

    def __init__(self, params):
        self.params = params

    def calculate(self, t, x_t):
        # beta - 0
        # s(t) - 1
        # z(t) - 2
        # N    - 3
        N = self.params[3]
        return self.params[0] * (self.params[1].calculate(t) - x_t)
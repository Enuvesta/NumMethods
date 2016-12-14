import numpy as np
import bisect

class InterpolatedFunction():

    def __init__(self, tabulated_func_filename, points=None):
        self.params = self.calculate_interpolation_coeffs(tabulated_func_filename, points)


    def fill_in_matrix(self, A, b, n, h, y):
        for i in range(1, n-2):
            A[i][i-1] = h[i]
            
            A[i][i  ] = 2*(h[i]+h[i+1])
            
            A[i][i+1] = h[i+1]
        
            b[i] = 3 * ((y[i+2] - y[i+1]) / h[i+1] - (y[i+1] - y[i]) / h[i])
        
        A[0][0  ] = 2*(h[0] + h[1])
        A[0][1  ] = h[1]
        b[0] = 3 * ((y[2] - y[1]) / h[1] - (y[1] - y[0]) / h[0])
        
        A[n-2][n-3] = h[n-2]
        A[n-2][n-2] = 2*(h[n-2] + h[n-1])
        b[n-2] = 3 * ((y[n] - y[n-1]) / h[n-1] - (y[n-1] - y[n-2]) / h[n-2])

        return(A, b)

    def kramer(self, m, b):
        tmp = list(zip(*m))
        delta = np.linalg.det(tmp)
        if delta == 0:
            return "Решений нет"
        result = []
        for i in range(len(m)):
            A = tmp[:]
            A[i] = b
            result.append((np.linalg.det(A) / delta))
        return np.array(result)

    def getSpline(self, x, y): 

        n = len(x) - 1
        
        h = [float(x[i] - x[i - 1]) for i in range(1, n + 1)]
        

        self.x, self.a = x, y

        self.b = [0] * (n + 1)
        self.c = [0] * (n + 1)
        self.d = [0] * (n + 1)
        
        
        A = np.zeros((n-1, n-1))
        b = np.zeros((n-1))

        
        A, b = self.fill_in_matrix(A, b, n, h, y)

        ans = self.kramer(A, b)

        for i in reversed(range(1, n)): self.c[i] = ans[i-1]
        self.c[0], self.c[n] = 0, 0
        
        for i in reversed(range(1,n+1)):
            self.d[i] = (self.c[i] - self.c[i-1]) / (3*h[i - 1])
            self.b[i] = ((y[i] - y[i-1]) / h[i-1]) + h[i-1]*(2*self.c[i] + (self.c[i-1]))/3
        self.x = x
        self.f = y
        return None

    def calculate_interpolation_coeffs(self, tabulated_func_filename, points=None):
        x = []
        f = []
        if points is not None:
            x = [point for point in points[0]]
            f = [point for point in points[1]]
        else:
            with open("tabulated_functions/" + tabulated_func_filename, 'r') as file:
                for line in file:
                    point = line.strip().split(' ')
                    x.append(float(point[0]))
                    f.append(float(point[1]))


        self.getSpline(x, f)
        return None

    def calculate(self, x):
        distribution = self.x
        indx = bisect.bisect_left(distribution, x)
        if indx == len(distribution): return 0
        dx = x - self.x[indx]
        return self.a[indx] + self.b[indx] * dx + self.c[indx] * dx**2 + self.d[indx] * dx**3
        
    def tabulate(self, points, filename):
        with open("tabulated_functions/" + filename, 'w') as f:
            for x in points:
                f.write("{} {}\n".format(x, self.calculate(x)))
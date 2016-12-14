import numpy as np
from functions import integral


def RungeKutta(f, g, t, x_0, y_0):
    x = np.zeros(len(t))
    x[0] = x_0
    y = np.zeros(len(t))
    y[0] = y_0
    
    for i in range(0, len(t) - 1):
        h = t[i + 1] - t[i]
        k0 = f(t[i], x[i], y[i]) * h
        q0 = g(t[i], x[i], y[i]) * h
        
        k1 = f(t[i] + h / 2, x[i] + k0 / 2, y[i] + q0 / 2) * h
        q1 = g(t[i] + h / 2, x[i] + k0 / 2, y[i] + q0 / 2) * h
        
        k2 = f(t[i] + h / 2, x[i] + k1 / 2, y[i] + q1 / 2) * h
        q2 = g(t[i] + h / 2, x[i] + k1 / 2, y[i] + q1 / 2) * h
        
        k3 = f(t[i] + h, x[i] + k2, y[i] + q2) * h
        q3 = g(t[i] + h, x[i] + k2, y[i] + q2) * h

        
        x[i + 1] = x[i] + (k0 + 2 * k1 + 2 * k2 + k3) / 6
        y[i + 1] = y[i] + (q0 + 2 * q1 + 2 * q2 + q3) / 6
    
    return x, y


def solve(x_0, y_0, beta, T, N, p_func, z_func, s_func, u_func, f_func):
    t_range = np.arange(0, T + T/N, T/N)

    def f_function(t, x, y):
        if t == T:
            derived_z_i = (z_func.calculate(t) - z_func.calculate(t - 1/(N * 10))) * N * 10
        else:
            derived_z_i = (z_func.calculate(t + 1/(N * 10)) - z_func.calculate(t)) * N * 10
        return derived_z_i * u_func.calculate(y)
    
    def g_function(t, x, y):
        return f_func.calculate(t, x)
    
    x_ans, y_ans = RungeKutta(f_function, g_function, t_range, x_0, y_0)
    print_solution(x_ans, y_ans, t_range)
    c2 = np.abs(x_ans[-1] - s_func.calculate(T)) / s_func.calculate(T)

    class C1Integrand2():
        def __init__(self):
            pass

        def calculate(w):
            return w * p_func.calculate(w)

    c1_integral_of_integrand = integral.Integral(C1Integrand2())

    class C1Integrand():
        def __init__(self, params):
            self.params = params

        def calculate(t):
            # x'(t)
            i = np.searchsorted(t_range, t)
            if t_range[i] < t or i == len(t_range) - 1:
                i -= 1
            derived_x = (x_ans[i + 1] - x_ans[i]) / (t_range[i + 1] - t_range[i])
            if t == t_range[i]:
                return derived_x * self.params.calculate(y_ans[i])
            return derived_x * self.params.calculate((y_ans[t] + y_ans[t + 1]) / 2)

    c1_integral = integral.Integral(C1Integrand(c1_integral_of_integrand))
    c1 =  1 - c1_integral.calculate(0) / (x_ans[-1] - x_ans[0])
    return c1, c2


def print_solution(x, y, t_range):
    with open("x_answer.txt", 'w') as output_file:
        for i in range(0, len(t_range)):
            output_file.write("{} {}\n".format(t_range[i], x[i]))
    with open("y_answer.txt", 'w') as output_file:
        for i in range(0, len(t_range)):
            output_file.write("{} {}\n".format(t_range[i], y[i]))
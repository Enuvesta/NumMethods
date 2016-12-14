import numpy as np
import sys
from PyQt5.QtWidgets import QApplication as QApp5
import Solver
import interface
from functions import z_function, p_function, s_function, integral, interpolated_function, f_function

def initialize_functions(a, b, c, d):
    p_func = p_function.PFunction([a, b])
    z_func = z_function.ZFunction([c])
    s_func = s_function.SFunction([d])

    return p_func, z_func, s_func

def func_to_min(c):
    return c[0] + 10 * c[1]

def manual_mode(a, b, c, d, x_0, y_0, beta, T, calculating_mod):
    N = 50

    if calculating_mod == "Ручной" or calculating_mod == "Авто":
        p_func, z_func, s_func = initialize_functions(a, b, c ,d)

        p_func.tabulate(np.arange(0, T + T/N, T/N), "p_func_tabulated")
        z_func.tabulate(np.arange(0, T + T/N, T/N), "z_func_tabulated")
        s_func.tabulate(np.arange(0, T + T/N, T/N), "s_func_tabulated")

    p_interpolated = interpolated_function.InterpolatedFunction("p_func_tabulated")
    z_interpolated = interpolated_function.InterpolatedFunction("z_func_tabulated")
    s_interpolated = interpolated_function.InterpolatedFunction("s_func_tabulated")

    p_interpolated.tabulate(np.arange(0, T + T/(N * 100), T/(N * 100)), "p_func_interp_tabulated")
    z_interpolated.tabulate(np.arange(0, T + T/(N * 100), T/(N * 100)), "z_func_interp_tabulated")
    s_interpolated.tabulate(np.arange(0, T + T/(N * 100), T/(N * 100)), "s_func_interp_tabulated")
    
    integral_p = integral.Integral(p_interpolated)

    f_func = f_function.FFunction([beta, s_interpolated, z_interpolated, N])

    c1, c2 = Solver.solve(x_0, y_0, beta, T,  N, p_interpolated, z_interpolated, s_interpolated, integral_p, f_func)

    return c1, c2

def main(a, b, c, d, x_0, y_0, beta, T, calculating_mod):
    if calculating_mod == "Ручной" or calculating_mod == "Ручной+файл":
        c1, c2 = manual_mode(a, b, c, d, x_0, y_0, beta, T, calculating_mod)
        print("c1: {}\n c2: {}".format(c1, c2))
        interface.draw_graphics(beta, c1, c2)
        return
    left, right = beta[0], beta[1]
    eps = (right - left) / 20
    delta = (right - left) / 1000
    while right - left > eps:
        print("left: {1}, right: {0}".format(right, left))
        x1 = (right + left - delta) / 2
        x2 = (right + left + delta) / 2
        y1 = func_to_min(manual_mode(a, b, c, d, x_0, y_0, x1, T, calculating_mod))
        y2 = func_to_min(manual_mode(a, b, c, d, x_0, y_0, x2, T, calculating_mod))
        if y1 >= y2:
            left = x1
        else:
            right = x2
    c1, c2 = manual_mode(a, b, c, d, x_0, y_0, (left + right) / 2, T, calculating_mod)
    print("final beta:", (left + right) / 2)
    print("c1: {}\n c2: {}".format(c1, c2))
    interface.draw_graphics((left + right) / 2, c1, c2)


if __name__ == '__main__':
    app = QApp5(sys.argv)
    window = interface.Window(main)
    sys.exit(app.exec_())

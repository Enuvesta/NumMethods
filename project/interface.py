import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
    QGridLayout, QApplication, QPushButton, QComboBox)


class Window(QWidget):

    p_edit_a = None
    p_edit_b = None
    s_edit = None
    z_edit = None
    x_0_edit = None
    y_0_edit = None
    beta_edit = None
    beta_edit_end = None
    T_edit = None
    info_text = None
    convertion_error_text = "Проверьте правильность ввода"
    open_error_text = "Проверьте файлы"
    calculating_mod = "Авто"

    def __init__(self, click_function):
        super().__init__()

        self.click_function = click_function
        self.initUI()


    def initUI(self):

        self.info_text = QLabel('')

        self.z_descr = QLabel('Введите параметры функции z = c * t + cos(t))')
        self.z_par_descr = QLabel('c: ')
        self.z_edit = QLineEdit()

        self.s_descr = QLabel('Введите параметры функции s = d * t + sin(t)')
        self.s_par_descr = QLabel('d: ')
        self.s_edit = QLineEdit()

        self.p_descr = QLabel('Введите параметры функции p = aw(b - w)')
        self.p_par_descr_a = QLabel('a: ')
        self.p_edit_a = QLineEdit()
        self.p_par_descr_b = QLabel('b: ')
        self.p_edit_b = QLineEdit()


        self.other_par_descr = QLabel("Введите начальные условия:")

        self.x_0_descr = QLabel("x0: ")
        self.x_0_edit = QLineEdit()

        self.y_0_descr = QLabel("y0: ")
        self.y_0_edit = QLineEdit()

        self.beta_descr = QLabel("beta: ")
        self.beta_edit = QLineEdit()
        self.beta_edit_end = QLineEdit()


        self.T_descr = QLabel("T: ")
        self.T_edit = QLineEdit()

    
        submit_btn = QPushButton("Решить", self)
        submit_btn.clicked.connect(self.on_button_click)

        comboBox = QComboBox(self)
        comboBox.addItem("Авто")
        comboBox.addItem("Ручной")
        comboBox.addItem("Авто+файл")
        comboBox.addItem("Ручной+файл")
        comboBox.activated[str].connect(self.update_calculating_mod)

        grid = QGridLayout()

        grid.addWidget(self.z_descr, 1, 0)
        grid.addWidget(self.z_par_descr, 2, 0)
        grid.addWidget(self.z_edit, 2, 1)

        grid.addWidget(self.s_descr, 3, 0)
        grid.addWidget(self.s_par_descr, 4, 0)
        grid.addWidget(self.s_edit, 4, 1)

        grid.addWidget(self.p_descr, 5, 0)
        grid.addWidget(self.p_par_descr_a, 6, 0)
        grid.addWidget(self.p_par_descr_b, 7, 0)
        grid.addWidget(self.p_edit_a, 6, 1)
        grid.addWidget(self.p_edit_b, 7, 1)

        grid.addWidget(self.other_par_descr, 8, 0)
        grid.addWidget(self.x_0_descr, 9, 0)
        grid.addWidget(self.y_0_descr, 10, 0)
        grid.addWidget(self.beta_descr, 11, 0)
        grid.addWidget(self.T_descr, 13, 0)
        grid.addWidget(self.x_0_edit, 9, 1)
        grid.addWidget(self.y_0_edit, 10, 1)
        grid.addWidget(self.beta_edit, 11, 1)
        grid.addWidget(self.beta_edit_end, 12, 1)
        grid.addWidget(self.T_edit, 13, 1)

        grid.addWidget(submit_btn, 14, 0)

        grid.addWidget(comboBox, 14, 1)

        grid.addWidget(self.info_text, 15, 0)

        self.setLayout(grid)

        self.setGeometry(500, 500, 400, 400)
        self.setWindowTitle('Численные методы')
        self.show()

    def on_button_click(self):
        if self.calculating_mod == "Ручной" or self.calculating_mod == "Авто":
            try:
                a = float(self.p_edit_a.text())
                b = float(self.p_edit_b.text())
                d = float(self.s_edit.text())
                c = float(self.z_edit.text())
                x_0 = float(self.x_0_edit.text())
                y_0 = float(self.y_0_edit.text())
                beta = float(self.beta_edit.text())
                T = float(self.T_edit.text())
            except:
                self.info_text.setText(self.convertion_error_text)
                return

            self.info_text.setText('')
            if self.calculating_mod == "Ручной":
                self.click_function(a, b, c, d, x_0, y_0, beta, T, self.calculating_mod)
            else:
                try:
                    beta_end = float(self.beta_edit_end.text())
                except:
                    self.info_text.setText(self.convertion_error_text)
                    return
                self.click_function(a, b, c, d, x_0, y_0, [beta, beta_end], T, self.calculating_mod)
        else:
            a = None
            b = None
            d = None
            c = None
            try:
                with open('tabulated_functions/p_func_tabulated', 'r') as k, \
                     open('tabulated_functions/z_func_tabulated', 'r') as l, \
                     open('tabulated_functions/s_func_tabulated', 'r') as m:
                        pass
            except:
                self.info_text.setText(self.open_error_text)
                return
            try:
                x_0 = float(self.x_0_edit.text())
                y_0 = float(self.y_0_edit.text())
                beta = float(self.beta_edit.text())
                T = float(self.T_edit.text())
            except:
                self.info_text.setText(self.convertion_error_text)
                return
            self.info_text.setText('')
            if self.calculating_mod == "Ручной+файл":
                self.click_function(a, b, c, d, x_0, y_0, beta, T, self.calculating_mod)
            else:
                try:
                    beta_end = float(self.beta_edit_end.text())
                except:
                    self.info_text.setText(self.convertion_error_text)
                    return
                self.click_function(a, b, c, d, x_0, y_0, [beta, beta_end], T, self.calculating_mod)

    def update_calculating_mod(self, mod_text):
        self.calculating_mod = mod_text
        if mod_text == "Ручной":
            self.p_par_descr_a.setHidden(False)
            self.p_par_descr_b.setHidden(False)
            self.p_descr.setHidden(False)
            self.z_descr.setHidden(False)
            self.z_par_descr.setHidden(False)
            self.s_descr.setHidden(False)
            self.s_par_descr.setHidden(False)
            self.p_edit_a.setHidden(False)
            self.p_edit_b.setHidden(False)
            self.z_edit.setHidden(False)
            self.s_edit.setHidden(False)
            self.beta_edit_end.setHidden(True)
        elif mod_text == "Авто":
            self.p_par_descr_a.setHidden(False)
            self.p_par_descr_b.setHidden(False)
            self.p_descr.setHidden(False)
            self.z_descr.setHidden(False)
            self.z_par_descr.setHidden(False)
            self.s_descr.setHidden(False)
            self.s_par_descr.setHidden(False)
            self.p_edit_a.setHidden(False)
            self.p_edit_b.setHidden(False)
            self.z_edit.setHidden(False)
            self.s_edit.setHidden(False)
            self.beta_edit_end.setHidden(False)
        else:
            if mod_text == "Ручной+файл":
                self.p_par_descr_a.setHidden(True)
                self.p_par_descr_b.setHidden(True)
                self.p_descr.setHidden(True)
                self.z_descr.setHidden(True)
                self.z_par_descr.setHidden(True)
                self.s_descr.setHidden(True)
                self.s_par_descr.setHidden(True)
                self.p_edit_a.setHidden(True)
                self.p_edit_b.setHidden(True)
                self.z_edit.setHidden(True)
                self.s_edit.setHidden(True)
                self.beta_edit_end.setHidden(True)
            else:
                self.p_par_descr_a.setHidden(True)
                self.p_par_descr_b.setHidden(True)
                self.p_descr.setHidden(True)
                self.z_descr.setHidden(True)
                self.z_par_descr.setHidden(True)
                self.s_descr.setHidden(True)
                self.s_par_descr.setHidden(True)
                self.p_edit_a.setHidden(True)
                self.p_edit_b.setHidden(True)
                self.z_edit.setHidden(True)
                self.s_edit.setHidden(True)
                self.beta_edit_end.setHidden(False)


def draw_graphics(beta, c1, c2):
    fig = plt.figure(1)
    fig.suptitle('beta = {}, c1 = {},  c2 = {}'.format(beta, c1, c2), fontsize=12,)
    t_x, x = [], []
    with open("x_answer.txt", 'r') as f:
        for line in f:
            data = line.split(' ')
            t_x.append(float(data[0]))
            x.append(float(data[1]))
    plt.subplot(231)
    plt.plot(t_x, x)
    plt.title('x(t)')

    t_s, t_s_interp, s, s_interp = [], [], [], []
    with open("tabulated_functions/s_func_tabulated", 'r') as f:
        for line in f:
            data = line.split(' ')
            t_s.append(float(data[0]))
            s.append(float(data[1]))
    with open("tabulated_functions/s_func_interp_tabulated", 'r') as f:
        for line in f:
            data = line.split(' ')
            t_s_interp.append(float(data[0]))
            s_interp.append(float(data[1]))
    plt.subplot(232)
    plt.plot(t_s, s, t_s_interp, s_interp)
    plt.title('S(t)')

    x_s = [x[i] - s[i] for i in range(0, len(t_x))]
    plt.subplot(233)
    plt.plot(t_x, x_s)
    plt.title('x(t) - S(t)')

    t_y, y, = [], []
    with open("y_answer.txt", 'r') as f:
        for line in f:
            data = line.split(' ')
            t_y.append(float(data[0]))
            y.append(float(data[1]))
    plt.subplot(234)
    plt.plot(t_y, y)
    plt.title('y(t)')

    t_p, t_p_interp, p, p_interp = [], [], [], []
    with open("tabulated_functions/p_func_tabulated", 'r') as f:
        for line in f:
            data = line.split(' ')
            t_p.append(float(data[0]))
            p.append(float(data[1]))
    with open("tabulated_functions/p_func_interp_tabulated", 'r') as f:
        for line in f:
            data = line.split(' ')
            t_p_interp.append(float(data[0]))
            p_interp.append(float(data[1]))
    plt.subplot(235)
    plt.plot(t_p, p, t_p_interp, p_interp)
    plt.title('p(w)')

    t_z, t_z_interp, z, z_interp = [], [], [], []
    with open("tabulated_functions/z_func_tabulated", 'r') as f:
        for line in f:
            data = line.split(' ')
            t_z.append(float(data[0]))
            z.append(float(data[1]))
    with open("tabulated_functions/z_func_interp_tabulated", 'r') as f:
        for line in f:
            data = line.split(' ')
            t_z_interp.append(float(data[0]))
            z_interp.append(float(data[1]))
    plt.subplot(236)
    plt.plot(t_z, z, t_z_interp, z_interp)
    plt.title('z(t)')


    plt.show()
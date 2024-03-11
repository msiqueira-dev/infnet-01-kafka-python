import matplotlib.pyplot as matplotlib

class GraphMatPlot:

    axes_total = None
    fig = None 
    axe = None
    def matplot_create_bargraph(self, array_x, array_x_subtitle, array_x_title, 
                                array_y, array_y_subtitle, array_y_title,
                                title, axe_num=None, show=None):
        try:
            title = str(title)
        except Exception:
            print("matplot_create_bargraph: varviavel title está vazio")
            return None
        try:
            if type(array_x) is not list:
                raise Exception("matplot_create_bargraph: variável array_x não é lista")
            if len(array_x) <= 0:
                raise Exception("matplot_create_bargraph: variável array_x não tem elementos suficientes")
        except Exception:
            print("matplot_create_bargraph: varviavel array_x está vazio ou não é uma lista válida")
            return None
        try:
            if type(array_y) is not list:
                raise Exception("matplot_create_bargraph: variável array_y não é lista")
            if len(array_y) <= 0:
                raise Exception("matplot_create_bargraph: variável array_y não tem elementos suficientes")
        except Exception:
            print("matplot_create_bargraph: varviavel array_y está vazio ou não é uma lista válida")
            return None
        if len(array_x) != len(array_y):
            print("matplot_create_bargraph: variáveis array_x e array_y não tem a mesma quantidade de elementos")
            return None
        array_x_bar_distance = []
        for count in range(len(array_x)):
            array_x_bar_distance.append(count)
        if axe_num is None or self.axe is None and self.axes_total > 1:
            self.fig, self.axe = matplotlib.subplots(layout='constrained')
            if array_x_title:
                matplotlib.xlabel(array_x_title)
            if array_y_title:
                matplotlib.ylabel(array_y_title)
            axe_num = 0
        if self.axes_total > 1:
            bar = self.axe[axe_num].bar(array_x_bar_distance, array_y, tick_label = array_x, width = 0.6, color = ['red', 'green'], label=array_y)
            self.axe[axe_num].bar_label(bar, padding=1)
        else:
            matplotlib.bar(array_x_bar_distance, array_y, tick_label = array_x, width = 0.6, color = ['red', 'green'], label=array_y)
            matplotlib.title = title
            matplotlib.xlabel(array_x_title, fontsize=8)
            matplotlib.ylabel(array_y_title, fontsize=8)
        if array_y_subtitle and self.axe:
            self.axe[axe_num].set_ylabel(array_y_subtitle)
        if array_x_subtitle and self.axe:
            self.axe[axe_num].set_xlabel(array_x_subtitle)
        if show is not None:
            matplotlib.show()

    def create_subplot(self):
        if self.axes_total > 1:
            self.fig, self.axe = matplotlib.subplots(self.axes_total, figsize=(9, 4.5), tight_layout=True)

    def show(self):
        matplotlib.show()
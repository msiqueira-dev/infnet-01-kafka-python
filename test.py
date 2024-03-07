import matplotlib.pyplot as matplotlib

class GraphMatplot:

    axes_total = None

    def matplot_create_bargraph(self, array_x, array_x_subtitle, array_x_title, 
                                array_y, array_y_subtitle, array_y_title,
                                title, axe=None, axe_num=None, show=None):
        """
            [PT]:
            [EN]:
        """
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
        if axe_num is None or axe is None:
            fig, axe = matplotlib.subplots(layout='constrained')
            if array_x_title:
                matplotlib.xlabel(array_x_title)
            if array_y_title:
                matplotlib.ylabel(array_y_title)
            axe_num = 0
        bar = axe[axe_num].bar(array_x_bar_distance, array_y, tick_label = array_x, width = 0.8, color = ['red', 'green'], label=[0, 1, 2, 3, 4, 5])
        axe[axe_num].bar_label(bar, padding=1)
        if array_y_subtitle:
            axe[axe_num].set_ylabel(array_y_subtitle)
        if array_x_subtitle:
            axe[axe_num].set_xlabel(array_x_subtitle)
        #matplotlib.title(title)
        if show is not None:
            matplotlib.show()

graph = GraphMatplot()
graph.axes_total = 2
fig, axes = matplotlib.subplots(graph.axes_total, figsize=(9, 4.5), tight_layout=True)
array_x = ['1999', '2000', '2001', '2002', '2003', '2004']
array_y = [1, 10, 4, 6, 8, 2]
title = f"Quantidade de disco lançados por ano com amostragem de {len(array_x)} dados"
bar1 = graph.matplot_create_bargraph(array_x, 'Ano', 'Ano', array_y, "Quantidade", 'Quantidade', title, axes, 0)
array_x = ['Infected', 'Astrix', 'Loud', 'GMS', 'Sun Project', 'Bliss']
array_y = [0, 10, 4, 6, 8, 1]
title = f"Quantidade de lançamentos por artistas com amostragem de {len(array_x)} dados"
bar2 = graph.matplot_create_bargraph(array_x, 'Ano', 'Ano', array_y, "Quantidade por artista", "Quantidade por artista", title, axes, 1)
matplotlib.show()



# fig.suptitle('Vertically stacked subplots')
# axes[0].bar([1,2,3,4,5,6], array_y, tick_label = array_x, width = 0.8, color = ['red', 'green'], label=[0, 1, 2, 3, 4, 5])
# axes[1].bar([1,2,3,4,5,6], array_y, tick_label = array_x, width = 0.8, color = ['red', 'green'], label=[0, 1, 2, 3, 4, 5])
# matplotlib.show()
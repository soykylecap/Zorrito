import matplotlib.pyplot as plt
import io
import urllib, base64
import numpy as np

def grafico_torta(labels, sizes):
        # # Datos para el gráfico
        # labels = ['Categoría 1', 'Categoría 2', 'Categoría 3']
        # sizes = [40, 30, 30]
        # colors = ['#ff9999', '#66b3ff', '#99ff99']
        #plt.style.use('_mpl-gallery-nogrid')

        colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(labels)))

        # Crear gráfico de torta
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=120, shadow=True, radius=3, wedgeprops={"linewidth": 1, "edgecolor": "white"})
        ax.axis('equal')  # Para que sea un círculo

        # Guardar el gráfico en un buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)

        return uri



category_names = ['Strongly disagree', 'Disagree',
                  'Neither agree nor disagree', 'Agree', 'Strongly agree']
results = {
    'Question 1': [10, 15, 17, 32, 26],
}


def survey(results, category_names):
    """
    Parameters
    ----------
    results : dict
        A mapping from question labels to a list of answers per category.
        It is assumed all lists contain the same number of entries and that
        it matches the length of *category_names*.
    category_names : list of str
        The category labels.
    """
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.colormaps['RdYlGn'](
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(9.2, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(labels, widths, left=starts, label=colname, height=0.5,  color=color)

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        ax.bar_label(rects, label_type='center', color=text_color)
    ax.legend(ncols=len(category_names), bbox_to_anchor=(0, 1), loc='lower left', fontsize='small')

    # Guardar el gráfico en un buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)





    return uri
#     return fig, ax 


# survey(results, category_names)
# plt.show()
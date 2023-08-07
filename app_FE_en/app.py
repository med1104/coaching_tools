import shinyswatch
from shiny import App, Inputs, Outputs, Session, render, ui
import matplotlib.pyplot as plt
import numpy as np
from shiny import App, render, ui
import textwrap

app_ui = ui.page_fluid(
    # Available themes:
    #  cerulean, cosmo, cyborg, darkly, flatly, journal, litera, lumen, lux,
    #  materia, minty, morph, pulse, quartz, sandstone, simplex, sketchy, slate,
    #  solar, spacelab, superhero, united, vapor, yeti, zephyr
    shinyswatch.theme.superhero(),
        ui.layout_sidebar(
            ui.panel_sidebar(
                ui.input_text("name", "", placeholder="Name"),
                ui.input_text("date", "", placeholder="Date"),
                ui.input_slider("FE1", "Activation", 0, 7, 2, step=0.1, ticks=False),
                ui.input_slider("FE2", "Focus", 0, 7, 2, step=0.1, ticks=False),
                ui.input_slider("FE3", "Sustained effort", 0, 7, 2, step=0.1, ticks=False),
                ui.input_slider("FE4", "Emotional Regulation ", 0, 7, 2, step=0.1, ticks=False),
                ui.input_slider("FE5", "Work memory", 0, 7, 2, step=0.1, ticks=False),
                ui.input_slider("FE6", "Action and Time", 0, 7, 2, step=0.1, ticks=False),
            ),
            ui.panel_main(
                ui.tags.h2("Wheel of Executive Functions"),
                ui.output_text_verbatim("name"),
                ui.output_text_verbatim("date"),
                ui.output_plot("plot"),
                ui.tags.h5("Developed by Marcos Espinel"),
                ui.tags.h6("med11.coaching@gmail.com"),
            ),
        ),
)


def server(input, output, session):

    @output
    @render.text
    def name():
        return f'{input.name()}'

    @output
    @render.text
    def date():
        return f'{input.date()}'
    
    @output
    @render.plot(alt="A plot")
    def plot():
        # Datos
        x = ["Activation",
     "Focus",
     "Sustained effort",
     "Emotional Regulation ",
     "Work memory",
     "Action and Time"]
        y = [input.FE1(), input.FE2(), input.FE3(),
             input.FE4(), input.FE5(), input.FE6()]
        
        # Colores de las barras
        colors = ['#F9837B', '#BEA819', '#19C14C', '#19C5CA', '#70A6FF', '#F673E6']
        
        # Crear la figura y los ejes en coordenadas polares
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        
        # Convertir los valores de x a radianes
        theta = np.linspace(0, 2 * np.pi, len(x), endpoint=False)
        
        # Calcular el ancho de las barras
        width = 2 * np.pi / len(x)
        
        # Crear el gráfico de barras en coordenadas polares con colores personalizados
        bars = ax.bar(theta, y, width=width, color=colors)
        
        # Configurar las etiquetas del eje radial
        ax.set_xticks(theta)
        
        # Dividir las etiquetas en múltiples líneas utilizando textwrap.wrap()
        wrapped_labels = [textwrap.wrap(label, 10) for label in x]
        # Unir las líneas con saltos de línea para mostrarlas en el gráfico
        wrapped_labels = ['\n'.join(lines) for lines in wrapped_labels]
        
        ax.set_xticklabels(wrapped_labels)
        
        # Mostrar la cuadrícula
        ax.yaxis.grid(True)
        ax.xaxis.grid(False)  # Ocultar las líneas de la cuadrícula del eje x
        
        # Ajustar el orden de dibujado de los elementos
        ax.set_axisbelow(True)
        
        # Ocultar los números del eje y
        ax.set_yticklabels([])
        
        # Ocultar la línea negra entre el gráfico y las etiquetas del eje x
        ax.spines['polar'].set_visible(False)
        
        # Crear la leyenda de colores con los nombres de las categorías y ajustar su posición
        legend_labels = [plt.Rectangle((0, 0), 1, 1, color=color) for color in colors]
        ax.legend(legend_labels, x, bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Calcular las coordenadas polares para la línea circular
        theta_line = np.linspace(0, 2 * np.pi, 100)
        r_line = np.ones_like(theta_line) * 5
        
        # Trazar la línea circular
        ax.plot(theta_line, r_line, color='black', linestyle='--', linewidth=1)
        
        # Establecer el rango fijo en el eje y
        ax.set_ylim(0, 7)
        
        # Redibujar la figura para rotar las etiquetas alrededor del gráfico
        plt.gcf().canvas.draw()
        
        # Obtener los ángulos de las etiquetas del eje angular en grados
        angles = np.rad2deg(theta)
        
        # Almacenar las etiquetas originales del eje angular
        labels = []
        
        # Vector de ángulos de rotación personalizados
        custom_angles = [0, 0, 0, 0, 0, 0]
        
        # Rotar las etiquetas según los ángulos personalizados
        for label, angle in zip(ax.get_xticklabels(), custom_angles):
            x, y = label.get_position()
            lab = ax.text(x, y - 0.15, label.get_text(), transform=label.get_transform(),
                          ha=label.get_ha(), va=label.get_va())
            lab.set_rotation(angle)
            labels.append(lab)
        
        # Ocultar las etiquetas originales del eje angular
        ax.set_xticklabels([])

app = App(app_ui, server, debug=True)
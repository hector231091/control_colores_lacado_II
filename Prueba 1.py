import datetime
import tkinter as tk
from csv import reader
from datetime import datetime
from tkinter import *
from tkinter import messagebox

import pandas as pd

from data import Record
from historical import HistoricalView
from input_entry import InputView

# Constantes
DATE_TIME_FORMAT = "%d/%m/%Y - %H:%M:%S"
REGISTRY_FILE_NAME = "Registro.csv"
COLOURS_FILE_NAME = "Colores.csv"
AVERAGE_CHANGE_TIME_NAME = "Tiempos de cambio.csv"
AMOUNT_OF_RECORDS_TO_SHOW = 6


def register_input(input_record):
    # Registra en el archivo.
    # TODO Falta ponerle en número del registro.
    # TODO Falta comprobar si está el archivo, en caso de que no esté, hacerlo nuevo poniéndole el encabezado
    #   (nº registro, colores, hora inicio cambio, hora inicio color, hora fin, bastidores y observaciones)
    # TODO Buscar la forma de registrar también la variable "efficiency_hangers" para poder tenerla en el registro.
    registry_file = open(REGISTRY_FILE_NAME, "a")
    registry_file.write(generate_input_to_register(input_record))
    registry_file.close()


def generate_input_to_register(input_record):
    return input_record.colour_code + ";" + \
           input_record.change_start_time + ";" + \
           input_record.colour_start_time + ";" + \
           input_record.colour_end_time + ";" + \
           input_record.hangers_amount + ";" + \
           input_record.observations + "\n"


def load_colours():
    with open(COLOURS_FILE_NAME, "r") as colour:
        lines = reader(colour)
        header = next(lines)

        colour_list = []

        # if header!=None:
        for line in colour:
            # lista_colores.append(linea)
            colour_list.append(line[0:8])
    colour_list.append("FIN")
    colour_list.append("OTRO")
    return colour_list


def load_average_colour_change_time():
    with open(AVERAGE_CHANGE_TIME_NAME, "r") as average_time:
        lines = reader(average_time)
        header = next(lines)

        list_average_change_time = []
        join_colour_1_and_2 = []

        for line in average_time:
            list_average_change_time.append(line[0:-1])
            c1 = line[0:8]
            inter_caracter = "-"
            c2 = line[9:17]
            # tendríamos que crear otra columna
            string_colours = c1 + inter_caracter + c2
            join_colour_1_and_2.append(string_colours)

    return join_colour_1_and_2, list_average_change_time


def get_change_colour_time_efficiency(color_1_and_2, change_times_list):
    num_rows, registry_file = load_history()

    last_colour = registry_file[0][num_rows - 1]
    penultimate_colour = registry_file[0][num_rows - 2]

    concatenate_two_colours = penultimate_colour + "-" + last_colour

    try:
        index_concatenate_colours = color_1_and_2.index(concatenate_two_colours)
        calculate_efficiency_change_colour(index_concatenate_colours)
        show_efficiency_change_colour.set(calculate_efficiency_change_colour(index_concatenate_colours))
    except ValueError:
        show_efficiency_change_colour.set("No hay datos\nanteriores con lo\nque comparar.")


def calculate_efficiency_change_colour(color_position_in_the_list):
    color_1_and_2, change_times_list = load_average_colour_change_time()

    num_rows, registry_file = load_history()

    average_time_of_colour_change = int((change_times_list[color_position_in_the_list][18:]))
    time1 = datetime.strptime(registry_file[1][num_rows - 1][:], DATE_TIME_FORMAT)
    time2 = datetime.strptime(registry_file[2][num_rows - 1][:], DATE_TIME_FORMAT)

    last_time_change = time2 - time1

    last_time_change_in_seconds = last_time_change.days * 24 * 3600 + last_time_change.seconds

    efficiency_change_last_colour = str(int((average_time_of_colour_change * 100) / last_time_change_in_seconds)) + " %"
    return efficiency_change_last_colour


def load_history():
    registry_file = pd.read_csv(REGISTRY_FILE_NAME, ";", header=None, na_filter=False)
    num_rows = len(registry_file[0])

    return num_rows, registry_file


def print_history():
    # Imprimir en el historial.
    # Pasamos el archivo de los registros a una matriz

    num_rows, registry_file = load_history()

    colour_1.set(registry_file[0][num_rows - 1])
    colour_2.set(registry_file[0][num_rows - 2])

    records = []
    for i in range(AMOUNT_OF_RECORDS_TO_SHOW):
        record = Record(num_rows - i,
                        registry_file[0][num_rows - i - 1],
                        registry_file[1][num_rows - i - 1][13:21],
                        registry_file[2][num_rows - i - 1][13:21],
                        registry_file[3][num_rows - i - 1][13:21],
                        registry_file[4][num_rows - i - 1],
                        registry_file[5][num_rows - i - 1])
        records.append(record)
    historical.update_historical(records)


def on_register_continue_button_click():
    # Si hay errores, mostramos un cuadro de diálogo al usuario y retornamos ejecución
    errors = inputView.is_input_valid()
    if len(errors) != 0:
        messagebox.showerror(message=errors[0], title="¡ERROR!")
        return -1

    input_record = inputView.get_input()
    inputView.reset(input_record.colour_end_time)
    get_colour_time_efficiency(input_record.colour_start_time,
                               input_record.colour_end_time,
                               input_record.hangers_amount)
    register_input(input_record)
    print_history()
    a, b = load_average_colour_change_time()
    get_change_colour_time_efficiency(a, b)


def on_register_end_button_click():
    # Si hay errores, mostramos un cuadro de diálogo al usuario y retornamos ejecución
    errors = inputView.is_input_valid()
    if len(errors) != 0:
        messagebox.showerror(message=errors[0], title="¡ERROR!")
        return

    input_record = inputView.get_input()
    inputView.reset(input_record.colour_end_time, True)
    get_colour_time_efficiency(input_record.colour_start_time,
                               input_record.colour_end_time,
                               input_record.hangers_amount)
    register_input(input_record)
    print_history()
    a, b = load_average_colour_change_time()
    get_change_colour_time_efficiency(a, b)

    register_button.config(state=DISABLED)
    register_end_button.config(state=DISABLED)
    register_close_button.config(state=NORMAL, bg="green")


def on_register_and_close_click():
    closing_message = messagebox.askquestion(message="¿Seguro que quieres registrar la línea y salir?",
                                             title="Cierre del programa")
    if closing_message == "yes":
        if on_register_continue_button_click() != -1:
            root.destroy()
        else:
            return


# def on_register_stop_button_click():
#     if on_register_continue_button_click() != -1:
#         on_close_click()
# Deben poder poner los minutos de descanso y que se les sume al tiempo del final del último color
# y se ponga en el tiempo inicia del cambio del siguiente color.


def get_colour_time_efficiency(start_datetime_as_string, end_datetime_as_string, amount_of_hangers_as_string):
    # Convierto los entrys en fechas para poder restarlas.
    start_colour = datetime.strptime(start_datetime_as_string, DATE_TIME_FORMAT)
    end_colour = datetime.strptime(end_datetime_as_string, DATE_TIME_FORMAT)

    # Evita calcular la eficiencia si el campo de bastidores está vacío
    if len(amount_of_hangers_as_string) == 0:
        return

    # Convertimos los bastidores a un entero.
    hangers = int(amount_of_hangers_as_string)

    # Restamos las dos fechas y lo pasamos a segundos.
    time_diff = end_colour - start_colour
    time_colour = time_diff.days * 24 * 3600 + time_diff.seconds

    # Comparamos el número de bastidores con los que podrían pasar con un rendimiento del 100%.
    ideal_hanger_passing_time = 10
    max_hangers_in_time_colour = time_colour / ideal_hanger_passing_time

    # Eficiencia del paso de bastidores de este color.
    efficiency_hangers = hangers / max_hangers_in_time_colour

    # round(number,1) sirve para redondear un flotante al decimal que queramos
    percentage_efficiency_hangers = str(int(efficiency_hangers * 100)) + " %"

    show_efficiency_hangers.set(percentage_efficiency_hangers)

    return efficiency_hangers


root = tk.Tk()
root.title("REGISTROS COLORES LACADO II")
# xroot = 790
# yroot = 630
root.geometry("1600x900")
# Para abrir la ventana maximizada
# root.state("zoomed")
# Adquirir las dimensiones de la pantalla
# xroot = root.winfo_screenwidth()
# yroot = root.winfo_screenheight()
# root.iconbitmap("Gaviota.ico")
# root.state("zoomed")

# Lugar en el que se debe hacer el gráfico
graphic = Frame(root, bg="WHITE", borderwidth=3, relief="groove")
graphic.place(relx=0.25, rely=0.655, relwidth=0.6, relheight=0.34)

# Variables a utilizar.
show_efficiency_hangers = StringVar()
colour_1 = StringVar()
colour_2 = StringVar()
show_efficiency_change_colour = StringVar()

# Variables de la posición de los cuadros de "Registrar" hacia abajo
x1 = 0.01
xclose = 0.85
yclose = 0.75

inputView = InputView(root, load_colours())
inputView.pack(fill="both")
inputView.place(relx=x1, rely=0.01, relwidth=0.975, relheigh=0.17)

# Botón Registrar y FIN
register_end_button = Button(root,
                             text="Registrar y FIN",
                             activebackground="green",
                             command=on_register_end_button_click,
                             state=NORMAL)
register_end_button.place(relx=0.072, rely=0.17, relwidth=0.2, relheigh=0.07)

# Botón Registrar y CONTINUAR
register_button = Button(root,
                         text="Registrar y CONTINUAR",
                         activebackground="green",
                         command=on_register_continue_button_click)
register_button.place(relx=0.39, rely=0.17, relwidth=0.2, relheigh=0.07)

# Botón Registrar y DESCANSO
# register_stop_button = Button(root,
#                               text="Registrar y DESCANSO",
#                               activebackground="green",
#                               command=on_register_stop_button_click,
#                               state=NORMAL)
# register_stop_button.place(relx=0.72, rely=0.17, relwidth=0.2, relheigh=0.07)

# Historial de los registros anteriores.
historical = HistoricalView(root, AMOUNT_OF_RECORDS_TO_SHOW)
historical.pack(fill="both")
historical.place(relx=x1, rely=0.25, relwidth=0.975, relheigh=0.42)
print_history()

# Botón para cerrar ventana. Ver si finalmente es necesario o no.
register_close_button = Button(root, text="Registrar y CERRAR",
                               activebackground="red",
                               command=on_register_and_close_click,
                               bg="grey",
                               fg="white",
                               font=("Comic Sans MS", 12),
                               state=DISABLED)
register_close_button.place(relx=xclose, rely=yclose, relwidth=0.135, relheigh=0.15)

# Mostrar el rendimiento del último color.
efficiency_colour_title = Label(root, text="Rendimiento del último color", relief="groove")
efficiency_colour_title.place(relx=x1, rely=0.655, relwidth=0.23, relheigh=0.05)

efficiency_colour_colour_1 = Label(root, text="Rendimiento del cambio de color",
                                   relief="groove",
                                   textvariable=colour_1,
                                   font=("Comic Sans MS", 15))
efficiency_colour_colour_1.place(relx=x1, rely=0.71, relwidth=0.1, relheigh=0.07)

efficiency_colour_result = Label(root, text="Rendimiento del cambio de color",
                                 relief="groove",
                                 background="white",
                                 textvariable=show_efficiency_hangers,
                                 font=("Comic Sans MS", 30))
efficiency_colour_result.place(relx=x1 + 0.1, rely=0.71, relwidth=0.13, relheigh=0.07)

efficiency_change_colour_title = Label(root, text="Rendimiento del último cambio de color", relief="groove")
efficiency_change_colour_title.place(relx=x1, rely=0.785, relwidth=0.23, relheigh=0.05)

efficiency_change_colour_1 = Label(root, text="Rendimiento del cambio de color",
                                   relief="groove",
                                   textvariable=colour_1,
                                   font=("Comic Sans MS", 15))
efficiency_change_colour_1.place(relx=x1, rely=0.84, relwidth=0.1, relheigh=0.06)

efficiency_change_colour_2 = Label(root, text="Rendimiento del cambio de color",
                                   relief="groove",
                                   textvariable=colour_2,
                                   font=("Comic Sans MS", 15))
efficiency_change_colour_2.place(relx=x1, rely=0.9, relwidth=0.1, relheigh=0.06)

efficiency_change_colour_result = Label(root, text="Rendimiento del cambio de color",
                                        relief="groove",
                                        background="white",
                                        textvariable=show_efficiency_change_colour,
                                        font=("Comic Sans MS", 15))
efficiency_change_colour_result.place(relx=x1 + 0.1, rely=0.84, relwidth=0.13, relheigh=0.12)

root.mainloop()

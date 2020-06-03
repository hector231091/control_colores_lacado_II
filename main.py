import tkinter as tk
from tkinter import *
from tkinter import messagebox

import pandas as pd

from data import Record
from historical import HistoricalView
from input_entry import InputView
from percentage import ShowPercentage

# Constantes
REGISTRY_FILE_NAME = "Registro.csv"
COLOURS_FILE_NAME = "Colores.csv"
AVERAGE_CHANGE_TIME_NAME = "Tiempos de cambio.csv"
AMOUNT_OF_RECORDS_TO_SHOW = 7


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
    colours_file = pd.read_csv(COLOURS_FILE_NAME, ";", header=None, na_filter=False)

    colour_map = {}
    for i in range(2, len(colours_file)):
        code = colours_file[0][i]
        name = colours_file[1][i]
        colour_map[code] = name

    colour_map["FIN"] = ["FIN"]
    colour_map["OTRO"] = ["OTRO"]

    return colour_map


def load_average_colour_change_time():
    average_time_file = pd.read_csv(AVERAGE_CHANGE_TIME_NAME, ";", header=None, na_filter=False)

    change_time_map = {}
    for i in range(2, len(average_time_file)):
        first_row_colour = average_time_file[0][i]
        separator = "-"
        second_row_colour = average_time_file[1][i]
        string_colours = first_row_colour + separator + second_row_colour  # e.g. "40100100-40100111"
        change_time_map[string_colours] = average_time_file[2][i]
    return change_time_map


def load_history():
    registry_file = pd.read_csv(REGISTRY_FILE_NAME, ";", header=None, na_filter=False)

    records = []
    registry_file_length = len(registry_file)
    for i in range(registry_file_length):
        record = Record(i,
                        registry_file[0][i],
                        registry_file[1][i],
                        registry_file[2][i],
                        registry_file[3][i],
                        registry_file[4][i],
                        registry_file[5][i])
        records.append(record)
    return records


def print_history():
    history_as_records = load_history()

    history_length = len(history_as_records)
    # Extraemos los últimos elementos de acuerdo a los especificado en AMOUNT_OF_RECORDS_TO_SHOW
    # e invertimos la lista para mostrar los últimos registros al principio de la lista
    records = history_as_records[history_length-AMOUNT_OF_RECORDS_TO_SHOW:history_length]
    records.reverse()

    historical.update_historical(records)


def on_register_continue_button_click():
    # Si hay errores, mostramos un cuadro de diálogo al usuario y retornamos ejecución
    errors = inputView.is_input_valid()
    if len(errors) != 0:
        messagebox.showerror(message=errors[0], title="¡ERROR!")
        return

    input_record = inputView.get_input()
    inputView.reset(input_record.colour_end_time)

    register_input(input_record)
    print_history()
    average_change_time_map = load_average_colour_change_time()
    history_as_records = load_history()
    percentage.update_change_colour_time_efficiency(average_change_time_map, history_as_records)
    percentage.update_colour_time_efficiency(input_record.colour_start_time,
                                             input_record.colour_end_time,
                                             input_record.hangers_amount)


def on_register_end_button_click():
    # Si hay errores, mostramos un cuadro de diálogo al usuario y retornamos ejecución
    errors = inputView.is_input_valid()
    if len(errors) != 0:
        messagebox.showerror(message=errors[0], title="¡ERROR!")
        return

    input_record = inputView.get_input()
    inputView.reset(input_record.colour_end_time, True)

    # Poner en el inicio hora lacado el tiempo que en inicio cambio de color.
    register_input(input_record)
    print_history()
    average_change_time_map = load_average_colour_change_time()
    history_as_records = load_history()
    percentage.update_change_colour_time_efficiency(average_change_time_map, history_as_records)
    percentage.update_colour_time_efficiency(input_record.colour_start_time,
                                             input_record.colour_end_time,
                                             input_record.hangers_amount)

    register_button.config(state=DISABLED)
    register_end_button.config(state=DISABLED)
    register_stop_button.config(state=DISABLED)
    register_close_button.config(state=NORMAL, bg="green")


def on_register_and_close_click():
    closing_message = messagebox.askquestion(message="¿Seguro que quieres registrar la línea y salir?",
                                             title="Cierre del programa")
    if closing_message == "yes":
        # Si hay errores, mostramos un cuadro de diálogo al usuario y retornamos ejecución
        errors = inputView.is_input_valid()
        if len(errors) != 0:
            messagebox.showerror(message=errors[0], title="¡ERROR!")
            return

        input_record = inputView.get_input()

        # Poner en el inicio hora lacado el tiempo que en inicio cambio de color.
        register_input(input_record)

        root.destroy()


def on_register_stop_button_click():
    # Si hay errores, mostramos un cuadro de diálogo al usuario y retornamos ejecución
    errors = inputView.is_input_valid()
    if len(errors) != 0:
        messagebox.showerror(message=errors[0], title="¡ERROR!")
        return

    input_record = inputView.get_input()
    inputView.reset_break(input_record.colour_end_time)

    register_input(input_record)
    print_history()
    average_change_time_map = load_average_colour_change_time()
    history_as_records = load_history()
    percentage.update_change_colour_time_efficiency(average_change_time_map, history_as_records)
    percentage.update_colour_time_efficiency(input_record.colour_start_time,
                                             input_record.colour_end_time,
                                             input_record.hangers_amount)


root = tk.Tk()
root.title("REGISTROS COLORES LACADO II")
root.geometry("1600x900")
# root.iconbitmap("Gaviota.ico")
# root.state("zoomed")

# Variables de la posición de los cuadros de "Registrar" hacia abajo
left_margin = 0.01

inputView = InputView(root, load_colours())
inputView.pack(fill="both")
inputView.place(relx=left_margin, rely=0.01, relwidth=0.975, relheigh=0.25)

# Botón Registrar y CONTINUAR
register_button = Button(root,
                         text="Registrar y CONTINUAR",
                         activebackground="green",
                         command=on_register_continue_button_click)
register_button.place(relx=0.39, rely=0.17, relwidth=0.2, relheigh=0.07)

# Historial de los registros anteriores
historical = HistoricalView(root, AMOUNT_OF_RECORDS_TO_SHOW)
historical.pack(fill="both")
historical.place(relx=left_margin, rely=0.25, relwidth=0.975, relheigh=0.5)
print_history()

percentage = ShowPercentage(root)
percentage.pack(fill="both")
percentage.place(relx=0.41, rely=0.75, relwidth=0.3, relheigh=0.3)

# Botón Registrar y DESCANSO
register_stop_button = Button(root,
                              text="Registrar y DESCANSO",
                              activebackground="green",
                              command=on_register_stop_button_click,
                              state=NORMAL)
register_stop_button.place(relx=0.01, rely=0.93, relwidth=0.2, relheigh=0.07)

# Botón Registrar y FIN
register_end_button = Button(root,
                             text="Registrar y FIN",
                             activebackground="green",
                             command=on_register_end_button_click,
                             state=NORMAL)
register_end_button.place(relx=0.8, rely=0.93, relwidth=0.2, relheigh=0.07)

# Botón Registrar y CERRAR
register_close_button = Button(root, text="Registrar y CERRAR",
                               activebackground="red",
                               command=on_register_and_close_click,
                               bg="grey",
                               fg="white",
                               font=("Comic Sans MS", 12),
                               state=DISABLED)
register_close_button.place(relx=0.6, rely=0.85, relwidth=0.135, relheigh=0.15)

root.mainloop()

# TODO Cosas para hacer:
#  1.- Crear un botón que abra una pantalla para poder registrar un nuevo color.
#      Tendrían que añadir él cógido del color y el nombre y al registrar que lo añada en los colores.
#  2.- Botón de "Registrar y DESCANSO":
#      i) Preguntar si van a continuar con el mismo color.
#         a) Respuesta = SÍ: Poner el color en la casilla y cuando pulsen el botón para poner la hora del cambio,
#                            que se ponga también la de inicio.
#         b) Respuesta = NO: Borrar formulario, como ahora, para que ellos empiecen igual que si comenzara un día nuevo.

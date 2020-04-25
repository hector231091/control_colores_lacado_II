import datetime
import tkinter as tk
from csv import reader
from datetime import datetime
from tkinter import *
from tkinter import messagebox

import pandas as pd
import tk_tools
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from matplotlib import style
import matplotlib.animation as animation

# Constantes
REGISTRY_FILE_NAME = "Registro.csv"
COLOURS_FILE_NAME = "Colores.csv"
AVERAGE_CHANGE_TIME_NAME = "Tiempos de cambio.csv"


def validate_colour(text, new_text):
	# Me funciona el LED (validate="focusout") o me funciona lo de que solo me deje poner 8 números (validate="key"), pero las dos cosas no...
    if colour_entry.get() in load_colours():
    	led_colour.to_green(on=True)
    else:
    	led_colour.to_red(on=True)

    #if len(new_text)>8:
    #	return False

    return text.isdecimal()


def on_change_start_time_click():
    now_change_start = datetime.now()
    date = now_change_start.strftime("%d/%m/%Y - %H:%M:%S")
    change_start_date_time.set(date)
    change_start_time_button.config(state=DISABLED)
    colour_start_time_button.config(state=NORMAL)
    colour_end_time_button.config(state=DISABLED)
    led_change_start_time.to_green(on=True)


def on_colour_start_time_click():
    now_colour_start = datetime.now()
    date = now_colour_start.strftime("%d/%m/%Y - %H:%M:%S")
    colour_start_date_time.set(date)
    change_start_time_button.config(state=DISABLED)
    colour_start_time_button.config(state=DISABLED)
    colour_end_time_button.config(state=NORMAL)
    led_colour_start_time.to_green(on=True)


def on_colour_end_time_click():
    now_colour_end = datetime.now()
    date = now_colour_end.strftime("%d/%m/%Y - %H:%M:%S")
    colour_end_date_time.set(date)
    change_start_time_button.config(state=DISABLED)
    colour_start_time_button.config(state=DISABLED)
    colour_end_time_button.config(state=DISABLED)
    led_colour_end_time.to_green(on=True)


def validate_hangers(text, new_text):
	# Me funciona el LED (validate="focusout") o me funciona lo de que solo me deje poner 8 números (validate="key"), pero las dos cosas no...
    if hangers_entry.get() == "0":
    	led_hangers.to_red(on=True)

    elif hangers_entry.get() != "" and len(new_text) <= 2:
    	led_hangers.to_green(on=True)

    else:
    	led_hangers.to_red(on=True)

    if len(new_text) > 2:
        return False
    return text.isdecimal()


def validate_observations(text, new_text):
	# Lo mismo que en los anteriores, me funciona todo por separado pero junto no.
    if colour_entry.get() == "OTRO":
    	if observations_entry.get() in load_colours():
    		led_observations.to_green(on=True)
    	else:
    		led_observation.to_blue(on=True)
    """	
    if observations_entry.get() in load_colours():
    	led_observations.to_green(on=True)
    else:
    	led_observations.to_red(on=True)
    """

    if len(new_text) > 50:
        return False


def generate_input_to_register():
    # Buscar la forma de registrar también la variable "efficiency_hangers" para poder tenerla en el registro.
    return colour_entry.get() + ";" + \
           change_start_date_time.get() + ";" + \
           colour_start_date_time.get() + ";" + \
           colour_end_date_time.get() + ";" + \
           hangers_entry.get() + ";" + \
           observations_entry.get() + "\n"


def register_input():
    # Registrar en el archivo. Falta ponerle en número del registro. Falta comprobar si está el archivo,
    # en caso de que no está hacerlo nuevo poniéndole el encabezado (nº registro, colores, hora inicio cambio,
    # hora inicio color, hora fin, bastidores y observaciones)
    registry_file = open(REGISTRY_FILE_NAME, "a")
    registry_file.write(generate_input_to_register())
    registry_file.close()


def clear_input():
    # Eliminar el texto de las casillas que se completan
    colour_entry.delete("0", "end")
    change_start_date_time.set("")
    colour_start_date_time.set("")
    colour_end_date_time.set("")
    hangers_entry.delete("0", "end")
    observations_entry.delete("0", "end")


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
            #tendríamos que crear otra columna 
            string_colours = c1+inter_caracter+c2
            join_colour_1_and_2.append(string_colours)

    return join_colour_1_and_2, list_average_change_time


def get_change_colour_time_efficiency(color_1_and_2, change_times_list):
    
    num_rows, registry_file = load_history()

    last_colour = registry_file[0][num_rows - 1]
    penultimate_colour = registry_file[0][num_rows - 2]

    concatenate_two_colours = penultimate_colour+"-"+last_colour

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
    time1 = datetime.strptime(registry_file[1][num_rows - 1][:], "%d/%m/%Y - %H:%M:%S")
    time2 = datetime.strptime(registry_file[2][num_rows - 1][:], "%d/%m/%Y - %H:%M:%S")

    last_time_change = time2 - time1

    last_time_change_in_seconds = last_time_change.days * 24 * 3600 + last_time_change.seconds

    efficiency_change_last_colour = str(int((average_time_of_colour_change * 100)/ last_time_change_in_seconds))+" %"
    return efficiency_change_last_colour


def load_history():
    registry_file = pd.read_csv(REGISTRY_FILE_NAME, ";", header=None)
    num_rows = len(registry_file[0])

    return num_rows, registry_file


def print_history():
    # Imprimir en el historial.
    # Pasamos el archivo de los registros a una matriz

    num_rows, registry_file = load_history()

    colour_1.set(registry_file[0][num_rows - 1])
    colour_2.set(registry_file[0][num_rows - 2])

    L00.set(num_rows)
    L01.set(registry_file[0][num_rows - 1])
    L02.set(registry_file[1][num_rows - 1][13:21])
    L03.set(registry_file[2][num_rows - 1][13:21])
    L04.set(registry_file[3][num_rows - 1][13:21])
    L05.set(registry_file[4][num_rows - 1])
    L06.set(registry_file[5][num_rows - 1])

    L10.set(num_rows - 1)
    L11.set(registry_file[0][num_rows - 2])
    L12.set(registry_file[1][num_rows - 2][13:21])
    L13.set(registry_file[2][num_rows - 2][13:21])
    L14.set(registry_file[3][num_rows - 2][13:21])
    L15.set(registry_file[4][num_rows - 2])
    L16.set(registry_file[5][num_rows - 2])

    L20.set(num_rows - 2)
    L21.set(registry_file[0][num_rows - 3])
    L22.set(registry_file[1][num_rows - 3][13:21])
    L23.set(registry_file[2][num_rows - 3][13:21])
    L24.set(registry_file[3][num_rows - 3][13:21])
    L25.set(registry_file[4][num_rows - 3])
    L26.set(registry_file[5][num_rows - 3])

    L30.set(num_rows - 3)
    L31.set(registry_file[0][num_rows - 4])
    L32.set(registry_file[1][num_rows - 4][13:21])
    L33.set(registry_file[2][num_rows - 4][13:21])
    L34.set(registry_file[3][num_rows - 4][13:21])
    L35.set(registry_file[4][num_rows - 4])
    L36.set(registry_file[5][num_rows - 4])

    L40.set(num_rows - 4)
    L41.set(registry_file[0][num_rows - 5])
    L42.set(registry_file[1][num_rows - 5][13:21])
    L43.set(registry_file[2][num_rows - 5][13:21])
    L44.set(registry_file[3][num_rows - 5][13:21])
    L45.set(registry_file[4][num_rows - 5])
    L46.set(registry_file[5][num_rows - 5])

    L50.set(num_rows - 5)
    L51.set(registry_file[0][num_rows - 6])
    L52.set(registry_file[1][num_rows - 6][13:21])
    L53.set(registry_file[2][num_rows - 6][13:21])
    L54.set(registry_file[3][num_rows - 6][13:21])
    L55.set(registry_file[4][num_rows - 6])
    L56.set(registry_file[5][num_rows - 6])

    L60.set(num_rows - 6)
    L61.set(registry_file[0][num_rows - 7])
    L62.set(registry_file[1][num_rows - 7][13:21])
    L63.set(registry_file[2][num_rows - 7][13:21])
    L64.set(registry_file[3][num_rows - 7][13:21])
    L65.set(registry_file[4][num_rows - 7])
    L66.set(registry_file[5][num_rows - 7])

    """#L00.set(num_registro) No tengo ni idea de cómo hacer esto...
        L01.set(colour_2.get())
        L02.set(change_start_date_time.get())
        L03.set(colour_start_date_time.get())
        L04.set(colour_end_date_time.get())
        L05.set(hangers_2.get())
        L06.set(observations_2.get())"""


def on_register_continue_button_click():
    next_change_start_date_time = colour_end_date_time.get()
    # Cargar todos los colores en una lista.
    colour_list = load_colours()

    is_input_valid = str(colour_entry.get()[0:9]) in colour_list and \
                     colour_entry.get() != "" and \
                     change_start_date_time.get() != "" and \
                     colour_start_date_time.get() != "" and \
                     colour_end_date_time.get() != "" \
                     and hangers_entry.get() != ""

    is_any_input_empty = colour_entry.get() == "" or \
                         change_start_date_time.get() == "" or \
                         colour_start_date_time.get() == "" or \
                         colour_end_date_time.get() == "" or \
                         hangers_entry.get() == ""

    # TODO: la validación hay que re-comprobarla para no dejar ningún caso atrás
    if str(colour_entry.get()[0:9]) not in colour_list:
        if colour_entry.get() == "OTRO" and observations_entry.get() == "":
            messagebox.showerror(message="Si no me pones el color... ponlo en las observaciones :)",
                                 title="Falta poner el color en las observaciones")
            return -1

        else:
            messagebox.showerror(message="El color que se ha introducido no existe.\n\n"
                                         "Por favor, introduce un color válido y vuelve a registrar.",
                                 title="Color inválido")
            return -1

    elif is_any_input_empty:
        messagebox.showerror(message="Faltan algún dato por completar",
                             title="Algo no me cuadra...")
        return -1

    elif hangers_entry.get() == "0":
        messagebox.showerror(message="No pueden haber 0 bastidores.",
                             title="Error de número de bastidores")
        return -1

    elif is_input_valid:
        get_colour_time_efficiency(colour_start_date_time, colour_end_date_time, hangers_entry)
        register_input()
        reset_buttons()
        reset_leds()
        clear_input()
        print_history()
        change_start_date_time.set(next_change_start_date_time)
        a, b = load_average_colour_change_time()
        get_change_colour_time_efficiency(a, b)


def reset_buttons():
    change_start_time_button.config(state=DISABLED)
    colour_start_time_button.config(state=NORMAL)
    colour_end_time_button.config(state=DISABLED)


def reset_leds():
    led_colour.to_red(on=True)
    led_change_start_time.to_green(on=True)
    led_colour_start_time.to_red(on=True)
    led_colour_end_time.to_red(on=True)
    led_hangers.to_red(on=True)
    led_observations.to_red(on=True)


def on_register_end_button_click():
	if 	on_register_continue_button_click() != -1:
		print("Caso 1")
		final_colour.set("FIN")
		led_colour.to_green(on=True)
		register_button.config(state=DISABLED)
		register_stop_button.config(state=DISABLED)
		register_end_button.config(state=DISABLED)
		close.config(state=NORMAL)
		close.config(bg="green")
	else:
		return


def on_register_stop_button_click():
    if on_register_continue_button_click() != 1:
    	on_close_click()
    else:
    	return

    # Deben poder poner los minutos de descanso y que se les sume al tiempo del final del últimocolor y se ponga en el tiempo inicia del cambio del siguiente color.


def get_colour_time_efficiency(start_datetime_as_string, end_datetime_as_string, amount_of_hangers_as_string):
    # Convierto los entrys en fechas para poder restarlas.
    start_colour = datetime.strptime(start_datetime_as_string.get(), "%d/%m/%Y - %H:%M:%S")
    end_colour = datetime.strptime(end_datetime_as_string.get(), "%d/%m/%Y - %H:%M:%S")

    # Convertimos los bastidores a un entero.
    hangers = int(amount_of_hangers_as_string.get())

    # Restamos las dos fechas y lo pasamos a segundos.
    time_diff = end_colour - start_colour
    time_colour = time_diff.days * 24 * 3600 + time_diff.seconds

    # Comparamos el número de bastidores con los que podrían pasar con un rendimiento del 100%.
    ideal_hanger_passing_time = 10
    max_hangers_in_time_colour = time_colour / ideal_hanger_passing_time

    # Eficiencia del paso de bastidores de este color.
    efficiency_hangers = hangers / max_hangers_in_time_colour

    # round(number,1) sirve para redondear un flotante al decimal que queramos
    percentage_efficiency_hangers = str(int(efficiency_hangers*100))+" %"

    show_efficiency_hangers.set(percentage_efficiency_hangers)

    return efficiency_hangers


def on_close_click():
    closing_message = messagebox.askquestion(message="¿Seguro que quieres salir?",
    										 title="Cierre del programa")
    if closing_message == "yes":
        root.destroy()
    else:
        continue_or_not = messagebox.askquestion(message="Si no quieres cerrar\n¿Quieres registrar y continuar con otro color?",
    						   title="Aclárate!, ¿Qué quieres hacer?")
        if continue_or_not == "No":
        	messagebox.showinfo(message="Entonces es que no quieres irte. Nos vemos otro día",
    						   title="Hasta pronto")
        	root.destroy()
        else:
        	messagebox.showinfo(message="Bueno, pues entonces registramos la línea\nque has puesto y continuamos con otro color",
    						   title="Venga, vamos a continuar")
        	if on_register_continue_button_click() != 1:
        		on_close_click()
        	else:
        		return

root = tk.Tk()
root.title("REGISTROS COLORES LACADO II")
#xroot = 790
#yroot = 630
#root.geometry(str(xroot) + "x" + str(yroot))
# Para abrir la ventana maximizada
# root.state("zoomed")
# Adquirir las dimensiones de la pantalla
# xroot = root.winfo_screenwidth()
# yroot = root.winfo_screenheight()
# root.iconbitmap("Gaviota.ico")
root.state("zoomed")

# Lugar en el que se debe hacer el gráfico
graphic = Frame(root, bg="WHITE", borderwidth=3, relief="groove")
graphic.place(relx=0.25, rely=0.655, relwidth=0.6, relheight=0.34)


led_colour = tk_tools.Led(root, size=30)  # No sé cómo hacerlo funcionar.
led_colour.place(relx=0.07, rely=0.1)
led_colour.to_red(on=True)

led_change_start_time = tk_tools.Led(root, size=30)
led_change_start_time.place(relx=0.24, rely=0.1)
led_change_start_time.to_red(on=True)

led_colour_start_time = tk_tools.Led(root, size=30)
led_colour_start_time.place(relx=0.4, rely=0.1)
led_colour_start_time.to_red(on=True)

led_colour_end_time = tk_tools.Led(root, size=30)
led_colour_end_time.place(relx=0.56, rely=0.1)
led_colour_end_time.to_red(on=True)

led_hangers = tk_tools.Led(root, size=30)
led_hangers.place(relx=0.73, rely=0.1)
led_hangers.to_red(on=True)

led_observations = tk_tools.Led(root, size=30)  # No sé cómo hacerlo funcionar.
led_observations.place(relx=0.9, rely=0.1)
led_observations.to_red(on=True)

# Variables a utilizar.
final_colour = StringVar()
change_start_date_time = StringVar()
colour_start_date_time = StringVar()
colour_end_date_time = StringVar()
final_observation = StringVar()
show_efficiency_hangers = StringVar()
colour_1 = StringVar()
colour_2 = StringVar()
show_efficiency_change_colour = StringVar()

# Definir las variables de cada una de las celdas del historial
L00 = StringVar()
L01 = StringVar()
L02 = StringVar()
L03 = StringVar()
L04 = StringVar()
L05 = StringVar()
L06 = StringVar()

L10 = StringVar()
L11 = StringVar()
L12 = StringVar()
L13 = StringVar()
L14 = StringVar()
L15 = StringVar()
L16 = StringVar()

L20 = StringVar()
L21 = StringVar()
L22 = StringVar()
L23 = StringVar()
L24 = StringVar()
L25 = StringVar()
L26 = StringVar()

L30 = StringVar()
L31 = StringVar()
L32 = StringVar()
L33 = StringVar()
L34 = StringVar()
L35 = StringVar()
L36 = StringVar()

L40 = StringVar()
L41 = StringVar()
L42 = StringVar()
L43 = StringVar()
L44 = StringVar()
L45 = StringVar()
L46 = StringVar()

L50 = StringVar()
L51 = StringVar()
L52 = StringVar()
L53 = StringVar()
L54 = StringVar()
L55 = StringVar()
L56 = StringVar()

L60 = StringVar()
L61 = StringVar()
L62 = StringVar()
L63 = StringVar()
L64 = StringVar()
L65 = StringVar()
L66 = StringVar()

# Variables de la posición de los cuadros de "Registrar" hacia abajo
x1 = 0.01
x2 = x1 + 0.075
x3 = x2 + 0.1524
x4 = x3 + 0.1524
x5 = x4 + 0.1524
x6 = x5 + 0.1524
x7 = x6 + 0.1524
xclose = 0.85

y1 = 0.35
y2 = y1 + 0.05
y3 = y2 + 0.05
y4 = y3 + 0.05
y5 = y4 + 0.05
y6 = y5 + 0.05
y7 = y6 + 0.05
yclose = 0.75

# Registro de datos.
colour_label = Label(root, text="Color", anchor="center", relief="groove")
colour_label.place(relx=0.01, rely=0.01, relwidth=0.155, relheigh=0.045)
colour_entry = Entry(root,
                     justify="center",
                     validate="focusout",
                     validatecommand=(root.register(validate_colour), "%S", "%P"),
                     textvariable=final_colour)
colour_entry.place(relx=0.01, rely=0.06, relwidth=0.155, relheigh=0.045)

change_start_time_button = Button(root, text="Hora inicio cambio", state=NORMAL, command=on_change_start_time_click)
change_start_time_button.place(relx=0.175, rely=0.01, relwidth=0.155, relheigh=0.045)
change_start_time_label = Label(root, background="white", textvariable=change_start_date_time)
change_start_time_label.place(relx=0.175, rely=0.06, relwidth=0.155, relheigh=0.045)

colour_start_time_button = Button(root, text="Hora inicio color", state=DISABLED, command=on_colour_start_time_click)
colour_start_time_button.place(relx=0.34, rely=0.01, relwidth=0.155, relheigh=0.045)
colour_start_time_label = Label(root, background="white", textvariable=colour_start_date_time)
colour_start_time_label.place(relx=0.34, rely=0.06, relwidth=0.155, relheigh=0.045)

colour_end_time_button = Button(root, text="Hora final color", state=DISABLED, command=on_colour_end_time_click)
colour_end_time_button.place(relx=0.505, rely=0.01, relwidth=0.155, relheigh=0.045)
colour_end_time_label = Label(root, background="white", textvariable=colour_end_date_time)
colour_end_time_label.place(relx=0.505, rely=0.06, relwidth=0.155, relheigh=0.045)

hangers_label = Label(root, text="Nº de bastidores", anchor="center", relief="groove")
hangers_label.place(relx=0.67, rely=0.01, relwidth=0.155, relheigh=0.045)
hangers_entry = Entry(root,
                      justify="center",
                      validate="focusout",
                      validatecommand=(root.register(validate_hangers), "%S", "%P"))
hangers_entry.place(relx=0.67, rely=0.06, relwidth=0.155, relheigh=0.045)

observations_label = Label(root, text="Observaciones", anchor="center", relief="groove")
observations_label.place(relx=0.835, rely=0.01, relwidth=0.155, relheigh=0.045)
observations_entry = Entry(root,
                           justify="center",
                           validate="focusout",
                           validatecommand=(root.register(validate_observations), "%S", "%P"),
                           textvariable=final_observation)
observations_entry.place(relx=0.835, rely=0.06, relwidth=0.155, relheigh=0.045)

# Botón Registrar y FIN
register_end_button = Button(root,
                             text="Registrar y FIN",
                             activebackground="green",
                             command=on_register_end_button_click, 
                             state=NORMAL)
register_end_button.place(relx=0.072, rely=0.17, relwidth=0.2, relheigh=0.07)

# Botón Registrar
register_button = Button(root, text="Registrar y CONTINUAR", 
							   activebackground="green",
							   command=on_register_continue_button_click)
register_button.place(relx=0.39, rely=0.17, relwidth=0.2, relheigh=0.07)

# Botón Registrar y DESCANSO
register_stop_button = Button(root, text="Registrar y DESCANSO",
									activebackground="green", 
									command=on_register_stop_button_click,
									state=NORMAL)
register_stop_button.place(relx=0.72, rely=0.17, relwidth=0.2, relheigh=0.07)

# Historial de los registros anteriores.
historical_title_label = Label(root, text="Historial de Registros", relief="sunken", background="cyan")
historical_title_label.place(relx=x1, rely=0.25, relwidth=0.975, relheigh=0.042)

registry_number_title_label = Label(root, text="Nº", relief="groove", background="cyan")
registry_number_title_label.place(relx=x1, rely=0.3, relwidth=0.06329, relheigh=0.0476)

colour_title_label = Label(root, text="Color", relief="groove", background="cyan")
colour_title_label.place(relx=x2, rely=0.3, relwidth=0.1392, relheigh=0.0476)

change_start_time_title_label = Label(root, text="Hora inicio cambio", relief="groove", background="cyan")
change_start_time_title_label.place(relx=x3, rely=0.3, relwidth=0.1392, relheigh=0.0476)

colour_start_time_title_label = Label(root, text="Hora inicio color", relief="groove", background="cyan")
colour_start_time_title_label.place(relx=x4, rely=0.3, relwidth=0.1392, relheigh=0.0476)

colour_end_time_title_label = Label(root, text="Hora final color", relief="groove", background="cyan")
colour_end_time_title_label.place(relx=x5, rely=0.3, relwidth=0.1392, relheigh=0.0476)

hangers_title_label = Label(root, text="Nº de bastidores", relief="groove", background="cyan")
hangers_title_label.place(relx=x6, rely=0.3, relwidth=0.1392,relheigh=0.0476)

observations_title_label = Label(root, text="Observaciones", relief="groove", background="cyan")
observations_title_label.place(relx=x7, rely=0.3, relwidth=0.1392, relheigh=0.0476)

# ---------------------------------------------------------------------------

L_0_0 = Label(root, background="white", textvariable=L00, relief="groove")
L_0_0.place(relx=0.01, rely=0.35, relwidth=0.06329, relheigh=0.0476)

L_0_1 = Label(root, background="white", textvariable=L01, relief="groove")
L_0_1.place(relx=x2, rely=y1, relwidth=0.1392, relheigh=0.0476)

L_0_2 = Label(root, background="white", textvariable=L02, relief="groove")
L_0_2.place(relx=x3, rely=y1, relwidth=0.1392, relheigh=0.0476)

L_0_3 = Label(root, background="white", textvariable=L03, relief="groove")
L_0_3.place(relx=x4, rely=y1, relwidth=0.1392, relheigh=0.0476)

L_0_4 = Label(root, background="white", textvariable=L04, relief="groove")
L_0_4.place(relx=x5, rely=y1, relwidth=0.1392, relheigh=0.0476)

L_0_5 = Label(root, background="white", textvariable=L05, relief="groove")
L_0_5.place(relx=x6, rely=y1, relwidth=0.1392, relheigh=0.0476)

L_0_6 = Label(root, background="white", textvariable=L06, relief="groove")
L_0_6.place(relx=x7, rely=y1, relwidth=0.1392, relheigh=0.0476)

# ---------------------------------------------------------------------------

L_1_0 = Label(root, background="white", textvariable=L10, relief="groove")
L_1_0.place(relx=0.01, rely=0.4, relwidth=0.06329, relheigh=0.0476)

L_1_1 = Label(root, background="white", textvariable=L11, relief="groove")
L_1_1.place(relx=x2, rely=y2, relwidth=0.1392, relheigh=0.0476)

L_1_2 = Label(root, background="white", textvariable=L12, relief="groove")
L_1_2.place(relx=x3, rely=y2, relwidth=0.1392, relheigh=0.0476)

L_1_3 = Label(root, background="white", textvariable=L13, relief="groove")
L_1_3.place(relx=x4, rely=y2, relwidth=0.1392, relheigh=0.0476)

L_1_4 = Label(root, background="white", textvariable=L14, relief="groove")
L_1_4.place(relx=x5, rely=y2, relwidth=0.1392, relheigh=0.0476)

L_1_5 = Label(root, background="white", textvariable=L15, relief="groove")
L_1_5.place(relx=x6, rely=y2, relwidth=0.1392, relheigh=0.0476)

L_1_6 = Label(root, background="white", textvariable=L16, relief="groove")
L_1_6.place(relx=x7, rely=y2, relwidth=0.1392, relheigh=0.0476)

# ---------------------------------------------------------------------------

L_2_0 = Label(root, background="white", textvariable=L20, relief="groove")
L_2_0.place(relx=0.01, rely=0.45, relwidth=0.06329, relheigh=0.0476)

L_2_1 = Label(root, background="white", textvariable=L21, relief="groove")
L_2_1.place(relx=x2, rely=y3, relwidth=0.1392, relheigh=0.0476)

L_2_2 = Label(root, background="white", textvariable=L22, relief="groove")
L_2_2.place(relx=x3, rely=y3, relwidth=0.1392, relheigh=0.0476)

L_2_3 = Label(root, background="white", textvariable=L23, relief="groove")
L_2_3.place(relx=x4, rely=y3, relwidth=0.1392, relheigh=0.0476)

L_2_4 = Label(root, background="white", textvariable=L24, relief="groove")
L_2_4.place(relx=x5, rely=y3, relwidth=0.1392, relheigh=0.0476)

L_2_5 = Label(root, background="white", textvariable=L25, relief="groove")
L_2_5.place(relx=x6, rely=y3, relwidth=0.1392, relheigh=0.0476)

L_2_6 = Label(root, background="white", textvariable=L26, relief="groove")
L_2_6.place(relx=x7, rely=y3, relwidth=0.1392, relheigh=0.0476)

# ---------------------------------------------------------------------------

L_3_0 = Label(root, background="white", textvariable=L30, relief="groove")
L_3_0.place(relx=0.01, rely=0.5, relwidth=0.06329, relheigh=0.0476)

L_3_1 = Label(root, background="white", textvariable=L31, relief="groove")
L_3_1.place(relx=x2, rely=y4, relwidth=0.1392, relheigh=0.0476)

L_3_2 = Label(root, background="white", textvariable=L32, relief="groove")
L_3_2.place(relx=x3, rely=y4, relwidth=0.1392, relheigh=0.0476)

L_3_3 = Label(root, background="white", textvariable=L33, relief="groove")
L_3_3.place(relx=x4, rely=y4, relwidth=0.1392, relheigh=0.0476)

L_3_4 = Label(root, background="white", textvariable=L34, relief="groove")
L_3_4.place(relx=x5, rely=y4, relwidth=0.1392, relheigh=0.0476)

L_3_5 = Label(root, background="white", textvariable=L35, relief="groove")
L_3_5.place(relx=x6, rely=y4, relwidth=0.1392, relheigh=0.0476)

L_3_6 = Label(root, background="white", textvariable=L36, relief="groove")
L_3_6.place(relx=x7, rely=y4, relwidth=0.1392, relheigh=0.0476)

# ---------------------------------------------------------------------------

L_4_0 = Label(root, background="white", textvariable=L40, relief="groove")
L_4_0.place(relx=0.01, rely=0.55, relwidth=0.06329, relheigh=0.0476)

L_4_1 = Label(root, background="white", textvariable=L41, relief="groove")
L_4_1.place(relx=x2, rely=y5, relwidth=0.1392, relheigh=0.0476)

L_4_2 = Label(root, background="white", textvariable=L42, relief="groove")
L_4_2.place(relx=x3, rely=y5, relwidth=0.1392, relheigh=0.0476)

L_4_3 = Label(root, background="white", textvariable=L43, relief="groove")
L_4_3.place(relx=x4, rely=y5, relwidth=0.1392, relheigh=0.0476)

L_4_4 = Label(root, background="white", textvariable=L44, relief="groove")
L_4_4.place(relx=x5, rely=y5, relwidth=0.1392, relheigh=0.0476)

L_4_5 = Label(root, background="white", textvariable=L45, relief="groove")
L_4_5.place(relx=x6, rely=y5, relwidth=0.1392, relheigh=0.0476)

L_4_6 = Label(root, background="white", textvariable=L46, relief="groove")
L_4_6.place(relx=x7, rely=y5, relwidth=0.1392, relheigh=0.0476)

# ---------------------------------------------------------------------------

L_5_0 = Label(root, background="white", textvariable=L50, relief="groove")
L_5_0.place(relx=0.01, rely=0.6, relwidth=0.06329, relheigh=0.0476)

L_5_1 = Label(root, background="white", textvariable=L51, relief="groove")
L_5_1.place(relx=x2, rely=y6, relwidth=0.1392, relheigh=0.0476)

L_5_2 = Label(root, background="white", textvariable=L52, relief="groove")
L_5_2.place(relx=x3, rely=y6, relwidth=0.1392, relheigh=0.0476)

L_5_3 = Label(root, background="white", textvariable=L53, relief="groove")
L_5_3.place(relx=x4, rely=y6, relwidth=0.1392, relheigh=0.0476)

L_5_4 = Label(root, background="white", textvariable=L54, relief="groove")
L_5_4.place(relx=x5, rely=y6, relwidth=0.1392, relheigh=0.0476)

L_5_5 = Label(root, background="white", textvariable=L55, relief="groove")
L_5_5.place(relx=x6, rely=y6, relwidth=0.1392, relheigh=0.0476)

L_5_6 = Label(root, background="white", textvariable=L56, relief="groove")
L_5_6.place(relx=x7, rely=y6, relwidth=0.1392, relheigh=0.0476)

# Botón para cerrar ventana. Ver si finalmente es necesario o no.
close = Button(root, text="Registrar y CERRAR",
					 activebackground="red",
					 command=on_close_click,
					 bg="grey",
					 fg="white",
					 font=("Comic Sans MS", 12), state=DISABLED)
# close.place(relx=xcerrar/xroot, y=yclose, relwidth=200/xroot, heigh=50)
close.place(relx=xclose, rely=yclose, relwidth=0.135, relheigh=0.15)

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
efficiency_colour_result.place(relx=x1+0.1, rely=0.71, relwidth=0.13, relheigh=0.07)

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
efficiency_change_colour_result.place(relx=x1+0.1, rely=0.84, relwidth=0.13, relheigh=0.12)

root.mainloop()
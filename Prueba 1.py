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

# Constantes
REGISTRY_FILE_NAME = "Registro.csv"
COLOURS_FILE_NAME = "Colores.csv"


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
    # Añadir la palabra FIN a la lista de los colores
    colour_list.append("FIN")
    colour_list.append("OTRO")
    return colour_list


def print_history():
    # Imprimir en el historial.
    # Pasamos el archivo de los registros a una matriz
    registry_file = pd.read_csv(REGISTRY_FILE_NAME, ";", header=None)
    num_rows = len(registry_file[0])

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
            return

        else:
            messagebox.showerror(message="El color que se ha introducido no existe.\n\n"
                                         "Por favor, introduce un color válido y vuelve a registrar.",
                                 title="Color inválido")
            return

    elif is_any_input_empty:
        messagebox.showerror(message="Faltan algún dato por completar",
                             title="Algo no me cuadra...")
        return

    elif hangers_entry.get() == "0":
    	messagebox.showerror(message="No pueden haber 0 bastidores.",
                             title="Error de número de bastidores")
    	return

    elif is_input_valid:
        get_colour_time_efficiency(colour_start_date_time, colour_end_date_time, hangers_entry)
        register_input()
        reset_buttons()
        reset_leds()
        clear_input()
        print_history()

    change_start_date_time.set(next_change_start_date_time)


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
    on_register_continue_button_click  # Si la pongo en la línea 214 hace justo lo que quiero pero no con el botón que quiero, en cambio si la pongo en la línea 220 no me hace nada...tiene que ver con el return??
    final_colour.set("FIN")


def on_register_stop_button_click():
    on_register_button_click

    # Deben poder poner los minutos de descanso y que se les sume al tiempo del final del últimocolor y se ponga en el tiempo inicia del cambio del siguiente color.


# Rendimiento de los bastidores
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

    # print(efficiency_hangers*100,"%")

    return efficiency_hangers


def on_close_click():
    if colour_entry.get() == "" and change_start_date_time.get() == "" and colour_start_date_time.get() == "" and colour_end_date_time.get() == "" and hangers_entry.get() == "" and observations_entry.get() == "":
        closing_message = messagebox.askquestion(
            message="¿Seguro que quieres salir?",
            title="Cierre del programa")
        if closing_message == "yes":
            root.destroy()
        else:
            messagebox.showinfo(message="Ya te querías ir eh...venga, a currar!!")
    else:
        messagebox.showerror(
            message="Para poder salir debes registrar todos los datos o borrarlos.\n\nNo te habrás dejado algo por registrar verdad...??",
            title="Cierre del programa")


# Mostrar todas las líneas que se han introducido por la pantalla.

# Capacidad de poder borrar/modificar o en su defecto agregar una observación a las líneas que ya se han introducido
# por si ha habido algún error.

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

# Frame para el gráfico.
graphic = Frame(root, bg="WHITE", borderwidth=3, relief="groove")
graphic.place(relx=0.25, rely=0.655, relwidth=0.6, relheight=0.34)

# Crear figura del gráfico.
figure = Figure(figsize=(25, 10), dpi=100)
x = ["4010016", "4010001", "4010017", "4010354", "4010236"]
y = [1.3, 0.75, 0.6, 0.85, 1.05]

# Poner el gráfico en la figura creada.
a = figure.add_subplot(111)
a.plot(x, y, marker="o")
a.set_xlabel("Colores")
a.set_ylabel("Rendimient (%)")
a.set_title("Rendimiento color")
a.legend()
a.grid()

# Creating Canvas
canv = FigureCanvasTkAgg(figure, master=graphic)
canv.draw()
get_widz = canv.get_tk_widget()
get_widz.pack()

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

led_hangers = tk_tools.Led(root, size=30)  # No sé cómo hacerlo funcionar.
led_hangers.place(relx=0.73, rely=0.1)
led_hangers.to_red(on=True)

led_observations = tk_tools.Led(root, size=30)  # No sé cómo hacerlo funcionar.
led_observations.place(relx=0.9, rely=0.1)
led_observations.to_red(on=True)

# registry_number=0 #Debería ser el número de registro más alto que tengamos en el excel, para que así al cerrar y abrir puedan ser consecutivos.

# Variables a utilizar.
final_colour = StringVar()
change_start_date_time = StringVar()
colour_start_date_time = StringVar()
colour_end_date_time = StringVar()
final_observation = StringVar()

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
xcerrar = 295

y1 = 0.35
y2 = y1 + 0.05
y3 = y2 + 0.05
y4 = y3 + 0.05
y5 = y4 + 0.05
y6 = y5 + 0.05
y7 = y6 + 0.05
yclose = 0.8

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
                             command=on_register_end_button_click)
register_end_button.place(relx=0.072, rely=0.17, relwidth=0.2, relheigh=0.07)

# Botón Registrar
register_button = Button(root, text="Registrar y continuar", activebackground="green",
                         command=on_register_continue_button_click)
register_button.place(relx=0.39, rely=0.17, relwidth=0.2, relheigh=0.07)

# Botón Registrar y DESCANSO
register_stop_button = Button(root, text="Registrar y PARADA", activebackground="green", command=on_register_stop_button_click)
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

# Botón para cerrar ventana
close = Button(root, text="Cerrar", activebackground="red", command=on_close_click)
# close.place(relx=xcerrar/xroot, y=yclose, relwidth=200/xroot, heigh=50)
close.place(relx=x1, rely=yclose, relwidth=0.2, relheigh=0.1)

root.mainloop()
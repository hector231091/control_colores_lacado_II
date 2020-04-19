import tkinter as tk
from tkinter import ttk
import datetime
from datetime import datetime
from tkinter import *
from tkinter import messagebox
from csv import reader
import sys
import pandas as pd
import tkinter

def validacion_color(text, new_text):
    if len(new_text)>8:
        return False
    return text.isdecimal()


def hora_inicio_cambio():
    now=datetime.now()
    fecha=now.strftime("%d/%m/%Y - %H:%M:%S")
    fecha_hora_inicio_cambio.set(fecha)
    return fecha_hora_inicio_cambio


def hora_inicio_color():
    now=datetime.now()
    fecha=now.strftime("%d/%m/%Y - %H:%M:%S")
    fecha_hora_inicio_color.set(fecha)
    return fecha_hora_inicio_color
    

def hora_final_color():
    now=datetime.now()
    fecha=now.strftime("%d/%m/%Y - %H:%M:%S")
    fecha_hora_final_color.set(fecha)
    return fecha_hora_final_color


def validacion_bastidor(text, new_text):
    if len(new_text)>2:
        return False
    return text.isdecimal()


def validacion_observaciones(text):
    if len(new_text)>50:
        return False


def registrar():
    
    # Cargar todos los colores en una lista.
    with open("Colores.csv", "r") as colores:
        lines = reader(colores)
        header = next(lines)
    
        lista_colores = []
    
        #if header!=None:
        for linea in colores:
            #lista_colores.append(linea)
            lista_colores.append(linea[0:8])

    # Añadir la palabra FIN a la lista de los colores
    lista_colores.append("FIN")
    lista_colores.append("OTRO")
    
    
    
    if color_2.get()=="OTRO" and observaciones_2.get()=="":
        messagebox.showerror(message="Si no me pones el color...ponlo en las observaciones :)", title="Falta poner el color en las observaciones")
    
    elif str(color_2.get()[0:9]) in lista_colores and color_2.get()!="" and fecha_hora_inicio_cambio.get()!="" and fecha_hora_inicio_color.get()!="" and fecha_hora_final_color.get()!="" and bastidores_2.get()!="":
    #elif color_2.get()!="" and fecha_hora_inicio_cambio.get()!="" and fecha_hora_inicio_color.get()!="" and fecha_hora_final_color.get()!="" and bastidores_2.get()!="":
    #if fecha_hora_inicio_cambio.get()!="" and fecha_hora_inicio_color.get()!="" and fecha_hora_final_color.get()!="" and bastidores_2.get()!="":
        # Registrar en el archivo.
        # Falta ponerle en número del registro.
        # Falta comprobar si está el archivo, en caso de que no esté hacerlo nuevo poniéndole el encabezado (nº registro, colores, hora inicio cambio, hora inicio color, hora fin, bastidores y observaciones)
        registro=open("Registro.csv", "a")
        registro.write(color_2.get()+";")
        registro.write(fecha_hora_inicio_cambio.get()+";")
        registro.write(fecha_hora_inicio_color.get()+";")
        registro.write(fecha_hora_final_color.get()+";")
        registro.write(bastidores_2.get()+";")
        registro.write(observaciones_2.get()+"\n")
        registro.close()
        
        # Eliminar el texto de las casillas que se completan
        color_2.delete("0", "end")
        fecha_hora_inicio_cambio.set("")
        fecha_hora_inicio_color.set("")
        fecha_hora_final_color.set("")
        bastidores_2.delete("0", "end")
        observaciones_2.delete("0", "end")
        
    else:
        if color_2.get()=="" or fecha_hora_inicio_cambio.get()=="" or fecha_hora_inicio_color.get()=="" or fecha_hora_final_color.get()=="" or bastidores_2.get()=="":
            messagebox.showerror(message="Faltan algún dato por completar", title="Algo no me cuadra...")
        
        elif str(color_2.get()[0:9]) in lista_colores:
            return True
        else:
            messagebox.showerror(message="El color que se ha introducino no existe.\n\nPor favor, introduce un color válido y vuelve a registrar", title="Error en el color")

    
    # Imprimir en el historial.
    # Pasamos el archivo de los registros a una matriz        
    df=pd.read_csv("Registro.csv",";",header=None)
    num_filas=len(df[0])
    
    L00.set(num_filas)
    L01.set(df[0][num_filas-1])
    L02.set(df[1][num_filas-1][13:21])
    L03.set(df[2][num_filas-1][13:21])
    L04.set(df[3][num_filas-1][13:21])
    L05.set(df[4][num_filas-1])
    L06.set(df[5][num_filas-1])
    
    L10.set(num_filas-1)
    L11.set(df[0][num_filas-2])
    L12.set(df[1][num_filas-2][13:21])
    L13.set(df[2][num_filas-2][13:21])
    L14.set(df[3][num_filas-2][13:21])
    L15.set(df[4][num_filas-2])
    L16.set(df[5][num_filas-2])
    
    L20.set(num_filas-2)
    L21.set(df[0][num_filas-3])
    L22.set(df[1][num_filas-3][13:21])
    L23.set(df[2][num_filas-3][13:21])
    L24.set(df[3][num_filas-3][13:21])
    L25.set(df[4][num_filas-3])
    L26.set(df[5][num_filas-3])
    
    L30.set(num_filas-3)
    L31.set(df[0][num_filas-4])
    L32.set(df[1][num_filas-4][13:21])
    L33.set(df[2][num_filas-4][13:21])
    L34.set(df[3][num_filas-4][13:21])
    L35.set(df[4][num_filas-4])
    L36.set(df[5][num_filas-4])
    
    L40.set(num_filas-4)
    L41.set(df[0][num_filas-5])
    L42.set(df[1][num_filas-5][13:21])
    L43.set(df[2][num_filas-5][13:21])
    L44.set(df[3][num_filas-5][13:21])
    L45.set(df[4][num_filas-5])
    L46.set(df[5][num_filas-5])
    
    L50.set(num_filas-5)
    L51.set(df[0][num_filas-6])
    L52.set(df[1][num_filas-6][13:21])
    L53.set(df[2][num_filas-6][13:21])
    L54.set(df[3][num_filas-6][13:21])
    L55.set(df[4][num_filas-6])
    L56.set(df[5][num_filas-6])
    
    L60.set(num_filas-6)
    L61.set(df[0][num_filas-7])
    L62.set(df[1][num_filas-7][13:21])
    L63.set(df[2][num_filas-7][13:21])
    L64.set(df[3][num_filas-7][13:21])
    L65.set(df[4][num_filas-7])
    L66.set(df[5][num_filas-7])
    
    """#L00.set(num_registro) No tengo ni idea de cómo hacer esto...
    L01.set(color_2.get())
    L02.set(fecha_hora_inicio_cambio.get())
    L03.set(fecha_hora_inicio_color.get())
    L04.set(fecha_hora_final_color.get())
    L05.set(bastidores_2.get())
    L06.set(observaciones_2.get())"""
    


def cerrar():

    if color_2.get()=="" and fecha_hora_inicio_cambio.get()=="" and fecha_hora_inicio_color.get()=="" and fecha_hora_final_color.get()=="" and bastidores_2.get()=="" and observaciones_2.get()=="":
        mensaje_cierre=messagebox.askquestion(message="¿Seguro que quieres salir?", title="Hasta otra!")
        if mensaje_cierre=="yes":
            root.destroy()
        else:
            messagebox.showinfo(message="Ya te querías ir eh...venga, a currar!!")
    else:

        messagebox.showerror(message="Para poder salir debes registrar todos los datos o borrarlos.\n\nNo te habrás dejado algo por registrar verdad...??", title="Algo no está bien...")

 
# Mostrar todas las líneas que se han introducido por la pantalla.

# Capacidad de poder borrar/modificar o en su defecto agregar una observación a las líneas que ya se han introducido por si ha habido algún error.

root=tk.Tk()
root.title("Registros")
root.resizable()
root.geometry("790x630")
#root.iconbitmap("Gaviota.ico")

#registros=Frame(root, relief="sunken")
#registros.pack(side="bottom")
#registros.config(bg="blue")
#registros.config(width="150", height="150")
#registros.place(x=100, y=150, width=100, heigh=100)

num_registro=0 #Debería ser el número de registro más alto que tengamos en el excel, para que así al cerra y abrir puedan ser consecutivos.

# Variables a utilizar.
fecha_hora_inicio_cambio = StringVar()
fecha_hora_inicio_color = StringVar()
fecha_hora_final_color = StringVar()

# Definir las variables de cada una de las celdas del historial

L00=StringVar()
L01=StringVar()
L02=StringVar()
L03=StringVar()
L04=StringVar()
L05=StringVar()
L06=StringVar()

L10=StringVar()
L11=StringVar()
L12=StringVar()
L13=StringVar()
L14=StringVar()
L15=StringVar()
L16=StringVar()

L20=StringVar()
L21=StringVar()
L22=StringVar()
L23=StringVar()
L24=StringVar()
L25=StringVar()
L26=StringVar()

L30=StringVar()
L31=StringVar()
L32=StringVar()
L33=StringVar()
L34=StringVar()
L35=StringVar()
L36=StringVar()

L40=StringVar()
L41=StringVar()
L42=StringVar()
L43=StringVar()
L44=StringVar()
L45=StringVar()
L46=StringVar()

L50=StringVar()
L51=StringVar()
L52=StringVar()
L53=StringVar()
L54=StringVar()
L55=StringVar()
L56=StringVar()

L60=StringVar()
L61=StringVar()
L62=StringVar()
L63=StringVar()
L64=StringVar()
L65=StringVar()
L66=StringVar()

# Registro de datos.
color_1=Label(root, text="Color", anchor="center", relief="groove")
color_1.place(x=10, y=10, width=120, heigh=30)
color_2=Entry(root, justify="center", validate="key", validatecommand=(root.register(validacion_color), "%S", "%P"))
color_2.place(x=10, y=50, width=120, heigh=30)

hora_ini_camb_1 = Button(root, text="Hora inicio cambio", command=hora_inicio_cambio)
hora_ini_camb_1.place(x=140, y=10, width=120, heigh=30)
hora_ini_camb_2 = Label(root, background="white", textvariable=fecha_hora_inicio_cambio)
hora_ini_camb_2.place(x=140, y=50, width=120, heigh=30)

hora_ini_col_1 = Button(root, text="Hora inicio color", command=hora_inicio_color)
hora_ini_col_1.place(x=270, y=10, width=120, heigh=30)
hora_ini_col_2 = Label(root, background="white", textvariable=fecha_hora_inicio_color)
hora_ini_col_2.place(x=270, y=50, width=120, heigh=30)

hora_fin_col_1 = Button(root, text="Hora final color", command=hora_final_color)
hora_fin_col_1.place(x=400, y=10, width=120, heigh=30)
hora_fin_col_2 = Label(root, background="white", textvariable=fecha_hora_final_color)
hora_fin_col_2.place(x=400, y=50, width=120, heigh=30)

bastidores_1 = Label(root, text="Nº de bastidores", anchor="center", relief="groove")
bastidores_1.place(x=530, y=10, width=120, heigh=30)
bastidores_2 = Entry(root, justify="center", validate="key", validatecommand=(root.register(validacion_bastidor), "%S", "%P"))
bastidores_2.place(x=530, y=50, width=120, heigh=30)

observaciones_1 = Label(root, text="Observaciones", anchor="center", relief="groove")
observaciones_1.place(x=660, y=10, width=120, heigh=30)
observaciones_2 = Entry(root, justify="center", validate="key", validatecommand=(root.register(validacion_observaciones), "%P"))
observaciones_2.place(x=660, y=50, width=120, heigh=30)

# Variables de la posición de los cuadros de "Registrar" hacia abajo

xregistrar = 295
xhistorial = 10
x1 = 10
x2 = 70
x3 = x2+120
x4 = x3+120
x5 = x4+120
x6 = x5+120
x7 = x6+120
xcerrar = 295

yregistrar = 150
ycabecera = 260
y1 = 295
y2 = y1+35
y3 = y2+35
y4 = y3+35
y5 = y4+35
y6 = y5+35
y7 = y6+35
ycerrar = 550

# Botón Registrar
registrar=Button(root, text="Registrar", activebackground="green", command=registrar)
registrar.place(x=xregistrar, y=yregistrar, width=200, heigh=50)

# Historial de los registros anteriores.
historial=Label(root, text="Historial de Registros", relief="sunken", background="cyan")
historial.place(x=x1, y=175+50, width=770, heigh=30)

num_registro=Label(root, text="Nº", relief="groove", background="cyan")
num_registro.place(x=x1, y=ycabecera, width=50, heigh=30)

color_3=Label(root, text="Color", relief="groove", background="cyan")
color_3.place(x=x2, y=ycabecera, width=110, heigh=30)

hora_ini_camb_3=Label(root, text="Hora inicio cambio", relief="groove", background="cyan")
hora_ini_camb_3.place(x=x3, y=ycabecera, width=110, heigh=30)

hora_ini_col_3=Label(root, text="Hora inicio color", relief="groove", background="cyan")
hora_ini_col_3.place(x=x4, y=ycabecera, width=110, heigh=30)

hora_fin_col_3=Label(root, text="Hora final color", relief="groove", background="cyan")
hora_fin_col_3.place(x=x5, y=ycabecera, width=110, heigh=30)

bastidores_3=Label(root, text="Nº de bastidores", relief="groove", background="cyan")
bastidores_3.place(x=x6, y=ycabecera, width=110, heigh=30)

observaciones_3=Label(root, text="Observaciones", relief="groove", background="cyan")
observaciones_3.place(x=x7, y=ycabecera, width=110, heigh=30)

#---------------------------------------------------------------------------

L_0_0=Label(root, background="white", textvariable=L00, relief="groove")
L_0_0.place(x=x1, y=y1, width=50, heigh=30)

L_0_1=Label(root, background="white", textvariable=L01, relief="groove")
L_0_1.place(x=x2, y=y1, width=110, heigh=30)

L_0_2=Label(root, background="white", textvariable=L02, relief="groove")
L_0_2.place(x=x3, y=y1, width=110, heigh=30)

L_0_3=Label(root, background="white", textvariable=L03, relief="groove")
L_0_3.place(x=x4, y=y1, width=110, heigh=30)

L_0_4=Label(root, background="white", textvariable=L04, relief="groove")
L_0_4.place(x=x5, y=y1, width=110, heigh=30)

L_0_5=Label(root, background="white", textvariable=L05, relief="groove")
L_0_5.place(x=x6, y=y1, width=110, heigh=30)

L_0_6=Label(root, background="white", textvariable=L06, relief="groove")
L_0_6.place(x=x7, y=y1, width=110, heigh=30)

#---------------------------------------------------------------------------

L_1_0=Label(root, background="white", textvariable=L10, relief="groove")
L_1_0.place(x=x1, y=y2, width=50, heigh=30)

L_1_1=Label(root, background="white", textvariable=L11, relief="groove")
L_1_1.place(x=x2, y=y2, width=110, heigh=30)

L_1_2=Label(root, background="white", textvariable=L12, relief="groove")
L_1_2.place(x=x3, y=y2, width=110, heigh=30)

L_1_3=Label(root, background="white", textvariable=L13, relief="groove")
L_1_3.place(x=x4, y=y2, width=110, heigh=30)

L_1_4=Label(root, background="white", textvariable=L14, relief="groove")
L_1_4.place(x=x5, y=y2, width=110, heigh=30)

L_1_5=Label(root, background="white", textvariable=L15, relief="groove")
L_1_5.place(x=x6, y=y2, width=110, heigh=30)

L_1_6=Label(root, background="white", textvariable=L16, relief="groove")
L_1_6.place(x=x7, y=y2, width=110, heigh=30)

#---------------------------------------------------------------------------

L_2_0=Label(root, background="white", textvariable=L20, relief="groove")
L_2_0.place(x=x1, y=y3, width=50, heigh=30)

L_2_1=Label(root, background="white", textvariable=L21, relief="groove")
L_2_1.place(x=x2, y=y3, width=110, heigh=30)

L_2_2=Label(root, background="white", textvariable=L22, relief="groove")
L_2_2.place(x=x3, y=y3, width=110, heigh=30)

L_2_3=Label(root, background="white", textvariable=L23, relief="groove")
L_2_3.place(x=x4, y=y3, width=110, heigh=30)

L_2_4=Label(root, background="white", textvariable=L24, relief="groove")
L_2_4.place(x=x5, y=y3, width=110, heigh=30)

L_2_5=Label(root, background="white", textvariable=L25, relief="groove")
L_2_5.place(x=x6, y=y3, width=110, heigh=30)

L_2_6=Label(root, background="white", textvariable=L26, relief="groove")
L_2_6.place(x=x7, y=y3, width=110, heigh=30)

#---------------------------------------------------------------------------

L_3_0=Label(root, background="white", textvariable=L30, relief="groove")
L_3_0.place(x=x1, y=y4, width=50, heigh=30)

L_3_1=Label(root, background="white", textvariable=L31, relief="groove")
L_3_1.place(x=x2, y=y4, width=110, heigh=30)

L_3_2=Label(root, background="white", textvariable=L32, relief="groove")
L_3_2.place(x=x3, y=y4, width=110, heigh=30)

L_3_3=Label(root, background="white", textvariable=L33, relief="groove")
L_3_3.place(x=x4, y=y4, width=110, heigh=30)

L_3_4=Label(root, background="white", textvariable=L34, relief="groove")
L_3_4.place(x=x5, y=y4, width=110, heigh=30)

L_3_5=Label(root, background="white", textvariable=L35, relief="groove")
L_3_5.place(x=x6, y=y4, width=110, heigh=30)

L_3_6=Label(root, background="white", textvariable=L36, relief="groove")
L_3_6.place(x=x7, y=y4, width=110, heigh=30)

#---------------------------------------------------------------------------

L_4_0=Label(root, background="white", textvariable=L40, relief="groove")
L_4_0.place(x=x1, y=y5, width=50, heigh=30)

L_4_1=Label(root, background="white", textvariable=L41, relief="groove")
L_4_1.place(x=x2, y=y5, width=110, heigh=30)

L_4_2=Label(root, background="white", textvariable=L42, relief="groove")
L_4_2.place(x=x3, y=y5, width=110, heigh=30)

L_4_3=Label(root, background="white", textvariable=L43, relief="groove")
L_4_3.place(x=x4, y=y5, width=110, heigh=30)

L_4_4=Label(root, background="white", textvariable=L44, relief="groove")
L_4_4.place(x=x5, y=y5, width=110, heigh=30)

L_4_5=Label(root, background="white", textvariable=L45, relief="groove")
L_4_5.place(x=x6, y=y5, width=110, heigh=30)

L_4_6=Label(root, background="white", textvariable=L46, relief="groove")
L_4_6.place(x=x7, y=y5, width=110, heigh=30)

#---------------------------------------------------------------------------

L_5_0=Label(root, background="white", textvariable=L50, relief="groove")
L_5_0.place(x=x1, y=y6, width=50, heigh=30)

L_5_1=Label(root, background="white", textvariable=L51, relief="groove")
L_5_1.place(x=x2, y=y6, width=110, heigh=30)

L_5_2=Label(root, background="white", textvariable=L52, relief="groove")
L_5_2.place(x=x3, y=y6, width=110, heigh=30)

L_5_3=Label(root, background="white", textvariable=L53, relief="groove")
L_5_3.place(x=x4, y=y6, width=110, heigh=30)

L_5_4=Label(root, background="white", textvariable=L54, relief="groove")
L_5_4.place(x=x5, y=y6, width=110, heigh=30)

L_5_5=Label(root, background="white", textvariable=L55, relief="groove")
L_5_5.place(x=x6, y=y6, width=110, heigh=30)

L_5_6=Label(root, background="white", textvariable=L56, relief="groove")
L_5_6.place(x=x7, y=y6, width=110, heigh=30)

#---------------------------------------------------------------------------

L_6_0=Label(root, background="white", textvariable=L60, relief="groove")
L_6_0.place(x=x1, y=y7, width=50, heigh=30)

L_6_1=Label(root, background="white", textvariable=L61, relief="groove")
L_6_1.place(x=x2, y=y7, width=110, heigh=30)

L_6_2=Label(root, background="white", textvariable=L62, relief="groove")
L_6_2.place(x=x3, y=y7, width=110, heigh=30)

L_6_3=Label(root, background="white", textvariable=L63, relief="groove")
L_6_3.place(x=x4, y=y7, width=110, heigh=30)

L_6_4=Label(root, background="white", textvariable=L64, relief="groove")
L_6_4.place(x=x5, y=y7, width=110, heigh=30)

L_6_5=Label(root, background="white", textvariable=L65, relief="groove")
L_6_5.place(x=x6, y=y7, width=110, heigh=30)

L_6_6=Label(root, background="white", textvariable=L66, relief="groove")
L_6_6.place(x=x7, y=y7, width=110, heigh=30)

# Botón para cerrar ventana
cerrar=Button(root, text="Cerrar", activebackground="red", command=cerrar)
cerrar.place(x=xcerrar, y=ycerrar, width=200, heigh=50)

root.mainloop()
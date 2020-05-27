from tkinter import *

CELL_MARGIN = 10
CELL_PADDING = 5


class HistoricalView(Frame):
    def __init__(self, parent, rows_to_show):
        Frame.__init__(self, parent)
        # rows_to_show indica el límite de filas a mostrar
        self.rows_to_show = rows_to_show
        # __labels es una variable que representa una matriz de Labels.
        # En esta variable se almacenan las Labels cuando se crea el esqueleto (mediante __init_empty_skeleton)
        # y después las reusa, accediendo mediante índices a la matriz, cuando necesita publicar los datos.
        # De este modo, no hace falta guardar una referencia a cada una de las Labels
        self.__labels = []

        self.__init_header()
        self.__init_empty_skeleton(self.__labels)

    # Esta función crea los encabezados del historial (celdas en azul)
    def __init_header(self):
        historical_header_label = Label(self, text="Historial de Registros", relief="sunken", background="cyan")
        historical_header_label.grid(row=0,
                                     column=0,
                                     columnspan=7,
                                     pady=(0, CELL_PADDING),
                                     ipadx=CELL_MARGIN,
                                     ipady=CELL_MARGIN,
                                     sticky=W + E + N + S)  # La celda se expande en todas direcciones

        registry_number_header_label = self.__create_header_label("Nº")
        registry_number_header_label.grid(row=1,
                                          column=0,
                                          padx=(0, CELL_PADDING),
                                          pady=CELL_PADDING,
                                          ipadx=CELL_MARGIN,
                                          ipady=CELL_MARGIN,
                                          sticky=W + E + N + S)
        self.grid_columnconfigure(0, weight=1)  # Toma el ancho de pantalla
        colour_header_label = self.__create_header_label("Color")
        colour_header_label.grid(row=1,
                                 column=1,
                                 padx=CELL_PADDING,
                                 pady=CELL_PADDING,
                                 ipadx=CELL_MARGIN,
                                 ipady=CELL_MARGIN,
                                 sticky=W + E + N + S)
        self.grid_columnconfigure(1, weight=1)
        change_start_time_header_label = self.__create_header_label("Hora inicio cambio")
        change_start_time_header_label.grid(row=1,
                                            column=2,
                                            padx=CELL_PADDING,
                                            pady=CELL_PADDING,
                                            ipadx=CELL_MARGIN,
                                            ipady=CELL_MARGIN,
                                            sticky=W + E + N + S)
        self.grid_columnconfigure(2, weight=1)
        colour_start_time_header_label = self.__create_header_label("Hora inicio color")
        colour_start_time_header_label.grid(row=1,
                                            column=3,
                                            padx=CELL_PADDING,
                                            pady=CELL_PADDING,
                                            ipadx=CELL_MARGIN,
                                            ipady=CELL_MARGIN,
                                            sticky=W + E + N + S)
        self.grid_columnconfigure(3, weight=1)
        colour_end_time_header_label = self.__create_header_label("Hora final color")
        colour_end_time_header_label.grid(row=1,
                                          column=4,
                                          padx=CELL_PADDING,
                                          pady=CELL_PADDING,
                                          ipadx=CELL_MARGIN,
                                          ipady=CELL_MARGIN,
                                          sticky=W + E + N + S)
        self.grid_columnconfigure(4, weight=1)
        hangers_header_label = self.__create_header_label("Nº de bastidores")
        hangers_header_label.grid(row=1,
                                  column=5,
                                  padx=CELL_PADDING,
                                  pady=CELL_PADDING,
                                  ipadx=CELL_MARGIN,
                                  ipady=CELL_MARGIN,
                                  sticky=W + E + N + S)
        self.grid_columnconfigure(5, weight=1)
        observations_header_label = self.__create_header_label("Observaciones")
        observations_header_label.grid(row=1,
                                       column=6,
                                       padx=(CELL_PADDING, 0),
                                       pady=CELL_PADDING,
                                       ipadx=CELL_MARGIN,
                                       ipady=CELL_MARGIN,
                                       sticky=W + E + N + S)
        self.grid_columnconfigure(6, weight=2)

    # Método de ayuda para evitar repetir código. Crea una Label para el encabezado del historial.
    def __create_header_label(self, text):
        return Label(self, text=text, relief="groove", background="cyan")

    # Inicializa una matriz de celdas vacías con Labels.
    # El límite de filas viene establecido por el parámetro rows_to_show.
    def __init_empty_skeleton(self, labels):
        for i in range(self.rows_to_show):
            row = []
            labels.append(row)
            self.__create_empty_record(i, row)

    def __create_empty_record(self, index, row):
        global_index = index + 2
        column0 = self.__create_empty_record_label()
        column0.grid(row=global_index,
                     column=0,
                     padx=(0, CELL_PADDING),
                     pady=CELL_PADDING,
                     ipadx=CELL_MARGIN,
                     ipady=CELL_MARGIN,
                     sticky=W + E + N + S)
        row.append(column0)

        column1 = self.__create_empty_record_label()
        column1.grid(row=global_index,
                     column=1,
                     padx=CELL_PADDING,
                     pady=CELL_PADDING,
                     ipadx=CELL_MARGIN,
                     ipady=CELL_MARGIN,
                     sticky=W + E + N + S)
        row.append(column1)

        column2 = self.__create_empty_record_label()
        column2.grid(row=global_index,
                     column=2,
                     padx=CELL_PADDING,
                     pady=CELL_PADDING,
                     ipadx=CELL_MARGIN,
                     ipady=CELL_MARGIN,
                     sticky=W + E + N + S)
        row.append(column2)

        column3 = self.__create_empty_record_label()
        column3.grid(row=global_index,
                     column=3,
                     padx=CELL_PADDING,
                     pady=CELL_PADDING,
                     ipadx=CELL_MARGIN,
                     ipady=CELL_MARGIN,
                     sticky=W + E + N + S)
        row.append(column3)

        column4 = self.__create_empty_record_label()
        column4.grid(row=global_index,
                     column=4,
                     padx=CELL_PADDING,
                     pady=CELL_PADDING,
                     ipadx=CELL_MARGIN,
                     ipady=CELL_MARGIN,
                     sticky=W + E + N + S)
        row.append(column4)

        column5 = self.__create_empty_record_label()
        column5.grid(row=global_index,
                     column=5,
                     padx=CELL_PADDING,
                     pady=CELL_PADDING,
                     ipadx=CELL_MARGIN,
                     ipady=CELL_MARGIN,
                     sticky=W + E + N + S)
        row.append(column5)

        column6 = self.__create_empty_record_label()
        column6.grid(row=global_index,
                     column=6,
                     padx=(CELL_PADDING, 0),
                     pady=CELL_PADDING,
                     ipadx=CELL_MARGIN,
                     ipady=CELL_MARGIN,
                     sticky=W + E + N + S)
        row.append(column6)

    # Método de ayuda para evitar repetir código. Crea una Label para el registro.
    def __create_empty_record_label(self):
        return Label(self, background="white", relief="groove")

    def update_historical(self, records):
        for i in range(self.rows_to_show):
            # Si no hay más records que mostrar, retornamos ejecución aunque el historial no esté completo.
            # Por ejemplo, el histórico se define para mostrar 6 filas de datos pero aquí solo se pasan 4.
            if len(records) == i:
                return

            record = records[i]
            self.__labels[i][0].configure(text=record.id)
            self.__labels[i][1].configure(text=record.colour_code)
            self.__labels[i][2].configure(text=record.change_start_time[11:21])
            self.__labels[i][3].configure(text=record.colour_start_time[11:21])
            self.__labels[i][4].configure(text=record.colour_end_time[11:21])
            self.__labels[i][5].configure(text=record.hangers_amount)
            self.__labels[i][6].configure(text=record.observations)

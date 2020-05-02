from tkinter import *

CELL_MARGIN = 10
CELL_PADDING = 2


class ShowPercentage(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.show_efficiency_hangers = StringVar()
        self.show_efficiency_change_colour = StringVar()

        self.efficiency_colour_title = Label(self, text="Rendimiento del último color", anchor="center",
                                             relief="groove")
        self.efficiency_colour_title.grid(row=0,
                                          column=0,
                                          padx=(0, CELL_PADDING),
                                          pady=(0, CELL_PADDING),
                                          ipadx=CELL_MARGIN,
                                          ipady=CELL_MARGIN,
                                          sticky=W + E + N + S)
        self.efficiency_colour_result = Label(self, textvariable=self.show_efficiency_hangers, bg="white",
                                              anchor="center", relief="groove")
        self.efficiency_colour_result.grid(row=1,
                                           column=0,
                                           padx=(0, CELL_PADDING),
                                           pady=(0, CELL_PADDING),
                                           ipadx=CELL_MARGIN,
                                           ipady=CELL_MARGIN,
                                           sticky=W + E + N + S)
        self.efficiency_change_colour_title = Label(self, text="Rendimiento del último cambio de color",
                                                    anchor="center", relief="groove")
        self.efficiency_change_colour_title.grid(row=3,
                                                 column=0,
                                                 padx=(0, CELL_PADDING),
                                                 pady=(0, CELL_PADDING),
                                                 ipadx=CELL_MARGIN,
                                                 ipady=CELL_MARGIN,
                                                 sticky=W + E + N + S)
        self.efficiency_change_colour_result = Label(self, textvariable=self.show_efficiency_change_colour, bg="white",
                                                     anchor="center", relief="groove")
        self.efficiency_change_colour_result.grid(row=4,
                                                  column=0,
                                                  padx=(0, CELL_PADDING),
                                                  pady=(0, CELL_PADDING),
                                                  ipadx=CELL_MARGIN,
                                                  ipady=CELL_MARGIN,
                                                  sticky=W + E + N + S)

    def __get_change_colour_time_efficiency(self, color_1_and_2, change_times_list):
        num_rows, registry_file = load_history()

        self.last_colour = registry_file[0][num_rows - 1]
        self.penultimate_colour = registry_file[0][num_rows - 2]

        self.concatenate_two_colours = self.penultimate_colour + "-" + self.last_colour

        try:
            self.index_concatenate_colours = color_1_and_2.index(self.concatenate_two_colours)
            self.calculate_efficiency_change_colour(self.index_concatenate_colours)
            self.show_efficiency_change_colour.set(
                self.calculate_efficiency_change_colour(self.index_concatenate_colours))

        except ValueError:
            self.show_efficiency_change_colour.set("No hay datos\nanteriores con lo\nque comparar.")

    def __get_colour_time_efficiency(self, start_datetime_as_string, end_datetime_as_string,
                                     amount_of_hangers_as_string):
        # Convierto los entrys en fechas para poder restarlas.
        self.start_colour = datetime.strptime(start_datetime_as_string.get(), "%d/%m/%Y - %H:%M:%S")
        self.end_colour = datetime.strptime(end_datetime_as_string.get(), "%d/%m/%Y - %H:%M:%S")

        # Convertimos los bastidores a un entero.
        self.hangers = int(self.amount_of_hangers_as_string.get())

        # Restamos las dos fechas y lo pasamos a segundos.
        self.time_diff = self.end_colour - self.start_colour
        self.time_colour = self.time_diff.days * 24 * 3600 + self.time_diff.seconds

        # Comparamos el número de bastidores con los que podrían pasar con un rendimiento del 100%.
        self.ideal_hanger_passing_time = 10
        self.max_hangers_in_time_colour = self.time_colour / ideal_hanger_passing_time

        # Eficiencia del paso de bastidores de este color.
        self.efficiency_hangers = self.hangers / self.self.max_hangers_in_time_colour

        # round(number,1) sirve para redondear un flotante al decimal que queramos
        self.percentage_efficiency_hangers = str(int(self.efficiency_hangers * 100)) + " %"

        self.show_efficiency_hanger

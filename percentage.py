from tkinter import *
from datetime import datetime

from constants import DATE_TIME_FORMAT

CELL_MARGIN = 10
CELL_PADDING = 2


class ShowPercentage(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.show_efficiency_hangers = StringVar()
        self.show_efficiency_change_colour = StringVar()

        self.efficiency_colour_title = Label(self,
                                             text="Rendimiento del último color",
                                             anchor="center",
                                             relief="groove")
        self.efficiency_colour_title.grid(row=0,
                                          column=0,
                                          padx=(0, CELL_PADDING),
                                          pady=(0, CELL_PADDING),
                                          ipadx=CELL_MARGIN,
                                          ipady=CELL_MARGIN,
                                          sticky=W + E + N + S)
        self.efficiency_colour_result = Label(self,
                                              textvariable=self.show_efficiency_hangers,
                                              bg="white",
                                              anchor="center",
                                              relief="groove")
        self.efficiency_colour_result.grid(row=1,
                                           column=0,
                                           padx=(0, CELL_PADDING),
                                           pady=(0, CELL_PADDING),
                                           ipadx=CELL_MARGIN,
                                           ipady=CELL_MARGIN,
                                           sticky=W + E + N + S)
        self.efficiency_change_colour_title = Label(self,
                                                    text="Rendimiento del último cambio de color",
                                                    anchor="center",
                                                    relief="groove")
        self.efficiency_change_colour_title.grid(row=3,
                                                 column=0,
                                                 padx=(0, CELL_PADDING),
                                                 pady=(0, CELL_PADDING),
                                                 ipadx=CELL_MARGIN,
                                                 ipady=CELL_MARGIN,
                                                 sticky=W + E + N + S)
        self.efficiency_change_colour_result = Label(self,
                                                     textvariable=self.show_efficiency_change_colour,
                                                     bg="white",
                                                     anchor="center",
                                                     relief="groove")
        self.efficiency_change_colour_result.grid(row=4,
                                                  column=0,
                                                  padx=(0, CELL_PADDING),
                                                  pady=(0, CELL_PADDING),
                                                  ipadx=CELL_MARGIN,
                                                  ipady=CELL_MARGIN,
                                                  sticky=W + E + N + S)

    def update_change_colour_time_efficiency(self,
                                             color_1_and_2_list,
                                             change_times_list,
                                             history_as_records):
        last_colour = history_as_records[len(history_as_records) - 1].colour_code
        penultimate_colour = history_as_records[len(history_as_records) - 2].colour_code
        concatenate_two_colours = penultimate_colour + "-" + last_colour

        try:
            index_concatenate_colours = color_1_and_2_list.index(concatenate_two_colours)
            efficiency = self.__calculate_efficiency_change_colour(index_concatenate_colours,
                                                                   change_times_list,
                                                                   history_as_records)
            self.show_efficiency_change_colour.set(efficiency)

        except ValueError:
            self.show_efficiency_change_colour.set("No hay datos\nanteriores con lo\nque comparar.")

    def update_colour_time_efficiency(self,
                                      start_datetime_as_string,
                                      end_datetime_as_string,
                                      amount_of_hangers_as_string):
        # Convierto los entrys en fechas para poder restarlas.
        start_colour = datetime.strptime(start_datetime_as_string, DATE_TIME_FORMAT)
        end_colour = datetime.strptime(end_datetime_as_string, DATE_TIME_FORMAT)

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

        self.show_efficiency_hangers.set(percentage_efficiency_hangers)

    def __calculate_efficiency_change_colour(self,
                                             color_position_in_the_list,
                                             change_times_list,
                                             history_as_records):
        average_time_of_colour_change = int((change_times_list[color_position_in_the_list][18:]))
        time1 = datetime.strptime(history_as_records[len(history_as_records) - 1].change_start_time, DATE_TIME_FORMAT)
        time2 = datetime.strptime(history_as_records[len(history_as_records) - 1].colour_start_time, DATE_TIME_FORMAT)

        last_time_change = time2 - time1

        last_time_change_in_seconds = last_time_change.days * 24 * 3600 + last_time_change.seconds

        efficiency_change_last_colour = \
            str(int((average_time_of_colour_change * 100) / last_time_change_in_seconds)) + " %"
        return efficiency_change_last_colour

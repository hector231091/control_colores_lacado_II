from datetime import datetime
from tkinter import *
from csv import reader

import tk_tools

import validator
from constants import DATE_TIME_FORMAT
from data import InputRecord, ValidationType

CELL_MARGIN = 10
CELL_PADDING = 10


class InputView(Frame):
    def __init__(self, parent, colour_map):
        Frame.__init__(self, parent)

        self.colour_map = colour_map

        self.colour_name = StringVar()
        self.change_start_date_time = StringVar()
        self.colour_start_date_time = StringVar()
        self.colour_end_date_time = StringVar()

        self.colour_label = Label(self, text="Color", anchor="center")
        self.colour_label.grid(row=0,
                               column=0,
                               padx=(0, CELL_PADDING),
                               pady=(0, CELL_PADDING),
                               ipadx=CELL_MARGIN,
                               ipady=CELL_MARGIN,
                               sticky=W + E + N + S)
        self.colour_entry = Entry(self,
                                  justify="center",
                                  validate="key",
                                  validatecommand=(self.register(self.__validate_colour_input), '%P'))
        self.colour_entry.grid(row=1,
                               column=0,
                               padx=(0, CELL_PADDING),
                               pady=CELL_PADDING,
                               ipadx=CELL_MARGIN,
                               ipady=CELL_MARGIN,
                               sticky=W + E + N + S)
        self.led_colour = tk_tools.Led(self, size=30)
        self.led_colour.grid(row=2, column=0)
        self.led_colour.to_grey(on=True)
        self.grid_columnconfigure(0, weight=1)  # La fila toma el ancho de pantalla
        self.colour_name_label = Label(self, textvariable=self.colour_name, anchor="center", relief="groove")
        self.colour_name_label.grid(row=3,
                                    column=0,
                                    padx=(0, CELL_PADDING),
                                    pady=CELL_PADDING,
                                    ipadx=CELL_MARGIN,
                                    ipady=CELL_MARGIN,
                                    sticky=W + E + N + S)

        self.change_start_time_button = Button(self,
                                               text="Hora inicio cambio",
                                               state=NORMAL,
                                               command=self.__on_change_start_time_click)
        self.change_start_time_button.grid(row=0,
                                           column=1,
                                           padx=CELL_PADDING,
                                           pady=(0, CELL_PADDING),
                                           ipadx=CELL_MARGIN,
                                           ipady=CELL_MARGIN,
                                           sticky=W + E + N + S)
        self.change_start_time_label = Label(self, background="white", textvariable=self.change_start_date_time)
        self.change_start_time_label.grid(row=1,
                                          column=1,
                                          padx=CELL_PADDING,
                                          pady=CELL_PADDING,
                                          ipadx=CELL_MARGIN,
                                          ipady=CELL_MARGIN,
                                          sticky=W + E + N + S)
        self.led_change_start_time = tk_tools.Led(self, size=30)
        self.led_change_start_time.grid(row=2, column=1)
        self.led_change_start_time.to_grey(on=True)
        self.grid_columnconfigure(1, weight=1)

        self.colour_start_time_button = Button(self,
                                               text="Hora inicio color",
                                               state=DISABLED,
                                               command=self.__on_colour_start_time_click)
        self.colour_start_time_button.grid(row=0,
                                           column=2,
                                           padx=CELL_PADDING,
                                           pady=(0, CELL_PADDING),
                                           ipadx=CELL_MARGIN,
                                           ipady=CELL_MARGIN,
                                           sticky=W + E + N + S)
        self.colour_start_time_label = Label(self, background="white", textvariable=self.colour_start_date_time)
        self.colour_start_time_label.grid(row=1,
                                          column=2,
                                          padx=CELL_PADDING,
                                          pady=CELL_PADDING,
                                          ipadx=CELL_MARGIN,
                                          ipady=CELL_MARGIN,
                                          sticky=W + E + N + S)
        self.led_colour_start_time = tk_tools.Led(self, size=30)
        self.led_colour_start_time.grid(row=2, column=2)
        self.led_colour_start_time.to_grey(on=True)
        self.grid_columnconfigure(2, weight=1)

        self.colour_end_time_button = Button(self,
                                             text="Hora final color",
                                             state=DISABLED,
                                             command=self.__on_colour_end_time_click)
        self.colour_end_time_button.grid(row=0,
                                         column=3,
                                         padx=CELL_PADDING,
                                         pady=(0, CELL_PADDING),
                                         ipadx=CELL_MARGIN,
                                         ipady=CELL_MARGIN,
                                         sticky=W + E + N + S)
        self.colour_end_time_label = Label(self, background="white", textvariable=self.colour_end_date_time)
        self.colour_end_time_label.grid(row=1,
                                        column=3,
                                        padx=CELL_PADDING,
                                        pady=CELL_PADDING,
                                        ipadx=CELL_MARGIN,
                                        ipady=CELL_MARGIN,
                                        sticky=W + E + N + S)
        self.led_colour_end_time = tk_tools.Led(self, size=30)
        self.led_colour_end_time.grid(row=2, column=3)
        self.led_colour_end_time.to_grey(on=True)
        self.grid_columnconfigure(3, weight=1)

        self.hangers_label = Label(self, text="Nº de bastidores", anchor="center")
        self.hangers_label.grid(row=0,
                                column=4,
                                padx=CELL_PADDING,
                                pady=(0, CELL_PADDING),
                                ipadx=CELL_MARGIN,
                                ipady=CELL_MARGIN,
                                sticky=W + E + N + S)
        self.hangers_entry = Entry(self,
                                   justify="center",
                                   validate="key",
                                   validatecommand=(self.register(self.__validate_hangers_input), '%P', '%S'))
        self.hangers_entry.grid(row=1,
                                column=4,
                                padx=CELL_PADDING,
                                pady=CELL_PADDING,
                                ipadx=CELL_MARGIN,
                                ipady=CELL_MARGIN,
                                sticky=W + E + N + S)
        self.led_hangers = tk_tools.Led(self, size=30)
        self.led_hangers.grid(row=2, column=4)
        self.led_hangers.to_grey(on=True)
        self.grid_columnconfigure(4, weight=1)

        self.observations_label = Label(self, text="Observaciones", anchor="center")
        self.observations_label.grid(row=0,
                                     column=5,
                                     padx=CELL_PADDING,
                                     pady=(0, CELL_PADDING),
                                     ipadx=CELL_MARGIN,
                                     ipady=CELL_MARGIN,
                                     sticky=W + E + N + S)
        self.observations_entry = Entry(self,
                                        justify="center",
                                        validate="key",
                                        validatecommand=(self.register(self.__validate_observations_input), '%P',),
                                        state=NORMAL)
        self.observations_entry.grid(row=1,
                                     column=5,
                                     padx=CELL_PADDING,
                                     pady=CELL_PADDING,
                                     ipadx=CELL_MARGIN,
                                     ipady=CELL_MARGIN,
                                     sticky=W + E + N + S)
        self.led_observations = tk_tools.Led(self, size=30)
        self.led_observations.grid(row=2, column=5)
        self.led_observations.to_grey(on=True)
        self.grid_columnconfigure(5, weight=2)

    # Devuelve la información introducida en pantalla dentro de la estructura de datos InputRecord
    def get_input(self):
        return InputRecord(self.colour_entry.get(),
                           self.change_start_time_label.cget("text"),
                           self.colour_start_time_label.cget("text"),
                           self.colour_end_time_label.cget("text"),
                           self.hangers_entry.get(),
                           self.observations_entry.get())

    # Resetea la vista.
    # Si el campo change_start_date_time no está vacío, lo actualiza como "Hora inicio cambio".
    # Si el campo force_end es True, añadimos "FIN" al color
    def reset(self, change_start_date_time="", force_end=False):
        self.__reset_buttons()
        self.__reset_leds()
        self.__clear_input(force_end, change_start_date_time)

        if change_start_date_time != "":
            self.__update_ui_on_change_start_time_click()
        # Al pulsar el botón "Registrar y FIN" los campos a habilitar y deshabilitar son diferentes (tanto botones como LEDs), así que lo actualizo con este "if".
        if force_end:
            self.colour_start_time_button.config(state=DISABLED)
            self.colour_end_time_button.config(state=NORMAL)
            self.led_colour_start_time.to_green(on=True)
            self.observations_entry.config(state=DISABLED) # Esta línea no funciona y no entiendo muy bien el por qué.

    def reset_break(self, change_start_date_time="", force_end=False):
        self.__reset_buttons()
        self.__reset_leds()
        self.__clear_input_break(change_start_date_time)

        # Al pulsar el botón "Registrar y FIN" los campos a habilitar y deshabilitar son diferentes (tanto botones como LEDs), así que lo actualizo con este "if".

    # Devuelve una lista con errores. Si la lista devuelta está vacía, significa que no hay errores.
    # La validación se realiza en el mismo orden en el que se muestran los diferentes campos,
    # es decir, se valida el color y después la hora de inicio de cambio y así sucesivamente.
    def is_input_valid(self):
        return validator.is_input_valid(self.get_input(), self.colour_map)

    def __on_change_start_time_click(self):
        date = self.__get_now_as_formatted_date_time()
        self.change_start_date_time.set(date)
        self.__update_ui_on_change_start_time_click()

    def __update_ui_on_change_start_time_click(self):
        # Habilitamos el siguiente campo
        self.change_start_time_button.config(state=DISABLED)
        self.colour_start_time_button.config(state=NORMAL)
        self.colour_end_time_button.config(state=DISABLED)

        # Actualizamos el led conforme a la información introducida
        validation = validator.validate_time(self.change_start_date_time.get())
        self.__update_led_by_validation_type(self.led_change_start_time, validation.type)

    def __on_colour_start_time_click(self):
        date = self.__get_now_as_formatted_date_time()
        self.colour_start_date_time.set(date)
        self.__update_ui_on_colour_start_time_click()

    def __update_ui_on_colour_start_time_click(self):
        self.change_start_time_button.config(state=DISABLED)
        self.colour_start_time_button.config(state=DISABLED)
        self.colour_end_time_button.config(state=NORMAL)
        validation = validator.validate_time(self.colour_start_date_time.get())
        self.__update_led_by_validation_type(self.led_colour_start_time, validation.type)

    def __on_colour_end_time_click(self):
        date = self.__get_now_as_formatted_date_time()
        self.colour_end_date_time.set(date)
        self.__update_ui_on_colour_end_time_click()

    def __update_ui_on_colour_end_time_click(self):
        self.change_start_time_button.config(state=DISABLED)
        self.colour_start_time_button.config(state=DISABLED)
        self.colour_end_time_button.config(state=DISABLED)
        validation = validator.validate_time(self.colour_end_date_time.get())
        self.__update_led_by_validation_type(self.led_colour_end_time, validation.type)

    def __validate_colour_input(self, final_value_if_allowed):
        # Limitamos el campo a 8 caracteres
        if len(final_value_if_allowed) > 8:
            return False

        # Actualizamos el led
        validation = validator.validate_colour(final_value_if_allowed, self.colour_map)
        self.__update_led_by_validation_type(self.led_colour, validation.type)

        # Actualizamos el nombre del color
        colour_name = self.colour_map.get(final_value_if_allowed)
        if colour_name is not None:
            self.colour_name.set(colour_name)
        else:
            self.colour_name.set("")

        return True

    def __validate_hangers_input(self, value_if_allowed, input_text):
        # Limitamos el campo a solo números y como máximo de dos dígitos
        if not input_text.isdecimal():
            return False
        if len(value_if_allowed) > 2:
            return False

        # Actualizamos el led
        validation = validator.validate_hangers(value_if_allowed, self.colour_entry.get())
        self.__update_led_by_validation_type(self.led_hangers, validation.type)

        return True

    def __validate_observations_input(self, final_value_if_allowed):
        # Limitamos el campo a 50 caracteres
        if len(final_value_if_allowed) > 50:
            return False

        # Actualizamos el led
        validation = validator.validate_observations(final_value_if_allowed, self.colour_entry.get())
        self.__update_led_by_validation_type(self.led_observations, validation.type)

        return True

    def __reset_buttons(self):
        self.change_start_time_button.config(state=NORMAL)
        self.colour_start_time_button.config(state=DISABLED)
        self.colour_end_time_button.config(state=DISABLED)

    def __reset_leds(self):
        self.led_colour.to_grey(on=True)
        self.led_change_start_time.to_grey(on=True)
        self.led_colour_start_time.to_grey(on=True)
        self.led_colour_end_time.to_grey(on=True)
        self.led_hangers.to_grey(on=True)
        self.led_observations.to_grey(on=True)

    def __clear_input(self, force_end, change_start_date_time=""):
        self.colour_entry.delete(0, "end")
        # No acabo de entender esta línea, como que si "Falso"? El qué es falso??
        if force_end: # Al pulsar el botón "Registrar y FIN", la hora inicio cambio e inicio color se deben actualizar con la hora de fin del color anterior.
            self.colour_entry.insert(0, "FIN")
            self.change_start_date_time.set(change_start_date_time)
            self.colour_start_date_time.set(change_start_date_time)
            self.colour_end_date_time.set("")
            self.hangers_entry.delete(0, "end")
            self.observations_entry.delete(0, "end")

        else:
            self.change_start_date_time.set(change_start_date_time)
            self.colour_start_date_time.set("")
            self.colour_end_date_time.set("")
            self.hangers_entry.delete(0, "end")
            self.observations_entry.delete(0, "end")

    # Como la función anterior no entiendo bien cómo funciona...hago una nueva para el descanso.
    def __clear_input_break(self, change_start_date_time=""):
        self.colour_entry.delete(0, "end")
        self.change_start_date_time.set("")
        self.colour_start_date_time.set("")
        self.colour_end_date_time.set("")
        self.hangers_entry.delete(0, "end")
        self.observations_entry.delete(0, "end")

    def __get_now_as_formatted_date_time(self):
        return datetime.now().strftime(DATE_TIME_FORMAT)

    def __update_led_by_validation_type(self, led, validation_type):
        if validation_type == ValidationType.EMPTY:
            led.to_grey(on=True)
        elif validation_type == ValidationType.INVALID:
            led.to_red(on=True)
        else:
            led.to_green(on=True)

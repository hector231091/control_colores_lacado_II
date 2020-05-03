from data import Validation, ValidationType


def validate_time(text):
    if len(text) == 0:
        return Validation(ValidationType.EMPTY, "Algún campo de registro de tiempo está vacío.")
    else:
        return Validation(ValidationType.VALID)


def validate_colour(text, colour_list):
    if len(text) == 0:
        return Validation(ValidationType.EMPTY, "El campo \"Color\" está vacío.")
    elif text in colour_list:
        return Validation(ValidationType.VALID)
    else:
        return Validation(ValidationType.INVALID, "El color que se ha introducido no existe.")


def validate_hangers(text, colour_entry):
    if colour_entry == "FIN":
        if len(text) == 0:
            return Validation(ValidationType.VALID)
        else:
            return Validation(ValidationType.INVALID,
                              "El campo \"Nº de bastidores\" debe permanecer vacío cuando se especifica FIN.")
    else:
        if len(text) == 0:
            return Validation(ValidationType.EMPTY, "El campo \"Nº de bastidores\" está vacío.")
        elif len(text) == 1:
            if text == "0":
                return Validation(ValidationType.INVALID, "No pueden haber 0 bastidores.")
            else:
                return Validation(ValidationType.VALID)
        else:
            if text == "00":
                return Validation(ValidationType.INVALID, "00 no es un nº de bastidor válido")
            else:
                if text[0] == "0":
                    return Validation(ValidationType.INVALID, "La cantidad de bastidores no puede empezar por cero.")
                else:
                    return Validation(ValidationType.VALID)


def validate_observations(text, colour_entry):
    if colour_entry == "OTRO":  # El color aún no ha sido codificado, usamos la palabra especial OTRO
        if len(text) == 0:
            return Validation(ValidationType.INVALID, "Falta poner el color en las observaciones.")
    elif len(text) == 0:
        return Validation(ValidationType.EMPTY, "El campo \"Observaciones\" está vacío.")
    else:
        return Validation(ValidationType.VALID)


# Devuelve una lista con errores. Si la lista devuelta está vacía, significa que no hay errores.
# La validación se realiza en el mismo orden en el que se muestran los diferentes campos,
# es decir, se valida el color y después la hora de inicio de cambio y así sucesivamente.
def is_input_valid(input_record, colour_list):
    colour_validation = validate_colour(input_record.colour_code, colour_list)
    change_validation = validate_time(input_record.change_start_time)
    colour_start_validation = validate_time(input_record.colour_start_time)
    colour_end_validation = validate_time(input_record.colour_end_time)
    hangers_validation = validate_hangers(input_record.hangers_amount, input_record.colour_code)
    observations_validation = \
        validate_observations(input_record.observations, input_record.colour_code)

    errors = []
    if colour_validation.type != ValidationType.VALID:
        errors.append(colour_validation.message)
    if change_validation.type != ValidationType.VALID:
        errors.append(change_validation.message)
    if colour_start_validation.type != ValidationType.VALID:
        errors.append(colour_start_validation.message)
    if colour_end_validation.type != ValidationType.VALID:
        errors.append(colour_end_validation.message)
    if hangers_validation.type != ValidationType.VALID:
        errors.append(hangers_validation.message)
    if observations_validation.type == ValidationType.INVALID:
        errors.append(observations_validation.message)
    return errors

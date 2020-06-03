import enum


class Record:
    def __init__(self,
                 id,
                 colour_code,
                 change_start_time,
                 colour_start_time,
                 colour_end_time,
                 hangers_amount,
                 observations):
        self.id = id
        self.colour_code = colour_code
        self.change_start_time = change_start_time
        self.colour_start_time = colour_start_time
        self.colour_end_time = colour_end_time
        self.hangers_amount = hangers_amount
        self.observations = observations


class InputRecord:
    def __init__(self,
                 colour_code,
                 change_start_time,
                 colour_start_time,
                 colour_end_time,
                 hangers_amount,
                 observations):
        self.colour_code = colour_code
        self.change_start_time = change_start_time
        self.colour_start_time = colour_start_time
        self.colour_end_time = colour_end_time
        self.hangers_amount = hangers_amount
        self.observations = observations


class ChangeTime:
    def __init__(self,
                 change,
                 time):
        self.change = change
        self.time = time


class Colour:
    def __init__(self,
                 code,
                 name):
        self.code = code
        self.name = name


class Validation:
    def __init__(self, v_type, message=""):
        self.type = v_type
        self.message = message


class ValidationType(enum.Enum):
    VALID = 1
    INVALID = 2
    EMPTY = 3


class RegisterMode(enum.Enum):
    CONTINUE = 1  # Para continuar registrando a continuación
    END = 2  # Para finalizar y cerrar el programa
    BREAK = 3  # Para tomar un descanso

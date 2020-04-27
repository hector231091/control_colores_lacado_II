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

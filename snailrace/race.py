import uuid


class SnailraceRace:
    def __init__(self):
        self.race_id = str(uuid.uuid4())[-11:]
        self.host = ""

        self._snails = []


        self.finished = False
        self.winner = None
       
    

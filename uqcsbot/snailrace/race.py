
import datetime
from enum import Enum
from discord import Interaction

from .snail import Snail


class RaceStatus(Enum):
    OPEN = 0
    CLOSED = 1
    STARTED = 2
    FINISHED = 3

class Race:
    def __init__(self, race_id: str, host: Snail):
        """
        Lets launch a new race!
        """

        self.race_id = race_id
        self.racers = [host]

        self.status = RaceStatus.OPEN
        self.open_time = datetime.datetime.now()
        self.open_interaction = None
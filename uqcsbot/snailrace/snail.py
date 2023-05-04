import random
from enum import Enum

from uqcsbot.snailrace.user import User

class SnailMood(Enum):
    SAD = -1
    HAPPY = 0
    FOCUSED = 1

    def generateBias(self):
        return random.uniform(-1.0 + self.value, 1.0 + self.value)

    def __str__(self):
        return self.name.lower()


class SnailStats:
    speed: int
    stamina: int
    weight: int


class Snail:
    id: int
    name: str
    level: int
    experience: int

    wins: int
    races: int

    owner: User
    original_owner: User

    stats: SnailStats
    mood: SnailMood

    _position: int
    _last_step: int

    def __init__(self):
        self._position = 0
        self._last_step = 0

    def step(self):
        # Generate Random Bias
        bias = self.mood.generateBias()

        # Calculate base interval before bias and acceleration
        max_step = 10 + self.stats.speed
        min_step = min(self.stats.stamina, max_step - 5)
        avg_step = (max_step + min_step) / 2

        # Calculate acceleration factor with weight and prevStep
        acceleration = (self.stats.weight - 5) / 5 + (self._last_step - avg_step) / 5
        min_step = max(min_step + (-1 if self.stats.weight < 5 else 1) * acceleration + bias, 0)
        max_step = min(max_step + (1 if self.stats.weight < 5 else -1) * acceleration + bias, 20)

        # Calculate new position
        self._last_step = random.uniform(min_step, max_step)
        self._position = min(self._positionposition + self._last_step, 100)

    def __str__(self):
        return '''{name} (lvl {level} - {experience}xp)'''
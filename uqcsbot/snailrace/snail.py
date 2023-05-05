import random, uuid
from enum import Enum

# from uqcsbot.snailrace.user import User


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

    # owner: User
    # original_owner: User

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
        min_step = max(
            min_step + (-1 if self.stats.weight < 5 else 1) * acceleration + bias, 0
        )
        max_step = min(
            max_step + (1 if self.stats.weight < 5 else -1) * acceleration + bias, 20
        )

        # Calculate new position
        self._last_step = random.uniform(min_step, max_step)
        self._position = min(self._positionposition + self._last_step, 100)

    def __str__(self):

        sp_bar = "Speed: ".ljust(10) + "[%s]" % ("=" * int(self.stats.speed)).ljust(10)
        st_bar = "Stamina: ".ljust(10) + "[%s]" % ("=" * int(self.stats.stamina)).ljust(10)
        wt_bar = "Weight: ".ljust(10) + "[%s]" % ("=" * int(self.stats.weight)).ljust(10)

        return "%s (lvl %d - %dxp)\n\t%s\n\t%s\n\t%s\n\t" % (self.name, self.level, self.experience, sp_bar, st_bar, wt_bar)

def NewSnail() -> Snail:
    snail = Snail()
    snail._position = 0
    snail._last_step = 0

    # Generate Random Name
    with open("./snail_adj.txt") as adj, open("./snail_noun.txt") as noun:
        adjectives = adj.readlines()
        nouns = noun.readlines()
        snail.name = random.choice(adjectives).strip() + "-" + random.choice(nouns).strip()

    # Generate Random Stats
    snail.stats = SnailStats()
    snail.stats.speed = random.randint(1, 10)
    snail.stats.stamina = random.randint(1, 10)
    snail.stats.weight = random.randint(1, 10)

    # Set Mood
    snail.mood = SnailMood.HAPPY

    snail.level = 1
    snail.experience = 0
    snail.wins = 0
    snail.races = 0

    return snail

def LoadSnail(id: str) -> Snail | None:
    # Fetch snail from database using id
    return None

def GetOdds(index: int, entrants: list[Snail]) -> float:
        # Sanity check
        if index < 0 or index >= len(entrants):
            return 0.0
        
        # Get the snail
        snail = entrants[index]

        # Pre-calculate values
        sp_norm = snail.stats.speed / sum([snail.stats.speed for snail in entrants])
        st_norm = snail.stats.stamina / sum([snail.stats.stamina for snail in entrants])

        win_rate = 1
        if snail.wins != 0:
            win_rate = 1.0 - (snail.wins / snail.races)
            if win_rate == 0:
                return 10.0 * (1 - (sp_norm + st_norm)) 

        # Calculate odds
        return 10.0 * win_rate * (1 - (sp_norm + st_norm))



# Testing stuff locally

snails = [NewSnail() for i in range(10)]

for i in range(len(snails)):

    snails[i].races = random.randint(1, 10)
    snails[i].wins = random.randint(1, snails[i].races)
    winrate = (snails[i].wins / snails[i].races) * 100.0

    print(snails[i])
    print("\tOdds: %f" % GetOdds(i, snails))
    print("\tw/l: %.02f%%\n" % winrate)
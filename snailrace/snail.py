import random, discord, datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, Integer, String, Time

from uqcsbot import bot

from uqcsbot.models import Base

# ===============================
#      Snail Mood Constants
# ===============================

SNAIL_MOOD_SAD = -1
SNAIL_MOOD_HAPPY = 0
SNAIL_MOOD_FOCUSED = 1

# ===============================
#      Snail Stat Constants
# ===============================

SNAIL_STAT_MIN = 1
SNAIL_STAT_MAX = 10
SNAIL_STAT_STARTER_MIN = 1
SNAIL_STAT_STARTER_MAX = 5
SNAIL_STAT_HIGHER_MIN = 5
SNAIL_STAT_HIGHER_MAX = 10

def generateMoodBias(mood: int) -> float:
    """
    Generates a random mood bias for a snail
    """
    return random.uniform(-1.0 + self.value, 1.0 + self.value)


# ===============================
#     Snail Logic and Record
# ===============================

class SnailraceSnail(Base):
    __tablename__ = 'snailrace_snails'

    # Snail Metadata
    id = Column("id", BigInteger, primary_key=True, nullable=False)
    name = Column("name", String, nullable=False)
    owner_id = Column("owner_id", BigInteger, nullable=False)
    created_at = Column("created_at", DateTime, nullable=False)

    # Snail progress stats
    level = Column("level", BigInteger, nullable=False)
    experience = Column("experience", BigInteger, nullable=False)
    races = Column("races", BigInteger, nullable=False)
    wins = Column("wins", BigInteger, nullable=False)

    # Stats that are used to calculate the snails's speed
    mood = Column("mood", Integer, nullable=False)
    speed = Column("speed", Integer, nullable=False)
    stamina = Column("stamina", Integer, nullable=False)
    weight = Column("weight", Integer, nullable=False)

    _race_position = 0
    _race_last_step = 0

    def initialiseSnailDefaults(self, owner_id: int):
        # Create a new user object
        self.owner_id = owner_id
        self.created_at = datetime.datetime.now()
        self.mood = SNAIL_MOOD_HAPPY
        self.level = 1
        self.experience = 0
        self.races = 0
        self.wins = 0

        # Generate Random Name
        with open("./snailrace/res/snail_adj.txt") as adj, open("./snailrace/res/snail_noun.txt") as noun:
            adjectives = adj.readlines()
            nouns = noun.readlines()
            self.name = random.choice(adjectives).strip() + "-" + random.choice(nouns).strip()

    def initialiseStarterSnail(self, owner_id: int):
        self.initialiseSnailDefaults(owner_id)

        # Set snail stats
        self.speed = random.randint(SNAIL_STAT_STARTER_MIN, SNAIL_STAT_STARTER_MAX)
        self.stamina = random.randint(SNAIL_STAT_STARTER_MIN, SNAIL_STAT_STARTER_MAX)
        self.weight = random.randint(SNAIL_STAT_STARTER_MIN, SNAIL_STAT_STARTER_MAX)

    def initialiseHigherSnail(self, owner_id: int):
        self.initialiseSnailDefaults(owner_id)

        # Set snail stats
        self.speed = random.randint(SNAIL_STAT_HIGHER_MIN, SNAIL_STAT_HIGHER_MAX)
        self.stamina = random.randint(SNAIL_STAT_HIGHER_MIN, SNAIL_STAT_HIGHER_MAX)
        self.weight = random.randint(SNAIL_STAT_HIGHER_MIN, SNAIL_STAT_HIGHER_MAX)

    def initialiseRandomSnail(self, owner_id: int):
        self.initialiseSnailDefaults(owner_id)

        # Set snail stats
        self.speed = random.randint(SNAIL_STAT_MIN, SNAIL_STAT_MAX)
        self.stamina = random.randint(SNAIL_STAT_MIN, SNAIL_STAT_MAX)
        self.weight = random.randint(SNAIL_STAT_MIN, SNAIL_STAT_MAX)

    def step(self):
        # Generate Random Bias
        bias = generateMoodBias(self.mood)

        # Calculate base interval before bias and acceleration
        max_step = 10 + self.speed
        min_step = min(self.stamina, max_step - 5)
        avg_step = float(max_step + min_step) / 2.0

        # Calculate acceleration factor with weight and prevStep
        acceleration = float(self.weight - 5) / 5.0 + float(self._last_step - avg_step) / 5.0
        min_step = max(
            0,
            min_step + (-1 if self.weight < 5 else 1) * acceleration + bias
        )
        max_step = min(
            20,
            max_step + (1 if self.weight < 5 else -1) * acceleration + bias
        )

        # Calculate new position
        self._last_step = random.uniform(min_step, max_step)
        self._position = min(self._positionposition + self._last_step, 100)
    
    def getStatString(self) -> str:
        speedStr = "Speed".ljust(9) + f"[{self.speed * '#'}{(SNAIL_STAT_MAX - self.speed) * ' '}]"
        staminaStr = "Stamina".ljust(9) + f"[{self.stamina * '#'}{(SNAIL_STAT_MAX - self.stamina) * ' '}]"
        weightStr = "Weight".ljust(9) + f"[{self.weight * '#'}{(SNAIL_STAT_MAX - self.weight) * ' '}]"
        return f"{speedStr}\n{staminaStr}\n{weightStr}\n"

    def __str__(self) -> str:
        return f"{self.name} (<@{self.owner_id}>)"


def GetSnail(bot_handle: bot.UQCSBot, user: discord.User, snail_id: int) -> SnailraceSnail | None:
    """
    Gets all snails owned by a user
    """
    
    # Get user from database
    db_session = bot_handle.create_db_session()
    snail = db_session.query(SnailraceSnail).filter(SnailraceSnail.owner_id == user.id and SnailraceSnail.id == snail_id).first()
    db_session.close()

    return snail

def GetSnails(bot_handle: bot.UQCSBot, user: discord.User) -> set[SnailraceSnail]:
    """
    Gets all snails owned by a user
    """
    
    # Get user from database
    db_session = bot_handle.create_db_session()
    snails = db_session.query(SnailraceSnail).filter(SnailraceSnail.owner_id == user.id)
    db_session.close()

    return set(snails)

def CreateSnail(bot_handle: bot.UQCSBot, user: discord.User) -> SnailraceSnail:
    """
    Creates a new snail in the database
    """
    
    # Create a new user object
    new_snail = SnailraceSnail()
    new_snail.initialiseStarterSnail(user.id)

    # Add user to database
    db_session = bot_handle.create_db_session()
    db_session.add(new_snail)
    db_session.commit()
    db_session.refresh(new_snail)
    db_session.close()

    return new_snail

def GenerateSnailOdd(snail_index: int, snails: set[SnailraceSnail]) -> float:
    """
    What are the chances of a snail winning? Generate the odds of a specific 
    in the snails set.
    """
    # Sanity check
    if snail_index < 0 or snail_index >= len(snails):
        return 0.0
    
    # Get the snail
    snail = snails[snail_index]

    # Pre-calculate values
    sp_norm = snail.speed / sum([snail.speed for snail in snails])
    st_norm = snail.stamina / sum([snail.stamina for snail in snails])

    win_rate = 1
    if snail.wins != 0:
        win_rate = 1.0 - (snail.wins / snail.races)
        if win_rate == 0:
            return 10.0 * (1 - (sp_norm + st_norm)) 

    # Calculate odds
    return 10.0 * win_rate * (1 - (sp_norm + st_norm))
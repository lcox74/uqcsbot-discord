import random

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, Integer, String, Time

from discord import User
from uqcsbot import bot

Base = declarative_base()

# ===============================
#      Snail Mood Constants
# ===============================

SNAIL_MOOD_SAD = -1
SNAIL_MOOD_HAPPY = 0
SNAIL_MOOD_FOCUSED = 1

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
    created_ad = Column("created_at", DateTime, nullable=False)

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
            min_step + (-1 if self.weight < 5 else 1) * acceleration + bias, 0
        )
        max_step = min(
            max_step + (1 if self.weight < 5 else -1) * acceleration + bias, 20
        )

        # Calculate new position
        self._last_step = random.uniform(min_step, max_step)
        self._position = min(self._positionposition + self._last_step, 100)


def GetSnail(bot_handle: bot.UQCSBot, user: discord.User) -> SnailraceSnail | None:
    """
    Gets all snails owned by a user
    """
    
    # Get user from database
    db_session = bot_handle.create_db_session()
    snails = db_session.query(SnailraceSnail).filter(SnailraceSnail.owner_id == user.id)
    db_session.close()

    return set(snails)

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
    new_snail.owner_id = user.id

    # Generate Random Name
    with open("./uqcsbot/snailrace/res/snail_adj.txt") as adj, open("./uqcsbot/snailrace/res/snail_noun.txt") as noun:
        adjectives = adj.readlines()
        nouns = noun.readlines()
        new_snail.name = random.choice(adjectives).strip() + "-" + random.choice(nouns).strip()

    # Set snail stats
    new_snail.speed = random.randint(1, 10)
    new_snail.stamina = random.randint(1, 10)
    new_snail.weight = random.randint(1, 10)

    # Add user to database
    db_session = bot_handle.create_db_session()
    db_session.add(new_snail)
    db_session.commit()
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
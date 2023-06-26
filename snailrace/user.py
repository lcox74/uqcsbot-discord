from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, Integer, String, Time

import discord
from uqcsbot import bot
from uqcsbot.models import Base

from snailrace.snail import CreateSnail

STARTING_MONEY = 10

class SnailraceUser(Base):
    __tablename__ = 'snailrace_users'

    # User Discord
    id = Column("user_id", BigInteger, primary_key=True, nullable=False) 

    # Snail to use by default
    default_snail_id = Column("default_snail_id", BigInteger, nullable=True)

    # User progress stats
    level = Column("level", BigInteger, nullable=False)
    experience = Column("experience", BigInteger, nullable=False)
    races = Column("races", BigInteger, nullable=False)
    wins = Column("wins", BigInteger, nullable=False)
    money = Column("money", BigInteger, nullable=False)

    def valid(self) -> bool:
        """
        Checks if the user object is valid and initialised
        """
        return (self.id is not None) and (self.default_snail_id is not None)



def GetUser(bot_handle: bot.UQCSBot, user: discord.User, create: bool = False) -> SnailraceUser | None:
    """
    Gets a user from the database. If the user does not exist, creates a new user.
    """
    
    # Get user from database
    db_session = bot_handle.create_db_session()
    user = db_session.query(SnailraceUser).filter(SnailraceUser.id == user.id).first()
    db_session.close()

    # If user does not exist, create a new user
    if user is None and create: 
        return CreateUser(bot, user)
    
    return user

def CreateUser(bot_handle: bot.UQCSBot, user: discord.User) -> SnailraceUser | None:
    """
    Creates a new user in the database
    """
    
    # Create a new user object
    new_user = SnailraceUser()
    new_user.id = user.id
    new_user.level = 1
    new_user.experience = 0
    new_user.races = 0
    new_user.wins = 0
    new_user.money = STARTING_MONEY

    # Add user to database
    db_session = bot_handle.create_db_session()
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)
    db_session.close()

    print("new user:", new_user.id)

    # Create a random snail for the user
    new_snail = CreateSnail(bot_handle, user)
    if new_snail is None:
        return None
    
    # Set the user's default snail
    SetUserDefaultSnail(bot_handle, user, new_snail.id)

    return GetUser(bot_handle, user)

def SetUserDefaultSnail(bot_handle: bot.UQCSBot, user: discord.User, snail_id: int) -> bool:
    """
    Sets the user's default snail
    """
    # Get user from database
    db_session = bot_handle.create_db_session()
    user = db_session.query(SnailraceUser).filter(SnailraceUser.id == user.id).first()

    # If user does not exist, return false
    if user is None:
        return False

    # Set user's default snail
    user.default_snail_id = snail_id

    # Update user in database
    db_session.add(user)
    db_session.commit()
    db_session.close()

    return True
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, Integer, String, Time

from discord import User
from uqcsbot import bot

Base = declarative_base()


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



def GetUser(bot_handle: bot.UQCSBot, user: discord.User) -> SnailraceUser:
    """
    Gets a user from the database. If the user does not exist, creates a new user.
    """
    
    # Get user from database
    db_session = bot_handle.create_db_session()
    user = db_session.query(SnailraceUser).filter(SnailraceUser.id == user.id).first()
    db_session.close()

    # If user does not exist, create a new user
    if user is None: 
        return CreateUser(bot, user)
    
    return user

def CreateUser(bot_handle: bot.UQCSBot, user: discord.User) -> SnailraceUser:
    """
    Creates a new user in the database
    """
    
    # Create a new user object
    new_user = SnailraceUser()
    new_user.id = user.id

    # Add user to database
    db_session = bot_handle.create_db_session()
    db_session.add(new_user)
    db_session.commit()
    db_session.close()

    # TODO: Create a snail for the user

    return new_user
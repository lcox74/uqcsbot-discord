from typing import List
from uqcsbot.snailrace.snail import Snail

from discord import User


class User:
    id: int
    level: int
    experience: int

    wins: int
    races: int

    _default_snail: Snail
    _snails: List[Snail]

    @staticmethod
    def Load(user: discord.User):
        pass
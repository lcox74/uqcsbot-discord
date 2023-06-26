import discord, uuid, random

from uqcsbot import bot

from snailrace.snail import SnailraceSnail

RACE_STATE = {
    "RACE_OPEN": 0,
    "BETS_OPEN": 1,
    "RACE_CLOSED": 2,
    "COMPLETED": 3
}

class SnailraceRace:
    def __init__(self, no_bets: bool, dont_fill: bool, only_one: bool):
        self.discord_message = None
        self.race_id = str(uuid.uuid4())[-11:]
        self.host = ""

        self._snails = []
        self._state = RACE_STATE["RACE_OPEN"]

        self.finished = False
        self.winner = None

        with open("./snailrace/res/race_locations.txt") as locations:
            self.location = random.choice(locations.readlines()).strip()

        # Set Flags
        self.no_bets = no_bets
        self.dont_fill = dont_fill
        self.only_one = only_one
    
    def regenId(self) -> str:
        self.race_id = str(uuid.uuid4())[-11:]
        return self.race_id

    def addSnail(self, snail: SnailraceSnail) -> bool:
        if snail in self._snails:
            return False

        if len(self._snails) >= 12:
            return False

        self._snails.append(snail)
        return True

    async def renderInitial(self, bot_handle: bot.UQCSBot, interaction: discord.Interaction):
        generate_message = ("# **Race: Open**\nA new race has been hosted by "
            f"{interaction.user.mention}\n\nRace ID: `{self.race_id}`\n"
            f"Location: `{self.location}`\n\nTo join via command, enther the "
            f"following:\n```\n/snailrace join {self.race_id}\n```\n"
            f"**Entrants: ({len(self._snails)}/12)**\n")
        
        for snail in range(len(self._snails)):
            # Get user from snail
            generate_message += f"{snail}. {self._snails[snail]}\n"

        await interaction.response.send_message(generate_message)
    
    def setMessage(self, response: discord.InteractionResponse):
        self.discord_message = response

    def __eq__(self, other) -> bool:
        return self.race_id == other.race_id

       
    

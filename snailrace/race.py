import discord, uuid, random

from discord import ui

from uqcsbot import bot

from snailrace.user import GetUser
from snailrace.snail import SnailraceSnail
from snailrace.embed_responses import *

RACE_STATE = {
    "RACE_OPEN": 0,
    "BETS_OPEN": 1,
    "RACE_CLOSED": 2,
    "COMPLETED": 3
}

# Trying out Discord buttons for Snail Race Interactions
class SnailRaceView(discord.ui.View):
    def __init__(self, joinCb):
        super().__init__()
        self.joinCb = joinCb

    @ui.button(label="Join Race", style=discord.ButtonStyle.primary)
    async def button_callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await self.joinCb(interaction)



class SnailraceRace:
    def __init__(self, bot_handle: bot.UQCSBot, host: str, no_bets: bool, dont_fill: bool, only_one: bool):
        self.discord_message = None
        self.race_id = str(uuid.uuid4())[-11:]
        self.host = host
        self.bot = bot_handle

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

    async def joinCb(self, interaction: discord.Interaction):
        get_user = GetUser(self.bot, interaction.user)
        if get_user is None:
            await interaction.response.send_message(
                embed=NOT_INIT_USER(interaction.user.name, "/snailrace join"), 
                ephemeral=True
            )
            return

        if not self.addSnail(get_user.cacheSnail):
            await interaction.response.send_message(
                embed=ALREADY_JOINED_OR_FULL(interaction.user.name), 
                ephemeral=True
            )
            return
        
        await interaction.response.send_message(
            embed=JOIN_SUCCESS(interaction.user.name), ephemeral=True
            
        )
        await self.renderOpen(interaction)

    def getOpenRaceEmbed(self) -> discord.Embed:
        embed = RACE_OPEN(self)
        
        for snail in range(len(self._snails)):
            # Get user from snail
            embed.description += f"{snail}. {self._snails[snail]}\n"

        return embed

    async def renderOpen(self, interaction: discord.Interaction):
        embed = self.getOpenRaceEmbed()

        if self.discord_message is None:
            self.discord_message = await interaction.channel.send(embed=embed, view=SnailRaceView(self.joinCb))
            return

        await self.discord_message.edit(embed=embed, view=SnailRaceView(self.joinCb))
    
    def setMessage(self, response: discord.InteractionResponse):
        self.discord_message = response

    def __eq__(self, other) -> bool:
        return self.race_id == other.race_id

       
    

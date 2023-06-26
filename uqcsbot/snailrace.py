import discord, asyncio
from discord import app_commands, ui

from discord.ext import commands
from uqcsbot.bot import UQCSBot
from typing import Optional

from snailrace.user import GetUser, CreateUser, CreateStarterSnail
from snailrace.race import SnailraceRace
from snailrace.embed_responses import *

class SnailRace(commands.Cog):
    snailrace_group = app_commands.Group(name="snailrace", description="Snailrace commands")

    def __init__(self, bot: UQCSBot):
        self.bot = bot
        self.active_races: [SnailraceRace] = []

    @snailrace_group.command(
        name="init",
        description="Are you a new user? Run this command to create your account."
    )
    async def initialise_user(self, interaction: discord.Interaction):
        """
        Initialises a user for snailrace. This will also create a snail for the
        user and set it as their default snail.
        """

        # Check if user is already initialised
        user = GetUser(self.bot, interaction.user)
        if user is not None:
            # Check if the user has a snail
            if not user.hasSnail():
                # Try and create a snail for the user
                if CreateStarterSnail(self.bot, interaction.user, user) is None:
                    await interaction.response.send_message(
                        embed=INIT_FAILED(interaction.user.name)
                    )
                    return
                    
            await interaction.response.send_message(
                embed=EXISTING_USER(interaction.user.name, user.cacheSnail)
            )
            return

        # Create the user and load the default snail
        user = CreateUser(self.bot, interaction.user)
        if user is None:
            await interaction.response.send_message(
                embed=INIT_FAILED(interaction.user.name)
            )
            return
        
        # Check if the user has a snail
        if not user.hasSnail():
            # Try and create a snail for the user
            if CreateStarterSnail(self.bot, interaction.user, user) is None:
                await interaction.response.send_message(
                    embed=INIT_FAILED(interaction.user.name)
                )
                return

        # Send success message
        await interaction.response.send_message(
            embed=INIT_SUCCESS(interaction.user.name, user.cacheSnail)
        )

    @snailrace_group.command(
        name="host",
        description="Let's host a snailrace!",
    )
    @app_commands.describe(
        no_bets="Stops users from making bets on this race (optional)",
        dont_fill="If the race has less than 4 snails, then dont fill (optional)",
        only_one="Don't allow a draw, keep racing until there is one (optional)"
    )
    async def host_race(self, interaction: discord.Interaction,
        no_bets: Optional[bool] = False, 
        dont_fill: Optional[bool] = False,
        only_one: Optional[bool] = False
    ):
        # Check if user is exists and is initialised
        user = GetUser(self.bot, interaction.user)
        if user is None:
            await interaction.response.send_message(
                embed=NOT_INIT_USER(interaction.user.name, "/snailrace host")
            )
            return

        # Generate a new race with unique id
        new_race = SnailraceRace(no_bets, dont_fill, only_one)
        while new_race in self.active_races:
            new_race.regenId()
        
        # Add the host snail to the race
        new_race.addSnail(user.cacheSnail)
        self.active_races.append(new_race)

        # Send the initial message
        await new_race.renderInitial(self.bot, interaction)



async def setup(bot: UQCSBot):
    await bot.add_cog(SnailRace(bot))

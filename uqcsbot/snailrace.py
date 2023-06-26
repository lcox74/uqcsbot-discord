import discord, asyncio
from discord import app_commands, ui

from discord.ext import commands
from uqcsbot.bot import UQCSBot

from snailrace.user import GetUser, CreateUser, CreateStarterSnail
from snailrace.embed_responses import *

class SnailRace(commands.Cog):
    snailrace_group = app_commands.Group(name="snailrace", description="Snailrace commands")

    def __init__(self, bot: UQCSBot):
        self.bot = bot

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

async def setup(bot: UQCSBot):
    await bot.add_cog(SnailRace(bot))

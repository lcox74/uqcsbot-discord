import discord, asyncio
from discord import app_commands, ui

from discord.ext import commands
from uqcsbot.bot import UQCSBot

from snailrace.user import GetUser, CreateUser

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
        if GetUser(self.bot, interaction.user) is not None:
            await interaction.response.send_message("You are already initialised!")
            return

        # Create the user
        user = CreateUser(self.bot, interaction.user)
        if user is None or not user.valid():
            await interaction.response.send_message("Failed to initialise user!")
            return
        
        # Send success message
        await interaction.response.send_message("Successfully initialised user!")


        


async def setup(bot: UQCSBot):
    await bot.add_cog(SnailRace(bot))

import discord

class EmbedStyle:
    """Class for storing embed styles"""
    def __init__(self, color, title, description):
        self.color = color
        self.title = title
        self.description = description
    
    def compile(self) -> discord.Embed:
        return discord.Embed(
            title=self.title,
            description=self.description,
            color=self.color
        )

EXISTING_USER: discord.Embed = lambda name, snail : EmbedStyle(
    color=discord.Color.blue(),
    title=f"You are already initialised {name}!",
    description=(
        f"Your snail currently active snail is **{snail.name} (lvl. "
        f"{snail.level})** with the following stats:\n\n```\n"
        f"{snail.getStatString()}\n```\n"
    )
).compile()

INIT_SUCCESS: discord.Embed = lambda name, snail : EmbedStyle(
    color=discord.Color.green(),
    title=f"Welcome to Snailrace {name}!",
    description=(
        f"Your snail is called **{snail.name} (lvl. {snail.level})** and has the"
        f" following stats:\n\n```\n{snail.getStatString()}\n```\n"
    )
).compile()

INIT_FAILED: discord.Embed = lambda name : EmbedStyle(
    color=discord.Color.red(),
    title=f"I'm sorry {name}, but there has been an issue",
    description=(
        "There has been an issue with initialising your account. Please try "
        "again later."
    )
).compile()

NOT_INIT_USER: discord.Embed = lambda name, cmd : EmbedStyle(
    color=discord.Color.red(),
    title=f"I'm sorry {name}, but you aren't initialised yet",
    description=(
        "Please run `/snailrace init` to initialise your account. Then you can "
        f"run `{cmd}` again."
    )
).compile()

RACE_HOSTED: discord.Embed = lambda name : EmbedStyle(
    color=discord.Color.green(),
    title=f"You've just hosted a race {name}!",
    description=(
        "Your snail is officially waiting at the starting line waiting for "
        "other snails to join."
    )
).compile()

ALREADY_JOINED_OR_FULL: discord.Embed = lambda name : EmbedStyle(
    color=discord.Color.red(),
    title=f"Sorry {name}",
    description=(
        "The race you have just tried to enter is either full or you are "
        "already in it."
    )
).compile()

JOIN_SUCCESS: discord.Embed = lambda name : EmbedStyle(
    color=discord.Color.green(),
    title=f"You've joined the race {name}!",
    description=(
        "Your snail is officially waiting at the starting line."
    )
).compile()

RACE_OPEN: discord.Embed = lambda race : EmbedStyle(
    color=discord.Color.green(),
    title=f"Race: Open",
    description=(
        f"A new race has been hosted by {race.host}\n\nRace ID: `{race.race_id}"
        f"`\nLocation: `{race.location}`\n\nTo join via command, enter the "
        f"following:\n```\n/snailrace join {race.race_id}\n```\n**Entrants: "
        f"({len(race._snails)}/12)**\n")
).compile()
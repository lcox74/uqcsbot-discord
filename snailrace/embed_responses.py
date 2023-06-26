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

INIT_SUCCESS: discord.Embed = lambda name, sName, sLvl, sStat : EmbedStyle(
    color=discord.Color.green(),
    title=f"Welcome to Snailrace {name}!",
    description=(
        f"Your snail is called**{snail.name} (lvl. {snail.level})** and has the"
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
        "Please run `\snailrace init` to initialise your account. Then you can "
        f"run `{cmd}` again."
    )
).compile()
from bot.base import Command
from bot.config import Config, Embed

# Just a simple about project command, tells info about the project
# first contribution from me
# originally made by ahz


class cmd(Command):
    """A discord command instance."""

    name = "about"
    usage = "about"
    description = "Explains about the project."

    async def execute(self, arguments, message) -> None:
        embed = Embed(
            title="About me",
            description="I am a community created open source project started by Virbox, you can contribute to me by going to the Github repository. *Type `v!help` to get started!*",
            color=0x00FF00,
        )
        embed.add_field(name="Github:", value="https://github.com/v1rbox/discox")
        embed.add_field(name="Virbox Channel:", value="https://www.youtube.com/@Virbox")

        await message.channel.send(embed=embed)

from bot.base import Command
from bot.commands.distroroles.add import DistroRoles
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "list"
    usage = "list"
    description = f"Shows available distro role options"

    async def execute(self, arguments, message) -> None:
        distroroles = DistroRoles()
        embed = Embed(title="Distro", description=distroroles.getWhitelist())
        await message.channel.send(embed=embed)

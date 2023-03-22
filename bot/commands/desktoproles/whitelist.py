from bot.base import Command
from bot.commands.desktoproles.add import DesktopRoles
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "list"
    usage = "list"
    description = f"Shows available desktop role options"

    async def execute(self, arguments, message) -> None:
        desktoproles = DesktopRoles()
        embed = Embed(title="Desktop", description=desktoproles.getWhitelist())
        await message.channel.send(embed=embed)

from bot.base import Command
from bot.commands.desktoproles.add import DesktopRoles
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "leaderboard"
    usage = "leaderboard"
    description = f"Leaderboard of most used desktops in the server"

    async def execute(self, arguments, message) -> None:
        desktoproles = DesktopRoles()
        embed = Embed(title="Desktop", description=desktoproles.getLeaderboard(message))
        await message.channel.send(embed=embed)

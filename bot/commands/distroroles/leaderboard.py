from bot.base import Command
from bot.commands.distroroles.add import DistroRoles
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "leaderboard"
    usage = "leaderboard"
    description = f"Leaderboard of most used distros in the server"

    async def execute(self, arguments, message) -> None:
        distroroles = DistroRoles()
        embed = Embed(
                title="Distro",
                description=distroroles.getLeaderboard(message)
                )
        await message.channel.send(embed=embed)

        

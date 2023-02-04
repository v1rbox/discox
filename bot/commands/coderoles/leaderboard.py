from bot.base import Command
from bot.commands.coderoles.add import CodeRoles
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "leaderboard"
    usage = "leaderboard"
    description = f"Leaderboard of most used languages in the server"

    async def execute(self, arguments, message) -> None:
        coderoles = CodeRoles()
        embed = Embed(
                title="Code",
                description=coderoles.getLeaderboard(message)
                )
        await message.channel.send(embed=embed)

        

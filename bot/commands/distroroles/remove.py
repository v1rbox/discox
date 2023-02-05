from bot.base import Command
from bot.commands.distroroles.add import DistroRoles
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "remove"
    usage = "remove <distribution>"
    description = f"Removes a distro role from user"

    async def execute(self, arguments, message) -> None:
        distroroles = DistroRoles() 
        embed = Embed(
                title="Distro",
                description=await distroroles.removeRole(message, arguments[0])
                )
        await message.channel.send(embed=embed)


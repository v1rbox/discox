from bot.base import Command
from bot.commands.distroroles.add import DistroRoles
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "roles"
    usage = "roles"
    description = f"Shows user's current distro roles"

    async def execute(self, arguments, message) -> None:
       distroroles = DistroRoles() 
       embed = Embed(
                title="Distro",
                description=distroroles.getRoles(message)
                )
       await message.channel.send(embed=embed)
 

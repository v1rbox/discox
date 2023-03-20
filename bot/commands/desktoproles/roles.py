from bot.base import Command
from bot.commands.desktoproles.add import DesktopRoles
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "roles"
    usage = "roles"
    description = f"Shows user's current Desktop roles"

    async def execute(self, arguments, message) -> None:
        desktoproles = DesktopRoles()
        embed = Embed(title="Desktop", description=desktoproles.getRoles(message))
        await message.channel.send(embed=embed)

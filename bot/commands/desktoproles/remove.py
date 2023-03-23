from bot.base import Command
from bot.commands.desktoproles.add import DesktopRoles
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "remove"
    usage = "remove <distribution>"
    description = f"Removes a Desktop role from user"

    async def execute(self, arguments, message) -> None:
        desktoproles = DesktopRoles()
        embed = Embed(
            title="Desktop",
            description=await desktoproles.removeRole(message, arguments[0]),
        )
        await message.channel.send(embed=embed)

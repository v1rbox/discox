from bot.commands.distroroles.add import DistroRoles
from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "whitelist"
    usage = "whitelist"
    description = f"Shows available distro role options"

    async def execute(self, arguments, message) -> None:
        distroroles = DistroRoles()
        distroroles.getWhitelist()

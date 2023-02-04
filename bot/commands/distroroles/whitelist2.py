from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "whitelist2"
    usage = "whitelist2"
    description = f"Shows available distro role options"

    async def execute(self, arguments, message) -> None:
        pass

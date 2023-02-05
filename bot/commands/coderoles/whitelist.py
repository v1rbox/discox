from bot.base import Command
from bot.commands.coderoles.add import CodeRoles
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "whitelist"
    usage = "whitelist"
    description = f"Shows available code role options"

    async def execute(self, arguments, message) -> None:
        coderoles = CodeRoles()
        embed = Embed(title="Code", description=coderoles.getWhitelist())
        await message.channel.send(embed=embed)

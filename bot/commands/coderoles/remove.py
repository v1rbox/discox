from bot.base import Command
from bot.commands.coderoles.add import CodeRoles
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "remove"
    usage = "remove <language>"
    description = f"Removes a code role from user"

    async def execute(self, arguments, message) -> None:
        coderoles = CodeRoles() 
        embed = Embed(
                title="Code",
                description=await coderoles.removeRole(message, arguments[0])
                )
        await message.channel.send(embed=embed)


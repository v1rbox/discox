from bot.base import Command
from bot.commands.coderoles.add import CodeRoles
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "roles"
    usage = "roles"
    description = f"Shows user's current code roles"

    async def execute(self, arguments, message) -> None:
       coderoles = CodeRoles() 
       embed = Embed(
                title="Code",
                description=coderoles.getRoles(message)
                )
       await message.channel.send(embed=embed)
 

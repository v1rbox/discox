from urllib.parse import unquote

from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "list"
    usage = "list"
    description = """Lists all tags"""

    async def execute(self, arguments, message) -> None:
        tags = await self.db.raw_exec_select("SELECT * FROM tags")
        embed = Embed(title="Tags")
        for tag in tags:
            name, content = tag
            embed.add_field(
                name=f"{unquote(name)}",
                value=f"{unquote(content)}",
            )
        await message.reply(embed=embed)

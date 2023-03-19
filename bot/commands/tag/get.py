from urllib.parse import quote, unquote

from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "get"
    usage = "Get <*name>"
    description = "Gets the content of a tag"

    async def execute(self, arguments, message) -> None:
        if not len(arguments) or arguments[0] == "":
            return await self.logger.send_error("Please provide a name", message)
        name = arguments[0]
        content = await self.db.raw_exec_select(
            """SELECT Content FROM tags WHERE Name = ?""", (quote(name),)
        )
        if not len(content):
            return await self.logger.send_error(f"Tag '{name}' doesn't exist", message)
        embed = Embed(
            title=f"Tag: `{name}`", description=f"Content: '{unquote(content[0][0])}'"
        )
        await message.reply(embed=embed)

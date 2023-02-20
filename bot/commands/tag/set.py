import asyncio

from urllib.parse import quote
from bot.config import Config, Embed
from bot.base import Command

class cmd(Command):
    """ A discord command instance. """

    name = "set"
    usage = "set <*name>"
    description = "Add or update a tag"

    async def execute(self, arguments, message) -> None:
        if not len(arguments) or arguments[0] == "":
            return await self.logger.send_error("Please provide a name", message)

        embed = Embed(
            title="New Tag",
            description="What should the content of the tag be?"
        )
        await message.reply(embed=embed)

        def check(m):
            return m.author == message.author and m.channel == message.channel

        try:
            while True:
                msg = await self.bot.wait_for("message", check=check, timeout=10)
                if msg:
                    break
        except asyncio.exceptions.TimeoutError:
            return await self.logger.send_error("No content was provided", message)

        await self.db.raw_exec_commit("""INSERT INTO tags VALUES(?, ?)""", (
            quote(arguments[0]),
            quote(msg.content),
        ))

        embed = Embed(
            title="Tag set",
            description=f"Tag `{arguments[0]}` set"
        )
        await message.reply(embed=embed)

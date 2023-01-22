import asyncio

import aiosqlite
from discord.message import Message

from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):

    name = "request"
    usage = "request"
    description = (
        "Add some recommendation to the server. Support multiple commands to deal with."
    )

    async def execute(self, arguments, message) -> None:
        member_id = message.author.__repr__()

        def check(m):
            return m.channel == message.channel and m.author.id == message.author.id

        title_request = Embed(title="What is the title of the request?")
        await message.channel.send(embed=title_request)

        try:
            title = await self.bot.wait_for("message", timeout=120.0, check=check)
            description_request = Embed(
                title="What is the description of this request?"
            )

            await message.channel.send(embed=description_request)
            text_info = await self.bot.wait_for("message", timeout=120.0, check=check)

        except asyncio.TimeoutError:
            await message.channel.send("Timed out.")
            return

        await self.db.raw_exec_commit(
            "INSERT INTO request(Member_id, Title, Description) VALUES(?, ?, ?)",
            (member_id, title.content, text_info.content),
        )

        embed = Embed(title="A request has been added!")
        await message.channel.send(embed=embed)

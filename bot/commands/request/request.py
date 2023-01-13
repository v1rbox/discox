import aiosqlite

from bot.base import Command
from bot.config import Config, Embed

from discord.message import Message

class cmd(Command):

    name = "request"
    usage = "request"
    description = "Add some recommendation to the server. Support multiple commands to deal with."

    async def execute(self, arguments, message) -> None:
        member_id = message.author.__repr__()
        title_request = Embed(title="What is the title of the request?")
        await message.channel.send(embed=title_request)
        title = await self.bot.wait_for("message", timeout=60.0, check=None)
        description_request = Embed(title="What is the description of this request?")
        await message.channel.send(embed=description_request)
        text_info = await self.bot.wait_for("message", timeout=60.0, check=None)

        

        db = self.db

        cursor = await db.cursor()

        await cursor.execute(
            "INSERT INTO request(Member_id, Title, Description) VALUES(?, ?, ?)", (member_id, title.content, text_info.content)
        )

        await db.commit()

        await cursor.close()

        embed = Embed(title="A request has been added!")
        await message.channel.send(embed=embed)

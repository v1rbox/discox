import aiosqlite

from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):

    name = "request"
    usage = "request <title> [description]"
    description = "Add some recommendation to the server. Support multiple commands to deal with. \nThe [description] argument here should be a code block. "

    async def execute(self, arguments, message) -> None:

        title = arguments[0]
        text_info = arguments[1]
        member_id = message.author.__repr__()

        db = self.db

        cursor = await db.cursor()

        await cursor.execute(
            "INSERT INTO request(Member_id, Title, Description) VALUES(?, ?, ?)",
            (member_id, title, text_info),
        )
        await db.commit()

        await cursor.close()

        embed = Embed(title="A request has been added!")
        await message.channel.send(embed=embed)

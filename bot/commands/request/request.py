import aiosqlite
from bot.config import Config, Embed
from bot.base import Command


class cmd(Command):

    name = "request"
    usage = "request <title> [description]. Description here should be a code block."
    description = "Add some recommendation to the server. Support multiple commands to deal with."

    async def execute(self, arguments, message) -> None:

        title = arguments[0]
        text_info = arguments[1]
        member_id = message.author.__repr__()

        db = self.db

        cursor = await db.cursor()

        await cursor.execute(
            "INSERT INTO request(Member_id, Title, Description) VALUES(?, ?, ?)", (member_id, title, text_info))
        await db.commit()

        await cursor.close()

        embed = Embed(title="A request has been added!")
        await message.channel.send(embed=embed)

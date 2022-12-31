import aiosqlite
from bot.config import Config, Embed
from bot.base import Command


class cmd(Command):

    name = "request"
    usage = "request <title> [description]"
    description = "Add some recommendation to the server. Support multiple commands to deal with."

    async def execute(self, arguments, message) -> None:
        if len(arguments) < 2:
            raise ValueError("Not enough parameters")
        elif len(arguments) > 2:
            raise ValueError("Too many parameters")
        else:
            title = arguments[0]
            text_info = arguments[1]

        db = self.db

        cursor = await db.cursor()

        await cursor.execute(
            "INSERT INTO request(Title, Description) VALUES(?, ?)", (title, text_info))
        await db.commit()

        await cursor.close()
        await db.close()

        embed = Embed(title="A request has been added!")
        await message.channel.send(embed=embed)

        self.db = await aiosqlite.connect("bot\\assets\\main.db")

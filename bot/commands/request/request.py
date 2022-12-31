from bot.config import Config, Embed
from bot.base import Command


class cmd(Command):

    name = "request"
    usage = "request <title> [description]"
    description = "Add some recommendation to the server. Support multiple commands to deal with."

    async def execute(self, arguments, message) -> None:
        db = self.db
        user_name = message.author.__repr__()

        title = arguments[0]
        text_info = arguments[1]

        cursor = await db.cursor()

        await cursor.execute(
            "INSERT INTO request(Member_id, Title, Description) VALUES(?, ?, ?)", (user_name, title, text_info))
        await db.commit()

        await cursor.close()

        embed = Embed(title="A request has been added!")
        await message.channel.send(embed=embed)

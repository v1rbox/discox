import aiosqlite
from bot.config import Config, Embed
from bot.base import Command


class cmd(Command):

    name = "request"
    usage = "request <title> <description>"
    description = "Add some recommendation to the server. Support multiple commands to deal with."

    def implement_text_block_arguments(self, arguments) -> list[str]:
        list_arguments = []

        start_index = 0
        for i, j in enumerate(arguments):
            if j[:3] == "```":
                start_index = i

        print(start_index)

    async def execute(self, arguments, message) -> None:
        title = arguments[0]
        arguments = arguments[1:]
        if arguments[0][:3] != "```":
            raise ValueError(
                "This is not a right parameter. You have to pass a block text like this: ```block text```")

        arguments[0] = arguments[0][3:]

        arguments[len(arguments) - 1] = arguments[len(arguments) -
                                                  1][:len(arguments[len(arguments) - 1]) - 3]
        text_info = ""

        for i in arguments:
            text_info += i + " "

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

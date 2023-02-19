from urllib.parse import quote
from bot.config import Config, Embed
from bot.base import Command

class cmd(Command):
    """ A discord command instance. """

    name = "removetag"
    usage = "removetag <*name>"
    description = "Removes a tag"

    async def execute(self, arguments, message) -> None:
        if not len(arguments) or arguments[0] == "":
            return await self.logger.send_error("Please provide a name", message)
        await self.db.raw_exec_commit("""DELETE FROM tags WHERE Name = ?""", (quote(arguments[0])))
        embed = Embed(
            title="Tag removed",
            description=f"The tag '{arguments[0]}' was removed"
        )
        await message.reply(embed=embed)

from bot.config import Config, Embed
from bot.base import Command

class cmd(Command):
    """ A discord command instance. """

    name = "ping2"
    usage = "ping2"
    description = "Check the current latency of the bot for a second time lol."

    async def execute(self, arguments, message) -> None:
        raise ValueError("I cry a lot :((")
        await message.channel.send("Im alive!! :o:O")

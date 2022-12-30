from bot.config import Config, Embed
from bot.base import Command

class cmd(Command):
    """ A discord command instance. """

    name = "ping"
    usage = "ping"
    description = "Check the current latency of the bot."

    async def execute(self, arguments, message) -> None:
        embed = Embed(title="Hello world!", description="This is a test embed")
        await message.channel.send("Im alive!!", embed=embed)

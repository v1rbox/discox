from bot.config import Config, Embed
from bot.base import Command


class cmd(Command):
    """ A discord command instance. """

    name = "ping"
    usage = "ping <type> [*test3]"
    description = "Check the current latency of the bot."

    async def execute(self, arguments, message) -> None:
        if arguments[0] == "print":
            embed = Embed(
                title="Hello world!", description=f"This is a test embed\nYou typed `{arguments[1]}`")
        else:
            embed = Embed(title="Hello world!",
                          description=f"This is a test embed")
        await message.channel.send("Im alive!!", embed=embed)

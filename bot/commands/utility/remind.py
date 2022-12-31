# /bot/commands/ping.py
from bot.config import Config, Embed
from bot.base import Command
from asyncio import sleep

class cmd(Command):
    """ A discord command instance. """

    name = "remind"
    usage = "remind <reminder> [hours] [*minutes]"
    description = "Reminds the user of something."

    async def execute(self, arguments, message) -> None:
        embed = Embed(title="New Reminder", description="Reminder set!")
        await message.reply(embed=embed)
        size = len(arguments)
        if size == 2:
            time = 60*30
        elif size == 3 and arguments[2] == "":
            time = 60*60*float(arguments[1])
        else:
            time = 60*60*float(arguments[1])+60*float(arguments[2])
        await sleep(time)
        embed = Embed(title=arguments[0], description="This is your reminder.")
        await message.channel.send(f"<@{message.author.id}>", embed=embed)

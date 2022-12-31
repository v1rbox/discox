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
        await message.channel.send(embed=embed)
        minutes = float(arguments[2])
        hours = float(arguments[1])
        if hours == None:
            time = 60*30
        elif minutes == None:
            time = 60*60*hours
        else:
            time = 60*60*hours+60*minutes
        await sleep(time)
        embed = Embed(title=arguments[0], description="This is your reminder.")
        await message.channel.send(embed=embed)

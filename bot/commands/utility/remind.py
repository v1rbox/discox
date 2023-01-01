# /bot/commands/ping.py
from bot.config import Config, Embed
from bot.base import Command
from asyncio import sleep
from re import match

class cmd(Command):
    """ A discord command instance. """

    name = "remind"
    usage = "remind <time> <*reminder>"
    description = "Reminds the user of something."

    async def execute(self, arguments, message) -> None:
        timeStr = arguments[0]
        regEx = r"(?:(?P<days>\d+)d)?(?:(?P<hours>\d+)h)?(?:(?P<minutes>\d+)m)?(?:(?P<seconds>\d+)s)?"
        times = match(regEx, timeStr).groupdict()
        d = int(times["days"]) if times["days"] else 0
        h = int(times["hours"]) if times["hours"] else 0
        m = int(times["minutes"]) if times["minutes"] else 0
        s = int(times["seconds"]) if times["seconds"] else 0
        time = d * 24 * 3600 + h * 3600 + m * 60 + s
        
        embed = Embed(title="New Reminder", description="Reminder set!")
        await message.reply(embed=embed)        
        await sleep(time)
        embed = Embed(title=arguments[1], description="This is your reminder.")
        await message.channel.send(f"<@{message.author.id}>", embed=embed)

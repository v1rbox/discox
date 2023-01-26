from discord.ext import tasks
import urllib.parse as parse
from asyncio import sleep
from time import time

from bot.base import Task
from bot.config import Config, Embed


class TaskLoop(Task):
    """A discord Task instance."""

    @tasks.loop(seconds=30)
    async def execute(self):
       	reminders = await self.db.raw_exec_select("SELECT * FROM reminders ORDER BY Timestamp ASC")
        for reminder in reminders:
            user, timestamp, remindMsg, channel, message = reminder
            if (timestamp > int(time())):
                channelObj = await self.bot.fetch_channel(channel)
                url = f"https://discord.com/channels/{channelObj.guild.id}/{channel}/{message}"
                embed = Embed(title=parse.unquote(remindMsg), description=f"""This is your reminder.
If you want to know the context, [here]({url}) is the link.""")
                await channelObj.send(f"<@{user}>", embed=embed)
                await self.db.raw_exec_commit("DELETE FROM reminders WHERE User = ? AND Timestamp = ?", (user, timestamp))

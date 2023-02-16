import asyncio
import datetime
import time

from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):
    name = "send"
    usage = "send <*message>"
    description = "Reply to the user in a report"

    async def execute(self, arguments, message) -> None:
        member = message.guild.get_member(int(message.channel.name.split(" - ")[0]))
        if member is not None:
            await member.send(arguments[0])

            for a in message.attachments:
                await member.send(a.url)

            await message.add_reaction("✅")
        else:
            await message.add_reaction("❌")

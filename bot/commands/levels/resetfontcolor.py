from typing import List

import discord

from bot.base import Command


class cmd(Command):
    name = "resetfontcolor"
    description = "Reset your font color to the default."
    usage = "resetfontcolor"

    async def execute(self, arguments: List[str], message: discord.Message) -> None:
        await self.db.raw_exec_commit(
            'UPDATE levels SET font_color = "255 255 255" WHERE user_id = ?',
            (message.author.id,),
        )
        await message.channel.send("Successfully reset font color.")

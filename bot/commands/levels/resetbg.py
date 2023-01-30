import discord
from bot.base import Command
from typing import List
class cmd(Command):
    name = "resetbg"
    description = "Reset your background to the default."
    usage = "resetbg"
    
    async def execute(self, arguments: List[str], message: discord.Message) -> None:
        await self.db.raw_exec_commit("UPDATE levels SET bg = NULL WHERE user_id = ?", (message.author.id,))
        await message.channel.send("Successfully reset background.")
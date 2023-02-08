import io

import colorthief
import discord

from bot.base import Command
from bot.config import Embed


class cmd(Command):
    name = "create_truefalse_option"
    description = "Create a true false poll. Options are seperated by a commas."
    usage = "create_truefalse_option <question>"

    async def execute(self, arguments: list[str], message: discord.Message) -> None:
        question = arguments[0]
        embed = Embed(
            title=f"True false Poll: {question}",
            description=f"Forced one option poll.",
            color=colorthief.ColorThief(io.BytesIO(await message.author.avatar.read() if message.author.avatar else await message.author.default_avatar.read())).get_color(quality=1),
        )
        a = await message.channel.send(embed=embed)
        await a.add_reaction("✅")
        await a.add_reaction("❌")
        await self.db.raw_exec_commit("INSERT INTO polls (channel_id, message_id, type) VALUES (?, ?, ?)", (message.channel.id, a.id, "single"))
        
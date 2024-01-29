import io

import colorthief
import discord

from bot.base import Command
from bot.config import Colour, Embed


class cmd(Command):
    name = "create_multiple_option"
    description = (
        "Create a poll with multiple options. Options are separated by commas."
    )
    usage = "create_multiple_option <question> <is_support_single:bool> <*options>"

    bind = [
        "0️⃣",
        "1️⃣",
        "2️⃣",
        "3️⃣",
        "4️⃣",
        "5️⃣",
        "6️⃣",
        "7️⃣",
        "8️⃣",
        "9️⃣",
    ]

    async def execute(self, arguments: list[str], message: discord.Message) -> None:
        question = arguments[0]
        single = arguments[1]
        options = arguments[2].split(",")
        assert len(options) <= 10, "You can only have 10 options."
        embed = Embed(
            title=f"Poll: {question}",
            description=f"{'Single' if single else 'Multiple'} option poll.",
            color=Colour.from_rgb(
                *colorthief.ColorThief(
                    io.BytesIO(
                        await message.author.avatar.read()
                        if message.author.avatar
                        else await message.author.default_avatar.read()
                    )
                ).get_color(quality=1)
            ),
        )
        i = 0
        for option in options:
            embed.add_field(name=f"{self.bind[i]}. ", value=option, inline=False)
            i += 1
        embed.set_footer(
            text=f"Poll created by {message.author} and when {message.created_at}"
        )
        embed.set_thumbnail(
            url=(
                message.author.avatar.url
                if message.author.avatar
                else message.author.default_avatar.url
            )
        )
        a = await message.channel.send(embed=embed)
        for i in range(len(options)):
            await a.add_reaction(self.bind[i])
        await self.db.raw_exec_commit(
            "INSERT INTO polls (channel_id, message_id, type) VALUES (?, ?, ?)",
            (message.channel.id, a.id, "multiple" if single else "single"),
        )

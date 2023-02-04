from re import findall
from colorthief import ColorThief
import requests
import os
from discord import Colour

from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "poll"
    usage = "poll <question> [*options]"
    description = "Start a poll."

    async def execute(self, arguments, message) -> None:
        emojis = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        yes_no = ["✅", "❌"]
        user_input = findall(r'"(.*?)"', message.content)
        question = user_input[0]
        options = False
        if len(user_input) > 1:
            options = user_input[1:]

        avatar_color = None
        try:
            b = requests.get(message.author.display_avatar.url, allow_redirects=True)
            open('avatar.png', 'wb').write(b.content)
            color_thief = ColorThief('avatar.png')
            avatar_color = color_thief.get_color(quality=1)
            os.remove("avatar.png")
        except:
            pass

        if options:
            options_str = ""
            index = 0
            for option in options:
                options_str += f'{emojis[index]} {option}\n'
                index += 1
            options_str = options_str[:-1]
            embed = Embed(
                title=question,
                description=options_str
            )
            embed.set_footer(
                text=f'{message.author} started a poll',
                icon_url=message.author.display_avatar.url
            )
            embed.set_thumbnail(url=message.author.display_avatar.url)
            if avatar_color:
                embed.color = Colour.from_rgb(
                    avatar_color[0], avatar_color[1], avatar_color[2]
                )  
            poll = await message.channel.send(embed=embed)
            index = 0
            for _ in options:
                await poll.add_reaction(emojis[index])
                index += 1
        else:
            embed = Embed(title=question)
            embed.set_footer(
                text=f'{message.author} started a poll',
                icon_url=message.author.display_avatar.url
            )
            embed.set_thumbnail(url=message.author.display_avatar.url)
            if avatar_color:
                embed.color = Colour.from_rgb(
                    avatar_color[0], avatar_color[1], avatar_color[2]
                )            
            poll = await message.channel.send(embed=embed)
            for emoji in yes_no:
                await poll.add_reaction(emoji)

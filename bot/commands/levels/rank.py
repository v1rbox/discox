import asyncio

import discord
from PIL import Image, ImageDraw, ImageFont

from bot.base import Command
from bot.config import Config, Embed


def genarateBar(xp, level):
    req = level * 25 + 100
    proc = xp / req * 100

    proc *= 4
    im = Image.new("RGBA", (400, 30), (0, 0, 0, 0))

    draw = ImageDraw.Draw(im)

    font = ImageFont.truetype("bot/assets/font.ttf", 12)
    draw.text(
        (0, 3), f"{round(proc/4)}% To level {level+1}", (240, 240, 240), font=font
    )

    TINT_COLOR = (0, 0, 0)  # Black
    TRANSPARENCY = 0.10  # Degree of transparency, 0-100%
    OPACITY = int(255 * TRANSPARENCY)
    draw.rectangle(((0, 16), (600, 25)), fill=TINT_COLOR + (OPACITY,))

    draw.line((0, 20, proc, 20), fill=(56, 132, 44), width=5)
    im.save("bot/assets/tmp/image.png", quality=95)


class cmd(Command):
    """A discord command instance."""

    name = "rank"
    usage = "rank [*user]"
    description = "Check the rank for another user, by default this is the author."

    async def execute(self, arguments, message) -> None:
        if arguments[0] == "":
            user = message.author
        else:
            user = message.guild.get_member_named(arguments[0])
            if user == None:
                embed = Embed(
                    title="User not found",
                    description=f"The user named `{arguments[0]}` not found.\n*Note: This command is case sensitive. E.g use `Virbox#2050` instead of `virbox#2050`.*",
                )
                embed.set_color("red")
                await message.channel.send(embed=embed)
                return

        async with message.channel.typing():

            result = await self.db.raw_exec_select(
                f"SELECT exp, level FROM levels WHERE user_id = '{user.id}'"
            )

            if len(result) == 0:
                result = (0, 0)
            else:
                result = result[0]

            genarateBar(result[0], result[1])
            tempChannel = message.guild.get_channel(Config.temp_channel)
            with open("bot/assets/tmp/image.png", "rb") as f:
                picture = discord.File(f)
                msg = await tempChannel.send(file=picture)
                url = msg.attachments[0].url
                await asyncio.sleep(1)

            embed = Embed()
            embed.set_author(
                name=f"{user.display_name}'s ranking information",
                icon_url=user.avatar.url,
            )
            embed.add_field(name="**Level**", value=f"**```css\n{result[1]}```**")
            embed.add_field(name="**Exp**", value=f"**```css\n{result[0]}```**")
            embed.set_image(url=url)

            await message.channel.send(embed=embed)

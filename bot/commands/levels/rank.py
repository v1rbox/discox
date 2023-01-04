from bot.config import Config, Embed
from bot.base import Command
import discord
import asyncio

from PIL import Image, ImageDraw, ImageFont


def genarateBar(xp, level):
    req = level * 25 + 100
    proc = xp / req * 100

    proc *= 4
    im = Image.new('RGBA', (400, 30), (0, 0, 0, 0))

    draw = ImageDraw.Draw(im)

    font = ImageFont.truetype("bot/assets/font.ttf", 12)
    draw.text((0, 3), f"{round(proc/4)}% To level {level+1}", (240, 240, 240), font=font)

    TINT_COLOR = (0, 0, 0)  # Black
    TRANSPARENCY = .10  # Degree of transparency, 0-100%
    OPACITY = int(255 * TRANSPARENCY)
    draw.rectangle(((0, 16), (600, 25)), fill=TINT_COLOR+(OPACITY,))


    draw.line((0, 20, proc, 20), fill=(255, 0, 61), width=5)
    im.save('bot/assets/tmp/image.png', quality=95)


class cmd(Command):
    """ A discord command instance. """

    name = "rank"
    usage = "rank [*user]"
    description = "Check the rank for another user, by default this is the author."

    async def execute(self, arguments, message) -> None:
        if arguments[0] == "":
            user = message.author
        else:
            user = await message.guild.get_member_named(arguments[0])

        async with message.channel.typing():

            cursor = await self.db.cursor()
            await cursor.execute(f"SELECT exp, level FROM levels WHERE user_id = '{user.id}'")
            result = await cursor.fetchone()

            if result is None:
                result = (0, 0)

            genarateBar(result[0], result[1])
            tempChannel = message.guild.get_channel(Config.temp_channel)
            with open('bot/assets/tmp/image.png', 'rb') as f:
                picture = discord.File(f)
                msg = await tempChannel.send(file=picture)
                url = msg.attachments[0].url
                await asyncio.sleep(1)

            embed = Embed()
            embed.set_author(name = f"{user.display_name}'s ranking information", icon_url = user.avatar.url)
            embed.add_field(name = "**Level**", value = f"**```css\n{result[1]}```**")
            embed.add_field(name = "**Exp**", value = f"**```css\n{result[0]}```**")
            embed.set_image(url=url)

            await message.channel.send(embed=embed)

            await cursor.close()


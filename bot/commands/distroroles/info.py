import io
import os
from re import search, sub

import aiohttp
import orjson
from colorthief import ColorThief
from discord import Colour

from bot.base import Command
from bot.config import Embed


class cmd(Command):
    """A discord command instance."""

    name = "info"
    usage = "info <distribution>"
    description = "Shows information about the given distro"

    async def execute(self, arguments, message) -> None:
        error_embed = Embed(
            title="Distro",
            description=f"**Not found**\n\nThe distro named `{arguments[0]}` not found.",
        )
        error_embed.set_color("red")

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://diwa.demo-web-fahmi.my.id/api/v2/distributions/{arguments[0]}"
            ) as result:
                if result.status != 200:
                    await message.channel.send(embed=error_embed)
                    return
                j = await result.json(loads=orjson.loads)
        if j["message"] != "success":
            await message.channel.send(embed=error_embed)
            return
        dominant_color = None
        distro_codename = None
        try:
            for entry in j["recent_related_news_and_releases"]:
                link = entry["url"]
                if "https://distrowatch.com/index.php?distribution=" in link:
                    distro_codename = link.replace(
                        "https://distrowatch.com/index.php?distribution=", ""
                    )
            if not distro_codename:
                for link in j["screenshots"]:
                    if "http://distrowatch.com/gallery.php?distribution=" in link:
                        distro_codename = link.replace(
                            "http://distrowatch.com/gallery.php?distribution=", ""
                        )
            if not distro_codename:
                for link in j["reviews"]:
                    if search(
                        "https\:\/\/distrowatch\.com\/weekly\.php\?issue\=.*\#", link
                    ):
                        distro_codename = sub(
                            "https\:\/\/distrowatch\.com\/weekly\.php\?issue\=.*\#",
                            "",
                            link,
                        )

            if distro_codename:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"https://distrowatch.com/images/yvzhuwbpy/{distro_codename}.png",
                        headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
                        },
                    ) as b:
                        b = io.BytesIO(await b.read())
                color_thief = ColorThief(b)
                dominant_color = color_thief.get_color(quality=1)
        except:
            pass

        embed = Embed(
            title=j["distribution"],
            description=j["about"],
            url=j["homepage"],
        )
        if distro_codename:
            embed.set_thumbnail(
                url=f"https://distrowatch.com/images/yvzhuwbpy/{distro_codename}.png"
            )
            embed.set_image(
                url=f"https://distrowatch.com/images/ktyxqzobhgijab/{distro_codename}.png"
            )
        embed.add_field(name="Average rating", value=j["average_rating"], inline=True)
        embed.add_field(
            name="Architectures", value=", ".join(j["architectures"]), inline=True
        )
        embed.add_field(name="OS type", value=j["os_type"], inline=True)
        embed.add_field(name="Development status", value=j["status"], inline=True)
        embed.add_field(
            name="Graphical environments",
            value=", ".join(j["desktop_environments"]),
            inline=False,
        )
        embed.add_field(
            name="Downloads", value="\n".join(j["download_mirrors"]), inline=False
        )
        if dominant_color:
            embed.color = Colour.from_rgb(
                dominant_color[0], dominant_color[1], dominant_color[2]
            )

        await message.channel.send(embed=embed)

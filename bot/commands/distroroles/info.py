import io
import os
from re import search, sub

import aiohttp
from colorthief import ColorThief
from discord import Colour

from bot.base import Command
from bot.config import Embed


class cmd(Command):
    """A discord command instance."""

    name = "info"
    usage = "info <distribution>"
    description = "Shows information about the user entered distro"

    async def execute(self, arguments, message) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://diwa.demo-web-fahmi.my.id/api/v2/distributions/{arguments[0]}"
            ) as result:
                result = await result.json()
        if result.status_code != 200 or result["message"] != "success":
            embed = Embed(
                title="Distro",
                description=f"**Not found**\n\nThe distro named `{arguments[0]}` not found.",
            )
            embed.set_color("red")
            await message.channel.send(embed=embed)
            return

        dominant_color = None
        distro_codename = None
        try:
            for entry in result["recent_related_news_and_releases"]:
                link = entry["url"]
                if "https://distrowatch.com/index.php?distribution=" in link:
                    distro_codename = link.replace(
                        "https://distrowatch.com/index.php?distribution=", ""
                    )
            if not distro_codename:
                for link in result["screenshots"]:
                    if "http://distrowatch.com/gallery.php?distribution=" in link:
                        distro_codename = link.replace(
                            "http://distrowatch.com/gallery.php?distribution=", ""
                        )
            if not distro_codename:
                for link in result["reviews"]:
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
                        f"https://distrowatch.com/images/yvzhuwbpy/{distro_codename}.png"
                    ) as b:
                        b = io.BytesIO(await b.read())
                color_thief = ColorThief(b)
                dominant_color = color_thief.get_color(quality=1)
        except:
            pass

        embed = Embed(
            title=result["distribution"],
            description=result["about"],
            url=result["homepage"],
        )
        if distro_codename:
            embed.set_thumbnail(
                url=f"https://distrowatch.com/images/yvzhuwbpy/{distro_codename}.png"
            )
        embed.add_field(
            name="Average rating", value=result["average_rating"], inline=True
        )
        embed.add_field(
            name="Architectures", value=", ".join(result["architectures"]), inline=True
        )
        embed.add_field(name="OS type", value=result["os_type"], inline=True)
        embed.add_field(name="Development status", value=result["status"], inline=True)
        embed.add_field(
            name="Graphical environments",
            value=", ".join(result["desktop_environments"]),
            inline=False,
        )
        embed.add_field(
            name="Downloads", value="\n".join(result["download_mirrors"]), inline=False
        )
        if dominant_color:
            embed.color = Colour.from_rgb(
                dominant_color[0], dominant_color[1], dominant_color[2]
            )

        await message.channel.send(embed=embed)

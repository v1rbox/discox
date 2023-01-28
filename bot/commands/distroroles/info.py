from bot.base import Command
from bot.config import Embed
import requests
from colorthief import ColorThief
from discord import Colour


class cmd(Command):
    """A discord command instance."""
    
    name = "info"
    usage = "info <distribution>"
    description = "Shows information about the user entered distro"
    
    async def execute(self, arguments, message) -> None:

        result = requests.get(f'https://diwa.demo-web-fahmi.my.id/api/v2/distributions/{arguments[0]}')
        if result.status_code != 200 or result.json()["message"] != "success":
            embed = Embed(
                title="Distro",
                description=f'**Not found**\n\nThe distro named `{arguments[0]}` not found.'
            )
            embed.set_color("red")
            await message.channel.send(embed=embed)
            return
        result = result.json()

        dominant_color = None
        distro_codename = None
        try:
            for entry in result["recent_related_news_and_releases"]:
                link = entry["url"]
                if "https://distrowatch.com/index.php?distribution=" in link:
                    distro_codename = link.replace("https://distrowatch.com/index.php?distribution=", "")

            if distro_codename:
                b = requests.get(f'https://distrowatch.com/images/yvzhuwbpy/{distro_codename}.png', allow_redirects=True)
                open('distro.png', 'wb').write(b.content)
                color_thief = ColorThief('distro.png')
                dominant_color = color_thief.get_color(quality=1)
        except:
            pass

        embed = Embed(
            title=result["distribution"],
            description=result["about"],
            url=result["homepage"]
        )
        if distro_codename:
            embed.set_thumbnail(url=f'https://distrowatch.com/images/yvzhuwbpy/{distro_codename}.png')
        embed.add_field(name="Average rating", value=result["average_rating"], inline=True)
        embed.add_field(name="Architectures", value=", ".join(result["architectures"]), inline=True)
        embed.add_field(name="OS type", value=result["os_type"], inline=True)
        embed.add_field(name="Development status", value=result["status"], inline=True)
        embed.add_field(name="Graphical environments", value=", ".join(result["desktop_environments"]), inline=False)
        embed.add_field(name="Downloads", value="\n".join(result["download_mirrors"]), inline=False)
        if dominant_color:
            embed.color = Colour.from_rgb(dominant_color[0], dominant_color[1], dominant_color[2])

        await message.channel.send(embed=embed)

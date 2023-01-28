from bot.base import Command
from bot.config import Embed
import requests


class cmd(Command):
    """A discord command instance."""
    
    name = "info"
    usage = "info <distribution>"
    description = "Shows information about the user entered distro"
   
    async def execute(self, arguments, message) -> None:
        result = requests.get(f'https://diwa.demo-web-fahmi.my.id/api/v2/distributions/{arguments[0]}').json()
        if result["message"] != "success":
            embed = Embed(
                title="Distro",
                description=f'**Invalid distro**\n\nThe distro named `{args[0]}` not found.\n*Note: Please don\'t type the distro name seperately.\n*Example: `endeavouros`'
            )
            embed.set_color("red")
            await message.channel.send(embed=embed)
            return
    
        embed = Embed(
            title=result["distribution"],
            description=result["about"],
            thumbnail=f'https://distrowatch.com/images/yvzhuwbpy/{arguments[0]}.png',
            url=result["homepage"],
        )
        embed.add_field("Average rating", result["average_rating"], inline=True)
        embed.add_field("Architectures", ", ".join(result["architectures"]), inline=True)
        embed.add_field("OS type", result["os_type"], inline=True)
        embed.add_field("Development status", result["status"], inline=True)
        embed.add_field("Graphical environments", ", ".join(result["desktop_environments"]), inline=False)
        embed.add_field("Downloads", "\n".join(result["download_mirrors"]), inline=False)
        embed.set_color("green")
        await message.channel.send(embed=embed)

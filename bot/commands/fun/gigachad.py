import json
import random

import aiohttp

from bot.base import Command
from bot.config import Embed


class cmd(Command):
    """A discord command instance."""

    name = "gigachad"
    usage = "gigachad"
    description = "Sends a random gigachad"

    async def execute(self, arguments, message) -> None:
        # Special thanks to the awesome work of justinlime for the collection of gigachads
        # Repo: https://github.com/justinlime/GigaChads

        # Start parsing every available images in the GigaChads repo
        gigaurl = (
            "https://raw.githubusercontent.com/justinlime/GigaChads/main/gigalist.json"
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(gigaurl) as result:
                if result.status != 200:
                    embed = Embed(title="GigaSad :(", description="Could Not Load")
                    embed.set_color("red")
                    await message.channel.send(embed=embed)
                    return
                gigalist = await result.json(content_type=None)
                gigalist = gigalist["gigachads"]

        # randomly
        gigachad = random.choice(gigalist)

        # send the image
        embed = Embed(title="Best GigaChad ever:")
        embed.set_image(
            url=f"https://raw.githubusercontent.com/justinlime/GigaChads/main/gigachads/{gigachad}"
        )
        await message.channel.send(embed=embed)

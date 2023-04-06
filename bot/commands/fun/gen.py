import base64
import time
from io import BytesIO

from craiyon import Craiyon

from bot.base import Command
from bot.commands.utility.__blocked_prompts import blocked
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    #
    name = "gen"
    usage = "gen <*prompt>"
    description = "Uses the Craiyon AI API to generate an image with a given prompt"

    async def execute(self, arguments, message) -> None:
        prompt = arguments[0]
        for word in prompt.split():
            if word.lower() in blocked:
                await message.channel.send(
                    "I'm not generating that you meanie >:( It's NSFW! Try something else!"
                )
                return

        loadingE = Embed(
            title=f"Image '{prompt}' currently generating, please wait a moment!"
        )
        loadingM = await message.channel.send(embed=loadingE)

        generator = Craiyon()
        result = generator.generate(prompt)
        images = result.images
        embed = Embed(title="Here is the generated image")
        embed.set_image(url=images[0])

        await loadingM.delete()
        await message.channel.send(embed=embed)

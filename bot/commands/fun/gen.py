from craiyon import Craiyon
from bot.config import Config, Embed
from bot.base import Command
from io import BytesIO
import base64
import time
from discox.bot.events.blocked_prompts import blocked

class cmd(Command):
    """ A discord command instance. """

    name = "gen"
    usage = "gen <*prompt>"
    description = "Uses the Craiyon AI API to generate an image with a given prompt"

    async def execute(self, arguments, message, prompt) -> None:
        if prompt.lower() in blocked:
            await message.channel.send("I'm not generating that you meanie >:( It's NSFW! Try something else!")
            return
            
        generator = Craiyon()
        result = generator.generate(prompt)
        images = result.images
        embed = Embed(title="Here is the generated image")
        embed.set_image(images)
        

        await message.channel.send(embed=embed)
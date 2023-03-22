import random

from bot.base import Command
from bot.config import Embed


class cmd(Command):
    """A discord command instance."""

    name = "gigachad"
    usage = "gigachad"
    description = "Gigachad random image"

    async def execute(self, arguments, message) -> None:
        # Special thanks to the awesome work of justinlime for the collection of gigachads
        # Repo: https://github.com/justinlime/GigaChads

        # Start parsing every available images in the GigaChads repo
        list_of_images = [
            "gigabigbrain.jpg",
            "gigacrab.png",
            "gigadesktop.jpg",
            "gigalaptop.jpg",
            "gigalegs.jpg",
            "gigamirror.jpg",
            "gigamutant.jpg",
            "gigaphone.jpg",
            "gigatriple.jpg",
            "gigatriplesupreme.jpg",
            "gigawide.jpg",
        ]
        # randomly
        image = random.choice(list_of_images)

        # send the image
        embed = Embed(title="Best GigaChad ever:")
        embed.set_image(
            url=f"https://raw.githubusercontent.com/justinlime/GigaChads/main/{image}"
        )
        await message.channel.send(embed=embed)

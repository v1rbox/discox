import io

import aiohttp
import discord
import PIL
import yarl
from discord import Message
from PIL import Image

from bot.base import Command

from .__uis import Confirm


class cmd(Command):

    """
    Set your own background for your rank card.
    """

    name = "setbg"
    usage = "setbg <url>"
    description = "Set your own background for your rank card. URL must be a direct link to an image."

    def is_valid_url(self, url: str) -> bool:
        try:
            assert yarl.URL(url).scheme in ("http", "https"), "Malformed URL."
            assert yarl.URL(url).host is not None, "Malformed URL."
            assert yarl.URL(url).host != "", "Malformed URL."
        except (ValueError) as e:
            raise ValueError("Invalid URL. Unable to parse URL") from e
        except (AssertionError) as e:
            raise ValueError("Invalid URL. URL is malformed.") from e

    async def is_valid_picture(self, url: str) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise ValueError(
                        f"Invalid URL. URL must be a direct link to an image. Status Code: {response.status}"
                    )
                try:
                    image = Image.open(io.BytesIO(await response.read()))
                except PIL.UnidentifiedImageError:
                    raise ValueError(
                        "Invalid URL. URL must be a direct link to an image. Got an invalid image data."
                    ) from None
                image.verify()
                image.close()
                return True

    async def execute(self, arguments, message) -> None:
        if arguments[0] == "":
            await message.channel.send("Please provide a url.")
            return
        view = Confirm(message.author)
        self.is_valid_url(arguments[0])
        await self.is_valid_picture(arguments[0])
        a: Message = await message.channel.send(
            "Are you sure you want to set this background?", view=view
        )
        await view.wait()
        answer = view.value
        if answer:
            await self.db.raw_exec_commit(
                "UPDATE levels SET bg = ? WHERE user_id = ?",
                (arguments[0], message.author.id),
            )
            await a.edit(content="Successfully set background.")
        else:
            await a.edit("Cancelled.")

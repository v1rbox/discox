import discord

from bot.base import Command

from .__uis import Confirm


class cmd(Command):

    """
    Set your own background for your rank card.
    """

    name = "setbg"
    usage = "setbg <url>"
    description = "Set your own background for your rank card. URL must be a direct link to an image."

    async def execute(self, arguments, message) -> None:
        if arguments[0] == "":
            await message.channel.send("Please provide a url.")
            return
        view = Confirm(message.author)
        await message.channel.send(
            "Are you sure you want to set this background?", view=view
        )
        await view.wait()
        answer = view.value
        if answer:
            await self.db.raw_exec_commit(
                "UPDATE levels SET bg = ? WHERE user_id = ?",
                (arguments[0], message.author.id),
            )
            await message.channel.send("Successfully set background.")
        else:
            await message.channel.send("Cancelled.")

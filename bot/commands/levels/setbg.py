import discord

from bot.base import Command

from .utils.__uis import OptionView


class cmd(Command):
    
    """
    Set your own background for your rank card.
    """
    
    name = "setbg"
    usage = "setbg [*url]"
    description = "Set your own background for your rank card. URL must be a direct link to an image."

    async def execute(self, arguments, message) -> None:
        if arguments[0] == "":
            await message.channel.send("Please provide a url.")
            return
        view = OptionView()
        await message.channel.send(
            "Are you sure you want to set this background?", view=view
        )
        answer = await view.get_answer()
        if answer:
            cursor = await self.db.cursor()
            await cursor.execute(
                f"UPDATE levels SET bg = '{arguments[0]}' WHERE user_id = '{message.author.id}'"
            )
            await message.channel.send("Successfully set background.")
        else:
            await message.channel.send("Cancelled.")

from bot.base import Command
from .__box_generator import generate_color_square
from .__uis import OptionView
class cmd(Command):
    name = "setfontcolor"
    usage = "setfontcolor <r> <g> <b>"
    description = "Set the font color for your rank card. RGB values must be between 0 and 255. If RGB has not been set, the default is white. If RGB malformed, It errors out."
    
    async def execute(self, arguments, message) -> None:
        rgb = tuple(int(i) for i in arguments if i.isdigit() and 0 <= int(i) <= 255 and len(arguments) == 3)
        if not len(rgb) == 3:
            raise ValueError("RGB malformed.")
        option = OptionView()
        await message.channel.send("Are you sure you want to set your font color to this?", view=option, file=generate_color_square(rgb))
        answer = await option.wait()
        if answer:
            await self.db.raw_exec_commit("UPDATE levels SET font_color = ? WHERE user_id = ?", (rgb, message.author.id))
            await message.channel.send("Font color set.")
        else:
            await message.channel.send("Reverted.")
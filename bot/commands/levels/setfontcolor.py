from bot.base import Command

from .__box_generator import generate_color_square
from .__uis import Confirm


class cmd(Command):
    name = "setfontcolor"
    usage = "setfontcolor <*rgb>"
    description = "Set the font color for your rank card. RGB values must be between 0 and 255. If the RGB value is malformed, throws an error."

    async def execute(self, arguments, message) -> None:
        arguments = arguments[0].split(" ")
        assert len(arguments) == 3, "RGB malformed. Expecting 3 values."
        rgb = tuple(int(i) for i in arguments if i.isdigit() and 0 <= int(i) <= 255)
        if not len(rgb) == 3:
            raise ValueError(
                "RGB malformed. Expecting 3 of them to be digits between 0 and 255."
            )
        option = Confirm(message.author)
        a = await message.channel.send(
            "Are you sure you want to set your font color to this?",
            view=option,
            file=generate_color_square(rgb),
        )
        await option.wait()
        answer = option.value
        if answer:
            await self.db.raw_exec_commit(
                "UPDATE levels SET font_color = ? WHERE user_id = ?",
                (" ".join([str(i) for i in rgb]), message.author.id),
            )
            await a.edit(content="Font color set.")
        else:
            await a.edit(content="Reverted.")

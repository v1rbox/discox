from bot.base import Command
from bot.config import Embed
import random


class cmd(Command):
    """A discord command instance."""

    name = "pp"
    usage = "pp [word]"
    description = "If an arg is provided, calculate pp size of arg, otherwise calculate pp size of user"

    async def execute(self, arguments, message) -> None:
        pp = message.author.name if not len(arguments) else arguments[0]
        random.seed(pp)
        pp_int=random.randint(0, 51)
        pp_size = "8" + "".join("=" for p in range(pp_int)) + "D"
        pp_rating = "smol" if pp_int < 18 else "avg" if pp_int < 36 else "chungo"
        embed = Embed(title=f"{pp}'s pp size \n\n**{pp_size}**\n\n*{pp_rating} pp*\n")
        await message.reply(embed=embed)

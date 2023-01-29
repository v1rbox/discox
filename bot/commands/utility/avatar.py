from re import findall

from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "avatar"
    usage = "avatar [mention]"
    description = "Returns the avatar of the user. If a mention or id is given, returns the avatar of that user"

    async def execute(self, arguments, message) -> None:
        if len(arguments):
            userId = int("".join(findall("\d", arguments[0])))
            user = await message.guild.fetch_member(userId)
        else:
            user = message.author

        url = user.display_avatar.url
        embed = Embed(
            title=f"Avatar of {str(user)}"
        )
        embed.set_image(url=url)
        await message.reply(embed=embed)

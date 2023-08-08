from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "avatar"
    usage = "avatar [mention:member]"
    description = "Shows the avatar of a user. If a mention or id is given, returns the avatar of that user. Otherwise, returns your avatar."

    async def execute(self, arguments, message) -> None:
        user = message.author if not len(arguments) else arguments[0]
        url = user.display_avatar.url
        embed = Embed(title=f"{user.name}'s avatar")
        embed.set_image(url=url)
        await message.reply(embed=embed)

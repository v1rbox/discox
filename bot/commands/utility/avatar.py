import re
from discord import NotFound

from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "avatar"
    usage = "avatar [mention]"
    description = "Returns the avatar of the user. If a mention or id is given, returns the avatar of that user"

    async def execute(self, arguments, message) -> None:
        if len(arguments):
            userId = int("0" + re.sub("\D", "", arguments[0]))
            if not re.search("^(<@\d+>|\d+)$", arguments[0]) or userId > 9223372036854775807:
                embed = Embed(
                    title="Error",
                    description=f"'{arguments[0]}' is not a valid user id"
                )
                embed.set_color("red")
                return await message.reply(embed=embed)
            try:
                user = await message.guild.fetch_member(userId)
            except NotFound:
                embed = Embed(
                    title="Error",
                    description=f"The user '{userId}' doesn't exist or is not in this server"
                )
                embed.set_color("red")
                return await message.reply(embed=embed)
        else:
            user = message.author

        url = user.display_avatar.url
        embed = Embed(title=f"Avatar of {str(user)}")
        embed.set_image(url=url)
        await message.reply(embed=embed)

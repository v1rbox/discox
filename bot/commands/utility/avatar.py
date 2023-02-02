from bot.base import Command
from bot.config import Embed
import discord

class cmd(Command):
    """A discord command instance."""

    name = "avatar"
    usage = "avatar [mention]"
    description = "Returns the avatar of the user. If a mention or id is given, returns the avatar of that user"

    async def execute(self, arguments, message) -> None:
        user = None
        if arguments[0] == "":
            user = message.author
        else:
            try:
                user = message.guild.get_member_named(arguments[0])
                assert user is not None
            except AssertionError:
                try:
                    user = await self.bot.fetch_user(arguments[0])
                except (discord.NotFound, discord.HTTPException):
                    embed = Embed(
                        title="User not found",
                        description=f"The user named `{arguments[0]}` not found.\n*Note: This command is case sensitive. E.g use `Virbox#2050` instead of `virbox#2050`.*",
                    )
                    embed.set_color("red")
                    await message.channel.send(embed=embed)
                    return
        embed = Embed(title=f"{user.name}'s avatar")
        embed.set_image(url=user.avatar.url if user.avatar else user.default_avatar.url)
        await message.channel.send(embed=embed)
        

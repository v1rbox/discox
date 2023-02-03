from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "avatar"
    usage = "avatar [mention:member]"
    description = "Returns the avatar of the user. If a mention or id is given, returns the avatar of that user"

    async def execute(self, arguments, message) -> None:
        user = message.author if not len(arguments) else arguments[0]
        url = user.display_avatar.url
        embed = Embed(title=f"Avatar of {str(user)}")
        embed.set_image(url=url)
        await message.reply(embed=embed)
                    except (discord.NotFound, discord.HTTPException, discord.Forbidden):
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

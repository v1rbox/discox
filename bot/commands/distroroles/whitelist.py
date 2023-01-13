from bot.base import Command
from bot.commands.distroroles.add import cmd as Distro
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "whitelist"
    usage = "whitelist"
    description = f"Shows available distro role options"

    async def execute(self, arguments, message) -> None:
        if len(Distro.whitelist) > 0:
            description = "**Available distro roles:**\n\n"
            for i in Distro.whitelist:
                description += f"`{i}`\n"
            embed = Embed(title="Distro", description=description)
            await message.channel.send(embed=embed)
        else:
            embed = Embed(
                title="Distro", description="**No distros currently whitelisted**"
            )
            embed.set_color("red")
            await message.channel.send(embed=embed)

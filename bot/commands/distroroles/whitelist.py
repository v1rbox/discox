from bot.config import Config, Embed
from bot.base import Command
from bot.commands.distroroles.add import cmd as Distro

class cmd(Command):
    """ A discord command instance. """
  
    name = "whitelist"
    usage = "distro whitelist"
    description = f"Shows available distro role options"

    async def execute(self, arguments, message) -> None:
      if len(Distro.whitelist) > 0:
        description = "**Available distro roles:**\n\n"
        for i in Distro.whitelist:
            description += f'`{i}`\n'
        embed = Embed(title="Distro", description=description)
        await message.channel.send(embed=embed)
      else:
        embed = Embed(title="Distro", description="**No distros currently whitelisted**")
        await message.channel.send(embed=embed)
from bot.config import Config, Embed
from bot.base import Command
from bot.commands.coderoles.add import cmd as Code

class cmd(Command):
    """ A discord command instance. """
  
    name = "whitelist"
    usage = "whitelist"
    description = f"Shows available languages"

    async def execute(self, arguments, message) -> None:
      if len(Code.whitelist) > 0:
        description = "**Available languages:**\n\n"
        for i in Code.whitelist:
            description += f'`{i}`\n'
        embed = Embed(title="Code", description=description)
        await message.channel.send(embed=embed)
      else:
        embed = Embed(title="Code", description="**No languages currently whitelisted**")
        embed.set_color("red")
        await message.channel.send(embed=embed)
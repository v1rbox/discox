from bot.config import Config, Embed
from bot.base import Command

class cmd(Command):
    """ A discord command instance. """

    name = "membercount"
    usage = "membercount"
    description = "Get the current membercount in the server."

    async def execute(self, arguments, message) -> None:
        embed = Embed(title="Member Count", description=f"Currently the server has `{message.guild.member_count}` members")
        await message.channel.send(embed=embed)

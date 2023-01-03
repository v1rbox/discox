from bot.config import Config, Embed
from bot.base import Command
import discord

class cmd(Command):
    """ A discord command instance. """

    name = "status"
    usage = "status <type>"
    description = "Changes the bot's status."

    async def execute(self, arguments, message) -> None:
        type = arguments[0].lower()
        match type:
            case "online":
                status = discord.Status.online
            case "idle":
                status = discord.Status.idle
            case "do_not_disturb":
                status = discord.Status.do_not_disturb
            case "invisible":
                status = discord.Status.invisible
            case _:
                embed = Embed(title="Invalid status", description=f"""'{type}' is an invalid status.
                Valid are: online, idle, do_not_disturb and invisible.""")
                message.reply(embed=embed)
                return
          
        await self.bot.change_presence(status=status, activity=self.bot.current_activity)
        self.bot.current_status = status
        embed = Embed(title="Status changed", description=f"Succesfully changed status to {type}")
        message.reply(embed=embed)

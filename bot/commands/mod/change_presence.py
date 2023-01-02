from bot.config import Config, Embed
from bot.base import Command
import discord

class cmd(Command):
    """ A discord command instance. """

    name = "change_presence"
    usage = "change_presence <command> <type> [*activity]"
    description = "Changes the status of the bot. Valid commands are status and activity."

    async def status(self, type):
        if type == "online":
            status = discord.Status.online
        elif type == "idle":
            status = discord.Status.idle
        elif type == "do_not_disturb":
            status = discord.Status.do_not_disturb
        elif type == "invisible":
            status = discord.Status.invisible
        else:
            return Embed(title="Invalid status", description=f"""'{type}' is an invalid status.
            Valid are: online, idle, do_not_disturb and invisible.""")
          
        await self.bot.change_presence(status=status, activity=self.bot.current_activity)
        self.bot.current_status = status
        return Embed(title="Status changed", description=f"Succesfully changed status to {type}")

    async def activity(self, type, message):
        if type == "playing":
            activityType = discord.ActivityType.playing
        elif type == "watching":
            activityType = discord.ActivityType.watching
        elif type == "listening":
            activityType = discord.ActivityType.listening
        else:
            return Embed(title="Invalid Activity", description=f"""'{type}' is an invalid activity.
            Valid are: playing, watching and listening.""")
        activity = discord.Activity(type=activityType, name=message)
        self.bot.current_activity = activity
        await self.bot.change_presence(activity=activity, status=self.bot.current_status)
        return Embed(title="Activity changed", description=f"Succesfully changed activity to {type}")
  
    async def execute(self, arguments, message) -> None:
        command = arguments[0]
        if command == "status":
            embed = await self.status(arguments[1])
            await message.reply(embed=embed)
        elif command == "activity":
            embed = await self.activity(arguments[1], arguments[2])
            await message.reply(embed=embed)
        else:
            embed = Embed(title="Invalid command", description=f"""'{command}' is an invalid command.
            Valid are: status and activity.""")
            await message.reply(embed=embed)

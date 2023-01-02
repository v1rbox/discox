from bot.config import Config, Embed
from bot.base import Command

class cmd(Command):
    """ A discord command instance. """

    name = "activity"
    usage = "activity <type> <*message>"
    description = "Changes the bot's activity."

    async def execute(self, arguments, message) -> None:
        type = arguments[0]
        match type:
            case "playing":
                activityType = discord.ActivityType.playing
            case "watching":
                activityType = discord.ActivityType.watching
            case "listening":
                activityType = discord.ActivityType.listening
            case _:
                embed =  Embed(title="Invalid Activity", description=f"""'{type}' is an invalid activity.
                Valid are: playing, watching and listening.""")
                message.reply(embed=embed)
                return
        activity = discord.Activity(type=activityType, name=arguments[1])
        self.bot.current_activity = activity
        await self.bot.change_presence(activity=activity, status=self.bot.current_status)
        embed = Embed(title="Activity changed", description=f"Succesfully changed activity to {type}")
        message.reply(embed=embed)

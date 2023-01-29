import urllib.parse as parse

from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "list"
    usage = "list"
    description = """Lists all reminders of the user"""

    async def execute(self, arguments, message) -> None:
        reminders = await self.db.raw_exec_select(
            "SELECT Timestamp, Reminder FROM reminders WHERE User = ?",
            (message.author.id,),
        )
        embed = Embed(
            title=f"Reminders of {message.author.name}#{message.author.discriminator}"
        )
        for reminder in reminders:
            timestamp, remindMsg = reminder
            embed.add_field(
                name=f"{parse.unquote(remindMsg)}",
                value=f"<t:{timestamp}:f> - <t:{timestamp}:R>",
            )
        await message.reply(embed=embed)

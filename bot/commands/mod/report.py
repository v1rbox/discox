from bot.base import Command
from bot.config import Config, Embed

import time
import datetime
import asyncio

class cmd(Command):

    name = "report"
    usage = "report <user_id>"
    description = "Report a user"

    async def execute(self, arguments, message) -> None:
        await message.delete()
        member = await message.guild.fetch_member(arguments[0])
        await member.timeout(datetime.timedelta(hours=3), reason=f"Report - {message.author}")

        ts = int(time.time())

        embedr = Embed(title="Editing report")
        embedr.add_field(name="User", value=f"<@{arguments[0]}>")
        embedr.add_field(name="Timestamp", value=f"<t:{ts}:R>")
        embedr.add_field(name="Reason", value=f"```No reason given```", inline=False)
        embedr.set_color("red")

        report = await message.author.send(embed=embedr)
        msg = await message.author.send("Please enter the reason for the report, you can also provide context using message links.")
        
        def check(m):
            return m.author.id == message.author.id and m.channel == msg.channel

        try:
            msg = await self.bot.wait_for('message', timeout=600.0, check=check)
        except asyncio.TimeoutError:
            await msg.channel.send("Timed out.")
            return

        reason: str = msg.content
        embedr.set_field_at(2, name="Reason", value=f"```{reason}```", inline=False)

        await report.edit(embed=embedr)

        embed = Embed(description="Do you want to save the report?")
        msg = await msg.channel.send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

        def check(reaction, user):
            return user == message.author and str(reaction.emoji) in ["❌", "✅"]

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=600.0, check=check)
        except asyncio.TimeoutError:
            await channel.send("Timed out.")
            return

        if str(reaction.emoji) == "✅":
            channel = await self.bot.fetch_channel(Config.report_channel_id)
            await channel.create_thread(
                name=f"{arguments[0]} - Report", 
                embed=embedr, 
                applied_tags=[channel.available_tags[0]]
            )
            await msg.send("Report has been posted")
        else:
            await msg.send("Report Canseled")
            # Remove timeout
            await member.timeout(datetime.timedelta(seconds=3), reason=f"Report Canseled - {message.author}")


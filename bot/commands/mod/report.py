import asyncio
import datetime
import time

from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):
    name = "report"
    usage = "report <user_id:member>"
    description = "Report a user"

    async def execute(self, arguments, message) -> None:
        await message.delete()
        member = arguments[0]
        await member.timeout(
            datetime.timedelta(hours=3), reason=f"Report - {message.author}"
        )
        
        embedf = Embed(title="Pending Report", description="A report has been opened on your account and is awaiting review by an administrator.\n\nYou can send messages in this DM channel once the reason has been supplied and they will be relaied to the administrator reviewing your report.\n\nYou have also been applied a 3 hour timeout, this is simply while we complete our review, this may be lifted after the process is complete. Thank you for your patience!")
        embedf.add_field(name="Reason", value="```Pending...```")

        embedf_msg = await member.send(embed=embedf)

        ts = int(time.time())

        embedr = Embed(title="Editing report")
        embedr.add_field(name="User", value=f"<@{member.id}>")
        embedr.add_field(name="Moderator", value=f"<@{message.author.id}>")
        embedr.add_field(name="Timestamp", value=f"<t:{ts}:R>")
        embedr.add_field(name="Reason", value=f"```No reason given```", inline=False)
        embedr.set_color("red")

        report = await message.author.send(embed=embedr)
        msg = await message.author.send(
            "Please enter the reason for the report, you can also provide context using message links."
        )

        def check(m):
            return m.author.id == message.author.id and m.channel == msg.channel

        try:
            msg = await self.bot.wait_for("message", timeout=600.0, check=check)
        except asyncio.TimeoutError:
            await msg.channel.send("Timed out.")
            await member.timeout(
                datetime.timedelta(seconds=3),
                reason=f"Report Canceled - {message.author}",
            )
            await member.send("Your report has been canseled. Sorry for the incontinence. Your timeout will be lifted in 3 seconds.")
            return

        reason: str = msg.content
        embedr.set_field_at(3, name="Reason", value=f"```{reason}```", inline=False)
        embedf.set_field_at(0, name="Reason", value=f"```{reason}```", inline=False)

        await report.edit(embed=embedr)
        await embedf_msg.edit(embed=embedf)

        embed = Embed(description="Do you want to save the report?")
        msg = await msg.channel.send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

        def check(reaction, user):
            return user == message.author and str(reaction.emoji) in ["❌", "✅"]

        try:
            reaction, user = await self.bot.wait_for(
                "reaction_add", timeout=600.0, check=check
            )
        except asyncio.TimeoutError:
            await channel.send("Timed out.")
            await member.timeout(
                datetime.timedelta(seconds=3),
                reason=f"Report Canceled - {message.author}",
            )
            await member.send("Your report has been canseled. Sorry for the incontinence. Your timeout will be lifted in 3 seconds.")
            return

        if str(reaction.emoji) == "✅":
            channel = await self.bot.fetch_channel(Config.report_channel_id)
            await channel.create_thread(
                name=f"{member.id} - {member} - Report",
                content="<@1053714720026267831>",
                embed=embedr,
                applied_tags=[channel.available_tags[0]],
            )
            await msg.channel.send("Report has been posted")
        else:
            await msg.channel.send("Report Canceled")
            # Remove timeout
            await member.timeout(
                datetime.timedelta(seconds=3),
                reason=f"Report Canceled - {message.author}",
            )

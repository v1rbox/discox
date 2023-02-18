from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "membercount"
    usage = "membercount"
    description = "Get the current membercount in the server."

    async def execute(self, arguments, message) -> None:
        memberCount = message.guild.member_count
        result = await self.db.raw_exec_select(f"SELECT membercount FROM membercount")
        if len(result) == 0:
            await self.db.raw_exec_commit(
                f"INSERT INTO membercount(membercount) VALUES(?)",
                (memberCount,),
            )
        result = await self.db.raw_exec_select(f"SELECT membercount FROM membercount")
        status = "increased"
        extra = ""
        isgood = ":fire:"
        if result[0][0] > memberCount:
            status = "decreased"
            isgood = ""
        if result[0][0] != memberCount:
            extra = f"\nThe member count has {status} by {abs(memberCount - result[0][0])} since last execution {isgood}"
        embed = Embed(
            title="Member Count",
            description=f"Currently the server has `{memberCount}` members.{extra}",
        )
        await message.channel.send(embed=embed)
        await self.db.raw_exec_commit(
            f"UPDATE membercount SET membercount = ?", (memberCount,)
        )
        if memberCount >= 1000 and memberCount < 1050:
            embed = Embed(
                title=":tada: We did it! :tada:",
                description="We have hit 1000 members. Thank you to everyone who joined!",
            )
            await message.channel.send(embed=embed)

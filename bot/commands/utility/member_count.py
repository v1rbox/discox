import math

from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "membercount"
    usage = "membercount"
    description = "Get the current membercount in the server."

    async def execute(self, arguments, message) -> None:
        member_count = message.guild.member_count
        result = await self.db.raw_exec_select(f"SELECT membercount FROM membercount")
        if len(result) == 0:
            await self.db.raw_exec_commit(
                f"INSERT INTO membercount(membercount) VALUES(?)",
                (member_count,),
            )
        result = await self.db.raw_exec_select(f"SELECT membercount FROM membercount")
        status = "increased"
        extra = ""
        isgood = ":fire:"
        if result[0][0] > member_count:
            status = "decreased"
            isgood = ""
        if result[0][0] != member_count:
            extra = f"\nThe member count has {status} by `{abs(member_count - result[0][0])}` since last execution {isgood}"
        embed = Embed(
            title="Member Count",
            description=f"Currently the server has `{member_count}` members.{extra}\n`{(int(math.ceil(member_count / 1000)) * 1000)-member_count}` members left to {int(math.ceil(member_count / 1000)) * 1000}",
        )
        await message.channel.send(embed=embed)
        await self.db.raw_exec_commit(
            f"UPDATE membercount SET membercount = ?", (member_count,)
        )
        if (
            member_count - (int(math.floor(member_count / 1000)) * 1000) < 50
            and (int(math.floor(member_count / 1000)) * 1000) != 0
        ):
            embed = Embed(
                title=":tada: We did it! :tada:",
                description=f"We have hit {int(math.floor(member_count / 1000)) * 1000} members. Thank you to everyone who joined!",
            )
            await message.channel.send(embed=embed)

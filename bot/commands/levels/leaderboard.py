from bot.config import Config, Embed
from bot.base import Command


class cmd(Command):
    """ A discord command instance. """

    name = "leaderboard"
    usage = "leaderboard"
    description = "Check the top 5 chatters."

    async def execute(self, arguments, message) -> None:
        cursor = await self.db.cursor()
        await cursor.execute(f"SELECT user_id, exp, level FROM levels ORDER BY level DESC, exp DESC")
        result = await cursor.fetchall()
        desc = ''
        v = 1
        for result in result:
            if v > 5:
                break

            if result[0] == None:
                continue

            user = self.bot.get_user(int(result[0]))
            lvl = result[2]
            desc += f'**{str(user)}** *(level {lvl})*\n'
            v += 1

        embed = Embed()
        embed.add_field(name='**Leaderboard Top 5**', value=desc)
        await message.channel.send(embed=embed)

        await cursor.close()

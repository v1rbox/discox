from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):

    name = "request_close"
    usage = "request_close <number_id>"
    description = "Close the request. Only mod can deal with it"

    async def execute(self, arguments, message) -> None:
        db = self.db
        cursor = await db.cursor()

        if arguments[0].isdigit() == False:
            embed = Embed(title="Invalid record")
            embed.set_color("red")
            await message.channel.send(embed=embed)
            return

        await cursor.execute(
            f"SELECT * FROM request WHERE Number_id = ?", (int(arguments[0]),)
        )
        res = await cursor.fetchone()

        if not res:

            embed = Embed(title="Invalid record")
            embed.set_color("red")
            await message.channel.send(embed=embed)
            return

        embed = Embed(
            title="Are you sure?",
            description="React 👍 if you wish to or 👎 if you don't want to. \nEstimate time: 1min",
        )
        embed.set_color("red")
        msg = await message.channel.send(embed=embed)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")

        reaction, user = await self.bot.wait_for(
            "reaction_add", timeout=60.0, check=None
        )
        if str(reaction) == "👍":
            new_cursor = await db.cursor()
            await new_cursor.execute(f"SELECT * FROM sqlite_sequence")
            res = await new_cursor.fetchall()

            await cursor.execute(
                f"DELETE FROM request WHERE Number_id=?", (int(arguments[0]),)
            )
            await cursor.execute(
                f"UPDATE sqlite_sequence SET seq = ? WHERE name = 'request'",
                (res[0][1] - 1,),
            )

            await cursor.execute(f"SELECT * FROM request")
            res = await cursor.fetchall()
            for i in range(0, len(res)):
                if i + 1 == int(res[i][0]):
                    continue
                await cursor.execute(
                    "UPDATE request SET Number_id = ? WHERE Number_id = ?",
                    (int(i) + 1, res[i][0]),
                )

            await db.commit()
            embed = Embed(title="The data has successfully been deleted!")
            await message.channel.send(embed=embed)

        elif str(reaction) == "👎":
            embed = Embed(title="The request has successfully been ignored!")
            await message.channel.send(embed=embed)

        await cursor.close()

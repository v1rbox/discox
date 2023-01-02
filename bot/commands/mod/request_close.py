from bot.config import Config, Embed
from bot.base import Command


class cmd(Command):

    name = "request_close"
    usage = "request_close <number_id>"
    description = "Close the request. Only mod can deal with it"

    async def execute(self, arguments, message) -> None:
        db = self.db
        cursor = await db.cursor()

        await cursor.execute(f"SELECT * FROM request WHERE Number_id = {int(arguments[0])}")
        res = await cursor.fetchone()

        if not res:

            embed = Embed(
                    title="Invalid number_id")
            embed.set_color("red")
            await message.channel.send(embed=embed)
            return

        embed = Embed(
                    title="Are you sure?", description="React 👍 if you wish to or 👎 if you don't want to. \nEstimate time: 1min")
        embed.set_color("red")
        await message.channel.send(embed=embed)
        
        
        reaction, user = await self.bot.wait_for('reaction_add',timeout=60.0,check=None)
        if str(reaction) == '👍':
            new_cursor = await db.cursor()
            await new_cursor.execute(f"SELECT * FROM sqlite_sequence")
            res = await new_cursor.fetchall()
            
            await cursor.execute(f"DELETE FROM request WHERE Number_id={int(arguments[0])}")
            await cursor.execute(f"UPDATE sqlite_sequence SET seq = {res[0][1] - 1} WHERE name = 'request'")
            
            await db.commit()
            embed = Embed(
                    title="The data has successfully deleted!")
            await message.channel.send(embed=embed)

        elif str(reaction) == '👎':
            embed = Embed(
                    title="The request has successfully ignored!")
            await message.channel.send(embed=embed)

        await cursor.close()
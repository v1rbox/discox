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
                    title="Are you sure?")
        embed.set_color("red")
        await message.channel.send(embed=embed)
        
        
        reaction, user = await self.bot.wait_for('reaction_add',timeout=60.0,check=None)
        if str(reaction) == '👍':
            await cursor.execute(f"DELETE FROM request WHERE Number_id={int(arguments[0])}")
            return
        elif str(reaction) == '👎':
            return 
        
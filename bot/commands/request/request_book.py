from bot.config import Config, Embed
from bot.base import Command


class cmd(Command):

    name = "request_book"
    usage = "request_book"
    description = "List of every requests in order."

    async def execute(self, arguments, message) -> None:
        db = self.db
        cursor = await db.cursor()
        await cursor.execute("SELECT * FROM request WHERE Number_id = 1")
        row = await cursor.fetchone()
        if not row:
            await message.channel.send("Couldn't find anything in database")
        else:
            await cursor.execute("SELECT * FROM request")
            rows = await cursor.fetchall()

            final_message = ""
            for row in rows:
                # implement number_id
                number_id = row[0]

                # implement member_id
                split_member_id = row[1].split(" ")
                member_name = split_member_id[2].replace("'", "")[5:]
                member_discriminator = split_member_id[3].replace("'", "")[14:]
                member_id = member_name + "#" + member_discriminator

                # implement title
                title = row[2]

                final = f"{number_id}. '{title}' by {member_id}"

                final_message += f"{final}\n"

            embed = Embed(title="List of all the requests:",
                          description=final_message)
            await message.channel.send(embed=embed)

        await cursor.close()

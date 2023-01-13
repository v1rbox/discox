from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):

    name = "request_book"
    usage = "request_book <number_id>"
    description = "List of every requests in order if the <number_id> == 0. Otherwise, just shown up the information in that number_id row"

    def display_row(self, row: tuple) -> str:

        """
        Display tuple (represented of the row in the table)
        """
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

        return final

    async def execute(self, arguments, message) -> None:
        if arguments[0] == "0":
            db = self.db
            cursor = await db.cursor()
            await cursor.execute("SELECT * FROM request WHERE Number_id = 1")
            row = await cursor.fetchone()
            if not row:
                embed = Embed(title="Couldn't find anything in the database")
                embed.set_color("red")
                await message.channel.send(embed=embed)
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

                embed = Embed(
                    title="List of all the requests:", description=final_message
                )
                await message.channel.send(embed=embed)

            await cursor.close()
        else:
            if arguments[0].isdigit() == False:
                embed = Embed(title="Invalid argument")
                embed.set_color("red")
                await message.channel.send(embed=embed)
                return

            arguments[0] = int(arguments[0])
            db = self.db

            cursor = await db.cursor()
            await cursor.execute(
                f"SELECT * FROM request WHERE Number_id = ?", (arguments[0],)
            )
            row = await cursor.fetchone()

            if not row:
                embed = Embed(title="Invalid number_id")
                embed.set_color("red")
                await message.channel.send(embed=embed)
                return

            final_message = self.display_row(row)
            final_message += f"\nDescription: ```{row[3]}```"
            embed = Embed(
                title=f"Show the information of the row with the given number_id: `{arguments[0]}`",
                description=final_message,
            )
            await message.channel.send(embed=embed)
            await cursor.close()

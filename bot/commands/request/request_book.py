from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):
    """
    INFO: This command is one of the support commands of the request command. It is used to show the request database.
    HOW TO USE:

    - Type in `v!req request_book <number_id_of_the_request>`
    The number_id here is just basically the order number of the request.
    If you want to show all of the database, the number_id will be 0

    For example:
        `v!req request_book 1` will show the request with the number_id: 1
        `v!req request_book 0` will show all of the request database
    """

    name = "request_book"
    usage = "request_book <number_id>"
    description = "List of every requests in order if the <number_id> == 0. Otherwise, just shown up the information in that number_id row"

    def display_request(self, row: tuple) -> str:
        """

        INFO: this method is used to display the request in the request table.
        After cursor.fetchone(), it will return a tuple which represents the request in the database. To make it easier to read, this function will reformat the tuple and then print out the formatted string.

        HOW IT WORKS:
        The tuple will look like this:
            (<number_id>, <author_information>, <title>, <description>, <upvote>, <downvote>, <pending_close>)
        For example:
            (1, "<Member id=917681283595919391 name='imindMan' discriminator='8536' bot=False nick=None guild=<Guild id=1032277950416035930 name='imindworld' shard_id=0 chunked=True member_count=36>>", 'Hello', 'Hello guys', 0, 0, 0)
        The bot will then use this tuple, reformat it to a string, then return it
        THe final result will look like this (based on the example):
            1. 'Hello' by imindMan#8536
               Vote count: U:0 - D:0 - G:0
               Pending close: 0
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

        # implement upvote
        upvote = row[4]
        # downvote
        downvote = row[5]

        # Pending_close
        pending_close = row[6]
        final = f"{number_id}. '{title}' by {member_id}\nVote count: U:{upvote} - D:{downvote} - G:{int(upvote) - int(downvote)}\nPending close: {pending_close}"
        return final

    async def execute(self, arguments, message) -> None:
        """
        MAIN EXECUTION:
            After the user type in the command, the bot will check if the arguments[0] (the first argument) is 0 or another number. If it's 0, then the bot will select the request table in the database and show all of them in a specific format that looks like this:
                List of all the requests:
                <number_id>. <title> by <member_id>.
                    Vote count: U:<upvote> - D:<downvote> - G:<upvote> - <downvote>
                    Pending close: <pending_close>
                    ...
            If it's another number, then the bot will select that row with that number_id. If the row doesn't exist, it throws error. Otherwise, it will show up like this:
                Show the information of the row with the given number_id: <number_id>
                    <number_id>. <title> by <member_id>.
                        Vote count: U:<upvote> - D:<downvote>
                        Pending close: <pending_close>
                    Description:
                        <description>
        """

        # in case if arguments[0] == "0"
        if arguments[0] == "0":
            # Select from the database
            rows = await self.db.raw_exec_select("SELECT * FROM request")
            if len(rows) == 0:
                # Throw error if the bot doesn't find anything in the database
                embed = Embed(title="Couldn't find anything in the database")
                embed.set_color("red")
                await message.channel.send(embed=embed)
            else:
                # Display as normally
                final_message = ""
                for row in rows:
                    # Looping through every elements in the database
                    final = self.display_request(row)
                    final_message += f"{final}\n"
                # Print all of them
                embed = Embed(
                    title="List of all the requests:", description=final_message
                )
                await message.channel.send(embed=embed)
        else:
            # Get the request based on the number_id
            arguments[0] = int(arguments[0])

            row = await self.db.raw_exec_select(
                f"SELECT * FROM request WHERE Number_id = ?", (arguments[0],)
            )
            if len(row) == 0:
                embed = Embed(title="Invalid number_id")
                embed.set_color("red")
                await message.channel.send(embed=embed)
                return

            row = row[0]
            # Display it
            final_message = self.display_request(row)
            final_message += f"\nDescription: ```{row[3]}```"
            embed = Embed(
                title=f"Show the information of the row with the given number_id: `{arguments[0]}`",
                description=final_message,
            )
            await message.channel.send(embed=embed)

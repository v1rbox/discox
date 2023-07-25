from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):
    """
    INFO:
    This command is a support command of request, it's used to close the request after reviewing and voting
    Easily by using `v!request_close <number_id>`, which <number_id> is the number_id of the request
    This command only works if the user is an administrator. The bot will detect if you are an administrator by checking your roles. If you have one of the role in the mod_role_id list (assume that you have configured it in the .env file), then you can use this command.

    """

    name = "request_close"
    usage = "request_close <number_id>"
    description = "Close a request. Only a mod can use this command."

    async def execute(self, arguments, message) -> None:
        """
        HOW IT WORKS:
            After entering the command, the bot will check that if the number_id is valid. If that's the case
            then the bot will send a message: Are you sure? and some options (as reactions).
            If the user's reaction is 👍, then the bot will delete the request out of the database (close the request)
            If the user's reaction is 👎, then the bot will ignore your request.
        """

        # Check if the number_id is valid
        if arguments[0].isdigit() == False:
            embed = Embed(title="Invalid record")
            embed.set_color("red")
            await message.channel.send(embed=embed)
            return

        res = await self.db.raw_exec_select(
            f"SELECT * FROM request WHERE Number_id = ?", (int(arguments[0]),)
        )

        if not res:
            embed = Embed(title="Invalid record")
            embed.set_color("red")
            await message.channel.send(embed=embed)
            return

        # Send the message to the user
        embed = Embed(
            title="Are you sure?",
            description="React 👍 if you wish to or 👎 if you don't want to. \nEstimate time: 1min",
        )
        embed.set_color("red")
        msg = await message.channel.send(embed=embed)
        # Add some options to choose
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")

        # Waiting for the user to react and then take that information to implement the next job
        reaction, user = await self.bot.wait_for(
            "reaction_add", timeout=60.0, check=None
        )

        # delete the request if the user reacts with a thumb up
        if str(reaction) == "👍":
            """
            HOW IT WORKS:
                By default, the request number_id is an attribute with the AUTO_INCREMENT key.
                That's why when deleting a request, we also have to update the number_id and AUTO_INCREMENT key.
                Since we use mysql, we can just ALTER TABLE request AUTO_INCREMENT = (curr_auto_incre - 1)
                For example, assuming we have a database looks like this:
                    1. "Sample request 1" by Foo
                    2. "Sample request 2" by Bar
                    3. "Sample request 3" by Egg

                When we run this command and delete the "Sample request 2" request, the database will look like this:
                Table: request
                    1. "Sample request 1" by Foo
                    3. "Sample request 3" by Egg
                Table: sqlite_sequence
                    name: request, seq: 3

                Since we only have 2 requests left, the sqlite_sequence should be updated like this:
                    name: request, seq: 2 (this way, we can keep track of the number_id correctly in the next time)
                And then, we also need to run a loop, keep track of all the requests and update their number_id.
                So the final result should be:

                Table: request
                    1. "Sample request 1" by Foo
                    2. "Sample request 3" by Egg # the name doesn't matter
                Table: sqlite_sequence
                    name: request, seq: 2
            """
            # Get the current AUTO_INCREMENT value
            res = await self.db.raw_exec_select(
                f"SELECT `AUTO_INCREMENT` FROM  INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'discox' AND   TABLE_NAME   = 'request';"
            )

            # delete the request
            await self.db.raw_exec_commit(
                f"DELETE FROM request WHERE Number_id=?", (int(arguments[0]),)
            )
            # Update the sqlite_sequence
            await self.db.raw_exec_commit(
                f"ALTER TABLE request AUTO_INCREMENT = ?",
                (res[0][0] - 1,),
            )

            # And then run a loop to update the number_id
            res = await self.db.raw_exec_select(f"SELECT * FROM request")
            for i in range(0, len(res)):
                if i + 1 == int(res[i][0]):
                    continue
                await self.db.raw_exec_commit(
                    "UPDATE request SET Number_id = ? WHERE Number_id = ?",
                    (int(i) + 1, res[i][0]),
                )
            # Send a notification to the user
            embed = Embed(title="The data has successfully been deleted!")
            await message.channel.send(embed=embed)
        # otherwise, ignore
        elif str(reaction) == "👎":
            embed = Embed(title="The request has successfully been ignored!")
            await message.channel.send(embed=embed)

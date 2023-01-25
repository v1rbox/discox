import asyncio

import aiosqlite
from discord.message import Message

from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):
    """
    INFO: this is a request command. It's used for requesting the server to do something.
    When you request something to the server, maybe the administrators don't get that.The request command will ping to all the administrators to notice your request, so they can review it immediately or start voting for your request!
    Support multiple commands to deal with it, too: request_book, request_close, request_start_vote, request_end_vote and request_status.
    """

    name = "request"
    usage = "request"
    description = (
        "Add some recommendation to the server. Support multiple commands to deal with."
    )

    async def execute(self, arguments, message) -> None:
        """
        HOW DOES IT WORK?
        Well, when you type 'v!req request', it will automatically start an interactive chat to you. It will ask you some information about the request, and then once you fill all of them, the command will add it to the database and ping every moderators and administrators to review it.

        INFORMATION ABOUT THE REQUEST:
            - Title of the request: (the title variable)
            - Description of the request: (the description variable)
            - Your id: (the member_id variable) so we will know who made the request
        """

        # Implement the member_id
        member_id = message.author.__repr__()

        # Pre-check function if the message is in the right spot.
        def check(m):
            return m.channel == message.channel and m.author.id == message.author.id

        # Start asking the user to get the title of the request
        title_request = Embed(title="What is the title of the request?")
        await message.channel.send(embed=title_request)

        ## How it works: the bot trys to ask the user all the required information, then
        # wait for the user to type, if in 120 secs the bot doesn't get the information
        # it will automatically throw the error message. After getting the information
        # the bot will check if the message is valid, then continue the job.
        try:
            title = await self.bot.wait_for("message", timeout=120.0, check=check)
            description_request = Embed(
                title="What is the description of this request?"
            )

            await message.channel.send(embed=description_request)
            description = await self.bot.wait_for("message", timeout=120.0, check=check)

        except asyncio.TimeoutError:
            await message.channel.send("Timed out.")
            return

        # MAIN EXECUTION: after getting all the information, the bot will add all of the information to the database
        await self.db.raw_exec_commit(
            "INSERT INTO request(Member_id, Title, Description, Upvote, Downvote, Pending_close) VALUES(?, ?, ?, ?, ?, ?)",
            (member_id, title.content, description.content, 0, 0, 0),
        )
        # Notify the user that the bot has added the request to the database.
        embed = Embed(title="A request has been added!")
        await message.channel.send(message.author.mention, embed=embed)

        # Notify the administrators to review the request
        ping_roles = ""
        for i in self.category.config.mod_role_id:
            ping_roles += "<@&" + str(i) + ">"
        embed = Embed(title="A request has been added! Please consider to review it and start voting!")
        await message.channel.send(ping_roles, embed=embed)

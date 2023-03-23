from discord import member

from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):
    """
    INFO: this command shows the status of the request database
    The status of the request database will look like this:
        <List-of-the-requests-haven't-started-voting-yet>
        <List-of-the-pending-close-requests>

    """

    name = "request_status"
    usage = "request_status"
    description = "Show the current status of the request database"

    def display_request(self, row: tuple) -> str:
        """

        INFO: this method is used to display the request in the request table.
        After cursor.fetchone(), it will return a tuple which represents the request in the database. To make it easier to read, this function will reformat the tuple and then print out the formatted string.

        HOW IT WORKS:
        The tuple will look like this:
            (<number_id>, <author_information>, <title>, <description>, <upvote>, <downvote>, <pending_close>)
        For example:
            (1, "imindMan#8536", 'Hello', 'Hello guys', 0, 0, 0)
        The bot will then use this tuple, reformat it to a string, then return it
        THe final result will look like this (based on the example):
            1. 'Hello' by imindMan#8536

        """
        # implement number_id
        number_id = row[0]

        # implement member_id
        member_id = row[1]

        # implement title
        title = row[2]

        final = f"{number_id}. '{title}' by {member_id}"
        return final

    async def execute(self, arguments, message) -> None:
        """
        HOW IT WORKS:
            The bot first checks all of the requests and collect these types of data:
                    <List-of-the-requests-haven't-started-voting-yet>
                    <List-of-the-pending-close-requests>
                    <Vote-count-for-the-requests>
            After collecting all of them, it just prints out the result and that's it!

            <Requests-haven't-started-voting-yet>:
                Looping for all of the requests, then tracing back all the requests with the upvote and downvote = 0.
                Return a list of number_id.
            <Pending_close-requests>
                Looping for all of the requests, then tracing back all the requests with the pending_close = 1
                Also return a list of number_id

        """

        # getting all of the requests
        requests = await self.db.raw_exec_select("SELECT * FROM request")
        # initialize all the needed variable (self-described names also)

        requests_havent_started_voting = []
        requests_havent_started_voting_count = 0
        requests_pending_close = []
        requests_pending_close_count = 0

        # looping and filtering every information

        for request in requests:
            # checking if the request has upvote and downvote = 0

            if int(request[4]) == int(request[5]) == 0:
                requests_havent_started_voting.append(int(request[0]))
                requests_havent_started_voting_count += 1
            # checking if the request has pending_close = 1
            if int(request[6]) == 1:
                requests_pending_close.append(int(request[0]))
                requests_pending_close_count += 1

        # after that, print out every thing

        requests_havent_started_voting_list = ""
        requests_pending_close_list = ""

        for i in requests_havent_started_voting:
            requests_havent_started_voting_list += (
                self.display_request(requests[i - 1]) + "\n"
            )
        for i in requests_pending_close:
            requests_pending_close_list += self.display_request(requests[i - 1]) + "\n"

        message_to_show = f"Total amount of requests haven't started voting yet: {requests_havent_started_voting_count}. List all of them: \n{requests_havent_started_voting_list}\nTotal amount of requests pending close: {requests_pending_close_count}. List all of them: \n{requests_pending_close_list}"
        requests_havent_started_voting_embed = Embed(
            title=f"Total amount of requests haven't started voting yet:  {requests_havent_started_voting_count}",
            description=requests_havent_started_voting_list,
        )
        await message.channel.send(embed=requests_havent_started_voting_embed)
        requests_pending_close_embed = Embed(
            title=f"Total amount of requests pending close: {requests_pending_close_count}",
            description=requests_pending_close_list,
        )
        await message.channel.send(embed=requests_pending_close_embed)

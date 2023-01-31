import random

import aiohttp

from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):
    """Gets a Random Leet Code Problem"""

    name = "leetcode"
    usage = "leetcode <command>"
    description = "Generates a random leetcode problem, use info to find total number of problem, use gen to generate a new problem"
    async def execute(self, arguments, message) -> None:

        leet_code_api_url = "https://leetcode.com/api/problems/all"
        async with aiohttp.ClientSession() as ses:
            async with ses.get(leet_code_api_url) as resp:
                problem_data = await resp.json()
        total_problem = problem_data["num_total"]

        if arguments[0] == "info":
            embed = Embed(
                title="Leet Code Problem",
                description=f"Total number of problems generated : {total_problem}.\nRun `{Config.prefix}leetcode gen` to generate random problem. Happy Coding :))",
            )
            await message.channel.send(embed=embed)

        elif arguments[0] == "gen":

            # Picks a random number betwwn 0 and total number of problem in leetcode - 1
            problem_index = random.randint(0, total_problem - 1)

            # Picks a random problem from all problems in leetcode
            problem = problem_data["stat_status_pairs"][problem_index]

            # Generates problem id
            problem_id = problem["stat"]["question_id"]

            # Generated problem title
            problem_title = problem["stat"]["question__title"]

            # Specify if the problem is paid or free
            problem_access = problem["paid_only"]
            problem_status = None
            if problem_access:
                problem_status = "Paid"
            else:
                problem_status = "Free"

            # Specify the diffculty of the problem
            problem_difficulty_level = problem["difficulty"]["level"]
            problem_difficulty = None
            if problem_difficulty_level == 1:
                problem_difficulty = "Easy"
            elif problem_difficulty_level == 2:
                problem_difficulty = "Moderate"
            else:
                problem_difficulty = "Hard"

            # Creates the Leetcode URL
            problem_url = (
                "https://leetcode.com/problems/"
                + problem["stat"]["question__title_slug"]
                + "/"
            )

            embed = Embed(
                title=problem_title,
                description=f"Problem ID: {problem_id}\n\nProblem Details: {problem_url}\n\nProblem Status: {problem_status}\n\nProblem Difficulty : {problem_difficulty}",
            )

            await message.channel.send(embed=embed)

        else:
            raise KeyError(f"Command {arguments[0]} not found.")

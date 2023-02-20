from bot.base import Command
from bot.config import Config, Embed

import subprocess


class cmd(Command):
    """A discord command instance."""

    name = "version"
    usage = "version"
    description = "Returns the latest commit."

    async def execute(self, arguments, message) -> None:
        repoLink = subprocess.run(
            [
                "git",
                "remote",
                "get-url",
                "origin"
            ],
            capture_output=True,
        ).stdout.decode().split("\n")[0]
        commits = subprocess.run(
            [
                "git",
                "log",
                "-n 3",
                f"--format=[%h: %s - %an]({repoLink}/commit/%H)",
                "--decorate=short"
            ],
            capture_output=True,
        ).stdout.decode()
        embed = Embed(
          title="Latest commits",
          description=commits
        )
        await message.channel.send(embed=embed)

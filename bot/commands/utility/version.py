import subprocess

from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "version"
    usage = "version"
    description = "Returns the latest commits."

    async def execute(self, arguments, message) -> None:
        repoLink = (
            subprocess.run(
                ["git", "remote", "get-url", "origin"],
                capture_output=True,
            )
            .stdout.decode()
            .split("\n")[0]
        )
        commits = subprocess.run(
            [
                "git",
                "log",
                "-n 3",
                f"--format=[%h: %s - %an]({repoLink}/commit/%H)",
                "--decorate=short",
            ],
            capture_output=True,
        ).stdout.decode()
        diff_message = str(
            subprocess.run(
                ["git", "status"],
                capture_output=True,
            )
            .stdout.decode()
            .strip()
            .split("\n")[1]
        )

        embed = Embed(
            title="Latest commits",
            description=f"*{diff_message[15:].capitalize()}*\n{commits}",
        )
        await message.channel.send(embed=embed)

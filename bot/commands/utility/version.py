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
        commit_diff = int(
            subprocess.run(
                ["git", "rev-list", "--count", "HEAD..origin/main"],
                capture_output=True,
            )
            .stdout.decode()
            .strip()
        )
        diff_message = (
            f"*{commit_diff} commits behind remote*"
            if commit_diff
            else "*Up to date with remote*"
        )
        embed = Embed(title="Latest commits", description=f"{diff_message}\n{commits}")
        await message.channel.send(embed=embed)

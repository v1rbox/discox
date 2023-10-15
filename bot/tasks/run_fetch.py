import subprocess

from discord.ext.tasks import loop

from bot.base import Task


class TaskLoop(Task):
    @loop(minutes=5)
    async def execute(self) -> None:
        subprocess.run(["git", "fetch"])

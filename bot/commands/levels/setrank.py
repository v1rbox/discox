import discord

from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):
    """Set rank to other user. Only <@936357105760370729> can use this command."""

    name = "setrank"
    usage = "setrank <user> [exp]"
    description = "Set the rank for another user. Administrator only."

    async def execute(self, arguments, message) -> None:
        if message.author.id != 936357105760370729:
            raise ValueError("Improper permissions.")

        # Calculate level
        lvl = 0
        exp = int(arguments[1])
        while True:
            if exp >= (lvl + 1) * 25 + 100:
                lvl += 1
                exp -= lvl * 25 + 100
            else:
                break

        await self.db.raw_exec_commit("UPDATE levels SET level = ?, exp = ? WHERE user_id = ?", (lvl, exp, int(arguments[0])))
        await message.channel.send(f"Updated rank to {lvl}.{exp}")

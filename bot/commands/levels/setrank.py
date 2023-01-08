import discord

from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

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

        cursor = await self.db.cursor()

        await cursor.execute(f"DELETE FROM levels WHERE user_id = ?", (arguments[0],))
        await self.db.commit()

        sql = "INSERT INTO levels(exp, level, user_id) VALUES (?,?,?)"
        val = (exp, lvl, arguments[0])
        await cursor.execute(sql, val)
        await self.db.commit()

        await cursor.close()

        await message.channel.send(f"Updated rank to {lvl}.{exp}")

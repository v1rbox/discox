from bot.base import Event
from bot.config import Config, Embed


class event(Event):
    """A discord event instance."""

    name = "on_message"
    lastMsgAuthorId = None

    async def execute(self, message) -> None:
        if not message.author.bot:
            if self.lastMsgAuthorId != message.author.id:
                self.lastMsgAuthorId = message.author.id

                result = await self.db.raw_exec_select(
                    f"SELECT exp, level FROM levels WHERE user_id = '{message.author.id}'"
                )

                if len(result) == 0:
                    await self.db.raw_exec_commit(
                        "INSERT INTO levels(exp, level, user_id) VALUES (?,?,?)",
                        (1, 0, message.author.id),
                    )
                else:
                    await self.db.raw_exec_commit(
                        "UPDATE levels SET level = ?, exp = ? WHERE user_id = ?",
                        (result[0][1], result[0][0] + 1, message.author.id),
                    )

                    if result[0][0] + 1 >= result[0][1] * 25 + 100:
                        await self.db.raw_exec_commit(
                            "UPDATE levels SET level = ?, exp = ? WHERE user_id = ?",
                            (result[0][1] + 1, 0, message.author.id),
                        )

                        await message.channel.send(
                            f"Congratulations {message.author.mention}, you just advanced to level {result[0][1] + 1}!"
                        )

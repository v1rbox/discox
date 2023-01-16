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

                cursor = await self.db.cursor()
                await cursor.execute(
                    f"SELECT exp, level FROM levels WHERE user_id = '{message.author.id}'"
                )
                result = await cursor.fetchone()

                if result is None:
                    sql = "INSERT INTO levels(exp, level, user_id) VALUES (?,?,?)"
                    val = (1, 0, message.author.id)
                    await cursor.execute(sql, val)
                    await self.db.commit()
                else:
                    sql = "UPDATE levels SET level = ?, exp = ? WHERE user_id = ?"
                    val = (result[1], result[0] + 1, message.author.id)
                    await cursor.execute(sql, val)
                    await self.db.commit()

                    if result[0] + 1 >= result[1] * 25 + 100:
                        sql = "UPDATE levels SET level = ?, exp = ? WHERE user_id = ?"
                        val = (result[1] + 1, 0, message.author.id)
                        await cursor.execute(sql, val)
                        await self.db.commit()

                        await message.channel.send(
                            f"Congratulations {message.author.mention}, you just advanced to level {result[1] + 1}!"
                        )

                await cursor.close()

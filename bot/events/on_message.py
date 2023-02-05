from bot.base import Event
from bot.config import Config, Embed

import discord

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

            if isinstance(message.channel, discord.channel.DMChannel):
                channel = await self.bot.fetch_channel(Config.report_channel_id)
                found = False
                for i in channel.threads:
                    if i.name.startswith(str(message.author.id)) and len(i.applied_tags) == 1:
                        embed = Embed(description=message.content)
                        embed.set_author(name=str(message.author), icon_url=message.author.display_avatar.url)
                        await i.send(embed=embed)

                        for a in message.attachments:
                            await i.send(f"User sent an attachment `{a.filename}`\n{a.url}")

                        await message.add_reaction("✅")
                        found = True




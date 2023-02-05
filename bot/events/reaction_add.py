from bot.base import Event
from bot.config import Config, Embed


class event(Event):
    """A discord event instance."""

    name = "on_raw_reaction_add"

    async def execute(self, payload) -> None:
        REACTION = "⭐"
        if not payload.emoji.name == REACTION:
            return
        channelObj = await self.bot.fetch_channel(payload.channel_id)
        messageObj = await channelObj.fetch_message(payload.message_id)
        for reaction in messageObj.reactions:
            if not reaction == REACTION:
                pass
            if reaction.count >= 5:
                already = await self.db.raw_exec_select(
                    "SELECT message_id FROM starboard WHERE message_id = ?",
                    (messageObj.id,)
                )
                if len(already) == 0:
                    starboard = await self.bot.fetch_channel(Config.starboard_channel)
                    embed = Embed()
                    embed.set_color("yellow")
                    embed.set_footer(
                        text=f'{messageObj.author} • {reaction.count} stars',
                        icon_url=messageObj.author.display_avatar.url
                    )
                    if messageObj.content:
                        embed.title = messageObj.content
                    if len(messageObj.attachments) != 0:
                        if "image" in messageObj.attachments[0].content_type:
                            embed.set_image(url=messageObj.attachments[0].url)
                            await starboard.send(embed=embed)
                        else:
                            content = ''
                            if messageObj.content:
                                content += f'{messageObj.content} • '
                            content += f'{reaction.count} stars • by {messageObj.author}\n{messageObj.attachments[0].url}'
                            await starboard.send(content)
                    await self.db.raw_exec_commit(
                        """INSERT INTO starboard(message_id) VALUES (?)""",
                        (messageObj.id,)
                    )

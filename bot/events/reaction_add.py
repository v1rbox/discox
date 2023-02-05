from bot.base import Event
from bot.config import Config, Embed


class event(Event):
    """A discord event instance."""

    name = "on_raw_reaction_add"

    async def execute(self, payload) -> None:
        REACTION = "⭐"
        starboard = await self.bot.fetch_channel(Config.starboard_channel)
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
                    (messageObj.id,),
                )
                if len(already) == 0:
                    board_message = None
                    embed = Embed()
                    embed.set_color("yellow")
                    embed.set_footer(
                        text=f"{messageObj.author} • {reaction.count} stars",
                        icon_url=messageObj.author.display_avatar.url,
                    )
                    if messageObj.content:
                        embed.title = messageObj.content
                    if len(messageObj.attachments) != 0:
                        if "image" in messageObj.attachments[0].content_type:
                            embed.set_image(url=messageObj.attachments[0].url)
                            board_message = await starboard.send(embed=embed)
                        else:
                            content = ""
                            if messageObj.content:
                                content += f"{messageObj.content} • "
                            content += f"{reaction.count} stars • by {messageObj.author}\n{messageObj.attachments[0].url}"
                            board_message = await starboard.send(content)
                    else:
                        board_message = await starboard.send(embed=embed)
                    await self.db.raw_exec_commit(
                        """INSERT INTO starboard(message_id, board_message_id) VALUES (?,?)""",
                        (
                            messageObj.id,
                            board_message.id,
                        ),
                    )
                else:
                    board_message_id = await self.db.raw_exec_select(
                        "SELECT board_message_id FROM starboard WHERE message_id = ?",
                        (messageObj.id,),
                    )
                    board_message_id = board_message_id[0][0]
                    board_message = await starboard.fetch_message(board_message_id)
                    if (
                        len(board_message.embeds) != 0
                        and board_message.embeds[0].footer
                    ):
                        new_embed = board_message.embeds[0]
                        new_embed.set_footer(
                            text=f"{messageObj.author} • {reaction.count} stars",
                            icon_url=messageObj.author.display_avatar.url,
                        )
                        if messageObj.content:
                            new_embed.title = messageObj.content
                        await board_message.edit(embed=new_embed)
                    else:
                        content = ""
                        if messageObj.content:
                            content += f"{messageObj.content} • "
                        content += f"{reaction.count} stars • by {messageObj.author}\n{messageObj.attachments[0].url}"
                        await board_message.edit(content=content)

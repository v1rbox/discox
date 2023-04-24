import enum
from re import search, sub

import discord

from bot.base import Event
from bot.config import Config, Embed


class EnumPollType(enum.Enum):
    single = "single"
    multiple = "multiple"


class event(Event):
    """A discord event instance."""

    name = "on_raw_reaction_add"

    async def execute(self, *args, **kwargs) -> None:
        await self.starboard(*args, **kwargs)
        await self.poll_single_or_multiple(*args, **kwargs)

    async def poll_single_or_multiple(
        self, payload: discord.RawReactionActionEvent
    ) -> None:
        bind = [
            "0️⃣",
            "1️⃣",
            "2️⃣",
            "3️⃣",
            "4️⃣",
            "5️⃣",
            "6️⃣",
            "7️⃣",
            "8️⃣",
            "9️⃣",
            "✅",
            "❌",
        ]
        if payload.emoji.name not in bind:
            return
        message = await (
            await self.bot.fetch_channel(payload.channel_id)
        ).fetch_message(payload.message_id)
        if message.author.id != self.bot.user.id:
            return
        type = (
            await self.db.raw_exec_select(
                "SELECT type FROM polls WHERE message_id = ?", (message.id,)
            )
        )[0][0]
        # now check for it's channel id and message id if its same
        message_id, channel_id = (
            await self.db.raw_exec_select(
                "SELECT message_id, channel_id FROM polls WHERE message_id = ?",
                (message.id,),
            )
        )[0]
        if message_id != message.id or channel_id != message.channel.id:
            return
        if type == EnumPollType.single.value:
            for reaction in message.reactions:
                print(reaction.emoji, payload.emoji.name)
                if reaction.emoji == payload.emoji.name:
                    continue
                try:
                    await message.remove_reaction(reaction.emoji, payload.member)
                except:
                    continue
        elif type == EnumPollType.multiple.value:
            pass

    async def starboard(self, payload: discord.RawReactionActionEvent) -> None:
        IMAGE_REGEX = "http(s)?:([\/|.|\w|\s]|-)*\.(?:jpg|gif|png|jpeg)(\?(.[^\s]*))?"
        REACTION = "⭐"
        starboard = await self.bot.fetch_channel(Config.starboard_channel)
        if payload.emoji.name != REACTION:
            return
        channelObj = await self.bot.fetch_channel(payload.channel_id)
        messageObj = await channelObj.fetch_message(payload.message_id)
        if messageObj.author.id == self.bot.user.id:
            return
        for reaction in messageObj.reactions:
            if reaction.emoji != REACTION:
                continue
            if reaction.count >= 5:
                already = await self.db.raw_exec_select(
                    "SELECT message_id FROM starboard WHERE message_id = ?",
                    (messageObj.id,),
                )
                if len(already) == 0:
                    board_message = None
                    embed = Embed()
                    embed.set_color("yellow")
                    embed.set_author(
                        name=f"{messageObj.author}",
                        url=f"https://discord.com/users/{messageObj.author.id}",
                        icon_url=messageObj.author.display_avatar.url,
                    )
                    embed.add_field(
                        name="Original", value=f"[Jump!]({messageObj.jump_url})"
                    )

                    if messageObj.content:
                        embed.description = messageObj.content
                    elif "MessageType.premium_guild" in str(messageObj.type):
                        embed.description = (
                            f"{messageObj.author} boosted the server :sunglasses:"
                        )
                    if len(messageObj.attachments) != 0:
                        if "image" in messageObj.attachments[0].content_type:
                            embed.set_image(url=messageObj.attachments[0].url)
                            board_message = await starboard.send(
                                content=f"{REACTION} **{reaction.count}**", embed=embed
                            )
                        else:
                            attachment_name = sub(
                                "http(s)?:\/\/.*\/attachments\/.*\/",
                                "",
                                messageObj.attachments[0].url,
                            )
                            embed.add_field(
                                name="Attachment",
                                value=f"[{attachment_name}]({messageObj.attachments[0].url})",
                            )
                            board_message = await starboard.send(
                                content=f"{REACTION} **{reaction.count}**", embed=embed
                            )

                    else:
                        direct_image_link = search(IMAGE_REGEX, messageObj.content)
                        if direct_image_link:
                            embed.set_image(url=direct_image_link.group())
                            if len(sub(IMAGE_REGEX, "", messageObj.content)) == 0:
                                embed.description = None
                            else:
                                embed.description = sub(
                                    IMAGE_REGEX, "[image link]", messageObj.content
                                )
                        board_message = await starboard.send(
                            content=f"{REACTION} **{reaction.count}**", embed=embed
                        )
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
                    new_embed = board_message.embeds[0]
                    new_embed.set_author(
                        name=f"{messageObj.author}",
                        url=f"https://discord.com/users/{messageObj.author.id}",
                        icon_url=messageObj.author.display_avatar.url,
                    )
                    if messageObj.content:
                        new_embed.description = messageObj.content

                    direct_image_link = search(IMAGE_REGEX, messageObj.content)
                    if direct_image_link:
                        new_embed.set_image(url=direct_image_link.group())
                        if len(sub(IMAGE_REGEX, "", messageObj.content)) == 0:
                            new_embed.description = None
                        else:
                            new_embed.description = sub(
                                IMAGE_REGEX, "[image link]", messageObj.content
                            )
                    if not direct_image_link and len(messageObj.attachments) == 0:
                        new_embed.set_image(url=None)
                    await board_message.edit(
                        content=f"{REACTION} **{reaction.count}**", embed=new_embed
                    )

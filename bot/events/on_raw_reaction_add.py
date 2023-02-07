from re import search, sub

from bot.base import Event
from bot.config import Config, Embed
import typing
import discord
import datetime
import enum

class EnumPollType(enum.Enum):
    single = "single"
    multiple = "multiple"

class event(Event):
    """A discord event instance."""

    name = "on_raw_reaction_add"

    async def execute(self, *args, **kwargs) -> None:
        await self.starboard(*args, **kwargs)
        await self.poll_checker(*args, **kwargs)
        
    async def convert_and_typehint_this(self,a: tuple[typing.Any]) -> tuple[
        discord.Guild,
        discord.TextChannel,
        discord.Message,
        int,
        datetime.datetime,
        bool,
        EnumPollType
    ]:
        j = self.bot.get_channel(a[1])
        return tuple(
            self.bot.get_guild(a[0]),
            j,
            await j.fetch_message(a[2]),
            int(a[3]),
            datetime.datetime.fromtimestamp(int(a[4])),
            bool(a[5]),
            EnumPollType(a[6])
        )
        
    async def poll_checker(self, payload: discord.RawReactionActionEvent):
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        a = await self.db.raw_exec_select(
            "SELECT * FROM polls WHERE guild_id = ? AND channel_id = ? AND message_id = ?",
            (
                message.guild.id,
                message.channel.id,
                message.id
            )
        )
        assert a and a[0], "No polls found with that ID"
        info = self.convert_and_typehint_this(a[0])
        
    async def starboard(self, payload: discord.RawReactionActionEvent) -> None:
        IMAGE_REGEX = "http(s)?:([\/|.|\w|\s]|-)*\.(?:jpg|gif|png|jpeg)"
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
                        await board_message.edit(
                            content=f"{REACTION} **{reaction.count}**", embed=new_embed
                        )

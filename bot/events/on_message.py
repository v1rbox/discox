import io

import aiohttp
import discord
import yarl
from PIL import Image

from bot.base import Event
from bot.config import Config, Embed


class event(Event):
    """A discord event instance."""

    name = "on_message"
    lastMsgAuthorId = None

    async def execute(self, message: discord.Message) -> None:
        await self.check_level(message)
        await self.check_is_link_to_message(message)

    async def check_level(self, message: discord.Message) -> None:
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
                    # Checks if user is an active member
                    if result[0][1] >= 3:
                        active_member_name = "Active Member"
                        active_member_color = discord.Color.blue()
                        # Checks if role already exits, if not, creates it
                        if active_member_name not in [
                            x.name.lower() for x in message.guild.roles
                        ]:
                            await message.guild.create_role(
                                name=active_member_name, colour=active_member_color
                            )

                        # Adds user to active member role
                        for role in message.guild.roles:
                            if role.name.lower() == active_member_name.lower():
                                await message.author.add_roles(
                                    role               
                                )
                                break

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
                    if (
                        i.name.startswith(str(message.author.id))
                        and len(i.applied_tags) == 1
                    ):
                        embed = Embed(description=message.content)
                        embed.set_author(
                            name=str(message.author),
                            icon_url=message.author.display_avatar.url,
                        )
                        await i.send(embed=embed)

                        for a in message.attachments:
                            await i.send(
                                f"User sent an attachment `{a.filename}`\n{a.url}"
                            )

                        await message.add_reaction("✅")
                        found = True

    async def check_is_link_to_message(self, message: discord.Message) -> None:
        content = message.content
        j = message
        # check if message have the link (even though it have message content)
        if "https://discord.com/channels/" in content:
            """
            ex:
            https://discord.com/channels/1052597660860821604/1057273716603617311/1089607678466212030

            first part is guild id
            second part is channel id
            third part is message id
            """
            # trim out every text except the link
            content = yarl.URL(
                content[content.find("https://discord.com/channels/") :].split(" ")[0]
            )
            assert content.host == "discord.com"
            assert content.path.startswith("/channels/")
            assert len(content.parts) == 5  # oh well it contains root too

            guild_id = int(content.parts[2])
            channel_id = int(content.parts[3])
            message_id = int(content.parts[4])

            guild = self.bot.get_guild(guild_id)
            assert guild is not None
            channel = guild.get_channel(channel_id)
            assert channel is not None
            message = await channel.fetch_message(message_id)

            embed = Embed(description=message.content)
            embed.set_author(
                name=str(message.author.display_name),
                icon_url=message.author.display_avatar.url,
            )
            embed.set_footer(
                text=f"Sent in {channel.name}. Embed only supports up to 4 picture attachments only!"
            )
            s = []
            for a in message.attachments:
                if await self.is_image(a.url):
                    e = Embed(url="https://dummyahhnolongerexist.com")
                    e.set_image(url=a.url)
                    s.append(e)
            await j.reply(embeds=[embed, *s])

    async def is_image(self, url: str) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    f = io.BytesIO(await resp.read())
                    try:
                        Image.open(f)
                        return True
                    except:
                        return False
                else:
                    return False

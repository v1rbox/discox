"""

"""

import discord
import orjson
from datetime import datetime
from bot.base import Command
from bot.config import Embed

from .__ui import PollButtons


class cmd(Command):
    name = "create"
    description = "Create a poll. Separate everything with commas. Question will be taken as the first argument. Description will be taken as the second argument (you can leave it alone with just give it blank value like this 'question,,a,b,c'). Else it is options."
    usage = "create <multiple_or_single> <*infos>"

    async def react_with_buttons(self, counts: int) -> None:
        return PollButtons(counts, self.when_clicked, self.when_timeout)

    async def when_clicked(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ) -> None:
        cursor: dict = orjson.loads(
            (
                await self.db.raw_exec_select(
                    "SELECT votes FROM polls WHERE message_id = ?",
                    (interaction.message.id,),
                )
            )[0][0]
        )
        type = await self.db.raw_exec_select("SELECT type FROM polls WHERE message_id = ?", (interaction.message.id,))
        if interaction.user.id in cursor["votes"][button.label]["users"] and type == "single":
            return
        elif interaction.user.id not in cursor["votes"][button.label]["users"] and type == "single":
            cursor["votes"][button.label]["users"].append(interaction.user.id)
            cursor["votes"][button.label]["count"] += 1
        elif type == "multiple":
            cursor["votes"][button.label]["users"].append(interaction.user.id)
            cursor["votes"][button.label]["count"] += 1
        else:
            raise ValueError("Unknown type or unreachable code.")
        await self.db.raw_exec_commit(
            "UPDATE polls SET votes = ? WHERE message_id = ?",
            (orjson.dumps(cursor), interaction.message.id),
        )
        h = await self.db.raw_exec_select(
            "SELECT message_id, guild_id, channel_id FROM polls WHERE message_id = ?",
            (interaction.message.id,),
        )
        guild = self.bot.get_guild(int(h[0][1]))
        assert guild is not None, "Guild not found."
        channel = guild.get_channel(int(h[0][2]))
        assert channel is not None, "Channel not found."
        message = await channel.fetch_message(int(h[0][0]))
        assert message is not None, "Message not found."
        embed = message.embeds[1]
        assert embed is not None, "Embed not found."
        embed.clear_fields()
        embed.add_field(name="Votes", value=cursor["votes"], inline=False)
        await message.edit(embeds=[message.embeds[0], embed])

    async def when_timeout(self, view: discord.ui.View) -> None:
        pass

    async def execute(self, arguments: list[str], message) -> None:
        assert arguments[0] not in ["single", "multiple"], "You need to specify the type of poll."
        poll_type = arguments[0]
        arguments = arguments[1].split(",")
        question = arguments[0]
        assert question != "", "Question cannot be empty."
        assert len(arguments) > 2, "You need at least 2 options."
        description = arguments[1]
        options = arguments[2:]
        embed = Embed(title=question, description=description)
        embed.set_footer(text="Poll created by " + message.author.name)
        embed.set_thumbnail(url=message.author.avatar_url)
        for i in range(len(options)):
            embed.add_field(name=str(i), value=options[i], inline=False)
        view = None
        emoji = False
        if len(options) > 5:
            view = await self.react_with_buttons(len(options))
        elif len(options) > 10:
            emoji = True
        msg: discord.Message = await message.channel.send(embed=embed, view=view)
        if emoji:
            for i in range(len(options)):
                await msg.add_reaction(str(i))
        else:
            await msg.delete()
            raise NotImplementedError("Unreachable code.")
        
        await self.db.raw_exec_commit(
            "INSERT INTO polls VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                message.guild.id,
                message.channel.id,
                msg.id,
                orjson.dumps(
                    {
                        "votes":{
                            x: {
                                "counts": 0,
                                "users": [],
                                "name": i,
                            } for x, i in enumerate(options)
                        },
                        
                    }
                ),
                datetime.now().timestamp(),
                True,
                poll_type,
                
            )
        )

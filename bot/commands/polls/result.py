import discord

from bot.base import Command
from bot.config import Embed


class cmd(Command):
    name = "result"
    description = "Get the result of a poll."
    usage = "result <message_id>"

    async def execute(self, arguments: list[str], message: discord.Message) -> None:
        try:
            channel_id = (
                await self.db.raw_exec_select(
                    "SELECT channel_id FROM polls WHERE message_id = ?", (arguments[0],)
                )
            )[0]
        except IndexError:
            return await message.channel.send(
                embed=Embed(
                    title="This message is not a poll.",
                    description="This message is not a poll. Please make sure you are using the correct message id.",
                    color=discord.Color.red(),
                )
            )
        message = await (await self.bot.fetch_channel(channel_id[0])).fetch_message(
            arguments[0]
        )
        embed = Embed(
            title=f"Poll Result: {message.embeds[0].title}",
            description=f"Poll result. {len(message.reactions)} options. {sum([x.count for x in message.reactions]) - len(message.reactions)} votes.",
            color=message.embeds[0].color,
        )
        if not message.reactions[0].emoji in ["✅", "❌"]:
            for i in range(len(message.embeds[0].fields)):
                embed.add_field(
                    name=message.embeds[0].fields[i].name,
                    value=f"{message.reactions[i].count - 1} votes out of {sum([x.count-1 for x in message.reactions])}. ({self.calc_percent(message.reactions[i].count-1, sum([x.count for x in message.reactions]) - len(message.reactions))}%)",
                    inline=False,
                )
        else:
            embed.add_field(
                name="True",
                value=f"{message.reactions[0].count - 1} votes out of {sum([x.count-1 for x in message.reactions])}. ({self.calc_percent(message.reactions[0].count-1, sum([x.count for x in message.reactions]) - len(message.reactions))}%)",
                inline=False,
            )
            embed.add_field(
                name="False",
                value=f"{message.reactions[1].count - 1} votes out of {sum([x.count-1 for x in message.reactions])}. ({self.calc_percent(message.reactions[1].count-1, sum([x.count for x in message.reactions]) - len(message.reactions))}%)",
                inline=False,
            )
        await message.channel.send(embed=embed)

    def calc_percent(self, number: int, total: int) -> int:
        return round((number / total) * 100, 2)

from bot.base import Event
from bot.config import Config, Embed


class event(Event):
    """A discord event instance."""

    name = "on_raw_reaction_add"

    async def execute(self, payload) -> None:
        REACTION = "star"
        if not payload.emoji.name == REACTION:
            return
        channelObj = await self.bot.fetch_channel(payload.channel_id)
        messageObj = await channelObj.fetch_message(payload.message_id)
        for reaction in messageObj.reactions:
            if not reaction == REACTION:
                pass
            if reaction.count == 5:
                starboard = await self.bot.fetch_channel(Config.starboard_channel)
                embed = Embed(
                    
                )
                await starboard.send(embed=embed)

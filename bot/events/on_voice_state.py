from bot.base import Event
from bot.config import Config, Embed


class event(Event):
    """A discord event instance."""

    name = "on_voice_state_update"

    async def execute(self, member, before, after) -> None:
        if "Voice Channel #" in before.channel.name and len(before.channel.members) == 0:
            await before.channel.delete(reason="Empty channel")
        if after.channel is not None and "Create VC" in after.channel.name:
            category = after.channel.category
            if len(category.voice_channels) > 6:
                await member.move_to(None, reason="No more available voice channels")
                await member.send("No more available voice channels.")
            else:
                channel = await category.create_voice_channel(
                    f"Voice Channel #{len(category.voice_channels)}"
                )
                await member.move_to(channel, reason="Created private channel")

import random

from bot.config import Config, Embed
from bot.base import Event


class event(Event):
    """ A discord event instance. """

    name = "on_member_join"

    def get_message(self, userId) -> str:
        with open("bot/assets/join_messages.txt", "r") as file:
            text = file.read()
            list = text.split("\n")
            message = random.choice(list)
            return message.replace("User", f"<@{userId}>")

    async def execute(self, member) -> None:
        message = self.get_message(str(member.id))
        embed = Embed(
            title="Welcome!",
            description=message
        )
        avatar = member.display_avatar.url
        embed.set_thumbnail(url=avatar)
        channel = await member.guild.fetch_channel(Config.join_message_channel)
        joinMessage = await channel.send(embed=embed)
        await joinMessage.add_reaction("👋")
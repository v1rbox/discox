from bot.config import Config, Embed
from bot.base import Event

class event(Event):
    """ A discord event instance. """

    name = "on_raw_reaction_add"

    async def execute(self, payload) -> None:
        print(payload)
        print(self.db)

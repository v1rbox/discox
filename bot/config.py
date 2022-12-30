from discord.embeds import Embed as DiscordEmbed
from discord import Colour

import datetime


class Embed(DiscordEmbed):
    """ Custom implementation of a discord embed object. """

    def __init__(self, *args, **kwargs) -> None:
        DiscordEmbed.__init__(self, *args, **kwargs)

        self.colors = {
            "green": Colour(int("38842c", 16)),
            "red": Colour(int("bf3036", 16)),
        }
        self.set_footer(
            text="Virbox Community Bot",
            icon_url="https://cdn.discordapp.com/icons/1052597660860821604/8fd53af279aa7d8d77a0451776c4fa35.webp?size=96"
        )
        self.timestamp = datetime.datetime.now()

        self.set_color("green")

    def set_color(self, color: str) -> None:
        """ Set a color from the default colorlist. """
        self.color = self.colors[color]


class Config:
    token: str = "MTA1NzI2NzI1Mjg5NTk2MTA4OA.Gf5jPq.ojX-ISHyGL6W6bf5SsUmbpmW2i5_Wa4mSiWH38"
    prefix: str = "v!"
    mod_role_id: int = 1057253751699816459

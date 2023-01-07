from discord.embeds import Embed as DiscordEmbed
from discord import Colour

import datetime


class Embed(DiscordEmbed):
    """ Custom implementation of a discord embed object. """
    def __init__(self, *args, **kwargs) -> None:
        DiscordEmbed.__init__(self, *args, **kwargs)

        # No need to make it public, so we make it private
        self.__colors = {
            "green": Colour(int("38842c", 16)),
            "red": Colour(int("bf3036", 16)),
            "blue": Colour(int("0d00ff", 16)),
            "yellow": Colour(int("f2ff00", 16)),
            "magenta": Colour(int("ff00ff", 16)),
            "brown": Colour(int("2b1313", 16)),
            "purple": Colour(int("5300b0", 16)),
            "pink": Colour(int("ff00fc", 16)),
            "black": Colour(int("000000", 16)),
            "white": Colour(int("ffffff", 16)),
            "cyan": Colour(int("00ffff", 16)),
            "grey": Colour(int("696969", 16)),  # yeah the funny number is grey

            "lightgreen": Colour(int("89f292", 16)),
            "lightred": Colour(int("ff7171", 16)),
            "lightblue": Colour(int("807bff", 16)),
            "lightyellow": Colour(int("f7ff80", 16)),
            "lightmagenta": Colour(int("ff8dfc", 16)),
            "lightbrown": Colour(int("956767", 16)),
            "lightpurple": Colour(int("bf67ff", 16)),
            "lightpink": Colour(int("ff88dc", 16)),
            "lightcyan": Colour(int("bcfbff", 16)),
        }

        self.set_footer(
                text="Virbox Community Bot", 
                icon_url="https://cdn.discordapp.com/icons/1052597660860821604/8fd53af279aa7d8d77a0451776c4fa35.webp?size=96"
            )
        self.timestamp = datetime.datetime.now()

        self.set_color("green")

    def set_color(self, color: str) -> None:
        """ Set a color from the default colorlist. """
        self.color = self.__colors[color]


class Config:
    token: str = "OTY4NTI5MzcyOTIxMzUyMjMz.G_OLSs.r7nypIaYVWHNLjJ54jsHpvuK4dRbD9GoIDjJ5o"
    prefix: str = "v!"
    mod_role_id: list[int] = [1057253751699816459]


if __name__ == "__main__":
    print("No ghosts want to approach Chuck Norris because they're afraid of dying a second time")


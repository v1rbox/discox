from discord import Colour
from discord.embeds import Embed as DiscordEmbed
from dotenv import load_dotenv

load_dotenv()

import datetime
import os
from typing import List


# os.getenv returns an empty string if the value is empty so it doesn't use the second argument
def getenv(name: str, other: str = None) -> any:
    """Gets an environment variable
    [Args]:
        name (str): The name of the env variable
        other (str): Will return if name is empty or None
    """
    env = os.getenv(name)
    return env if env or other is None else other


class Embed(DiscordEmbed):
    """Custom implementation of a discord embed object."""

    def __init__(self, *args, **kwargs) -> None:
        DiscordEmbed.__init__(self, *args, **kwargs)

        self.colors = {
            "green": Colour(int("38842c", 16)),
            "red": Colour(int("bf3036", 16)),
            "blue": Colour(int("303f9c", 16)),
            "yellow": Colour(int("b0ba2a", 16)),
            "magenta": Colour(int("a829b0", 16)),
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
            icon_url="https://cdn.discordapp.com/icons/1052597660860821604/8fd53af279aa7d8d77a0451776c4fa35.webp?size=96",
        )
        self.timestamp = datetime.datetime.now()

        self.set_color("green")

    def set_color(self, color: str) -> None:
        """Set a color from the default colorlist."""
        self.color = self.colors[color]


class Config:
    testing: dict = {
        "ignore_db": getenv("TESTING_IGNORE_DB", "False") == "True",
        "ignored_files": getenv("TESTING_IGNORED_FILES", "").split(
            ", "
        ),  # list of files that won't be imported
    }
    token: str = getenv("DISCOX_TOKEN")  # bot token
    prefix: str = getenv("DISCOX_PREFIX", "v!")  # prefix (default: v!)
    general_channel: int = int(getenv("DISCOX_GENERAL_ID", 1052597661578051666))
    report_channel_id: int = int(
        getenv("DISCOX_REPORT_ID", 1064539181193375784)
    )  # mod role id

    mod_role_id: List[int] = [
        int(x) for x in getenv("DISCOX_MOD_ROLE_ID", "0").split(",")
    ]  # mod role id
    temp_channel: int = int(getenv("DISCOX_TEMP_CHANNEL", "0"))  # temp channel id
    channel_id: str = getenv(
        "DISCOX_CHANNEL_ID", "UCCFVFyadjMuaR5O89yRToew"
    )  # channel id
    role_channel: int = int(getenv("DISCOX_ROLE_CHANNEL", "0"))  # role channel
    youtube_announcement_id: int = int(
        getenv("DISCOX_YOUTUBE_ANNOUNCEMENT_ID", 1056990617357521009)
    )  # youtube announcement id
    mysql_host: str = getenv("DISCOX_MYSQL_HOST", "localhost")
    mysql_port: int = int(getenv("DISCOX_MYSQL_PORT", 3306))
    mysql_user: str = getenv("DISCOX_MYSQL_USER", "root")
    mysql_password: str = getenv("DISCOX_MYSQL_PASSWORD", "")  # recommendaton :tf:
    mysql_database: str = getenv(
        "DISCOX_MYSQL_DATABASE", "discox"
    )  # HOW THE FUCK ITS DEFAULTING TO DISCOX ALL THE TIME
    starboard_channel: int = int(
        getenv("DISCOX_STARBOARD_CHANNEL", "0")
    )  # starboard channel
    welcome_channel: int = int(
        getenv("SERVER_WELCOME_CHANNEL", "1056171331059732541")
    )  # welcome channel
    minecraft_url: str = getenv("MINECRAFT_URL", "minecraft.virbos.xyz")
    minecraft_port: int = getenv("MINECRAFT_PORT", 25565)


if __name__ == "__main__":
    print(
        "No ghosts want to approach Chuck Norris because they're afraid of dying a second time"
    )

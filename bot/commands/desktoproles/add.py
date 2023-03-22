from discord import Color

from bot.base import Command, Roles
from bot.config import Config, Embed


class DesktopRoles(Roles):
    max = 3
    role_color = Color.from_rgb(185, 137, 240)
    prefix = "desktop"
    whitelist = [
        "GNOME",
        "KDE",
        "LXQT",
        "XFCE",
        "MATE",
        "Cinamon",
        "Enlightenment",
        "Deepin",
        "LXDE",
        "CDE",
        "TDE",
        "Pantheon",
        "Lumina",
        "ROX",
        "UKUI",
        "Sugar",
        "UDE",
        "Awesome",
        "Xmonad",
        "Hyprland",
        "Dwm",
        "Qtile",
        "Wayfire",
        "Sway",
        "bspwm",
        "FrankenWM",
        "herbstluftwm",
        "i3",
        "LeftWM",
        "Notion",
        "Ratpoison",
        "Snapwm",
        "Spectrwm",
        "Stumpwm",
        "dwl",
        "Cagebreak",
        "Cardboard",
        "japokwm",
        "newm",
        "river",
        "Velox",
        "Vivarium",
        "waymonad",
        "Openbox",
        "QTile",
        "EXWM",
    ]


class cmd(Command):
    """A discord command instance."""

    name = "add"
    usage = "add <distribution>"
    description = f"Assigns user a role based on selected desktop, max of {DesktopRoles.max} desktop roles per user."

    async def execute(self, arguments, message) -> None:
        desktoproles = DesktopRoles()
        embed = Embed(
            title="Desktop",
            description=await desktoproles.addRole(message, arguments[0]),
        )
        await message.channel.send(embed=embed)

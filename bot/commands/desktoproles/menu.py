from discord import Color

from bot.base import Command, RoleView
from bot.config import Config, Embed


class DesktopRoles(RoleView):
    max = 3
    role_color = Color.from_rgb(219, 240, 137)
    prefix = "desktop"
    whitelist = [
        "GNOME",
        "KDE",
        "LXQT",
        "XFCE",
        "MATE",
        "Cinnamon",
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

    name = "menu"
    usage = "menu"
    description = f"Desktop Roles Menu"

    async def execute(self, arguments, message) -> None:
        desktop = DesktopRoles(message)
        await message.channel.send(embed=desktop.default_embed,view=desktop)

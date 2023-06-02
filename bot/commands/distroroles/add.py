from discord import Color

from bot.base import Command, Roles
from bot.config import Config, Embed


class DistroRoles(Roles):
    max = 3
    role_color = Color.from_rgb(185, 137, 240)
    prefix = "distro"
    whitelist = [
        "/e/OS",
        "Alma",
        "Alpine",
        "Android",
        "AthenaOS",
        "Arch",
        "Archcraft",
        "Arco",
        "Artix",
        "Bedrock",
        "BlackArch",
        "BlendOS",
        "CachyOS",
        "CalyxOS",
        "CentOS",
        "Debian",
        "Devuan",
        "Deepin",
        "Elementary",
        "EndeavourOS",
        "Fedora",
        "FreeBSD",
        "Funtoo",
        "Garuda",
        "Gentoo",
        "GhostBSD",
        "Gnoppix",
        "GNUGuix",
        "GrapheneOS",
        "Haiku",
        "HarmonyOS",
        "iOS",
        "KaiOS",
        "Kali",
        "KISS Linux",
        "Kubuntu",
        "LineageOS",
        "LMDE",
        "Lubuntu",
        "MacOS",
        "Mageia",
        "Manjaro",
        "Mint",
        "MIUI",
        "Mobian",
        "MX",
        "NetBSD",
        "NixOS",
        "Nobara",
        "OpenBSD",
        "OpenMediaVault",
        "OpenSUSE",
        "Oracle",
        "Parrot",
        "Plasma Mobile",
        "Pop!_OS",
        "ReactOS",
        "RebornOS",
        "Redcore",
        "RedHat",
        "Rocky",
        "Sailfish OS",
        "Salix",
        "Slackware",
        "Solaris",
        "SUSE",
        "Tails",
        "TempleOS",
        "TrueNAS",
        "Ubuntu",
        "Ubuntu Touch",
        "Ultramarine",
        "UwUntu",
        "VanillaOS",
        "VirbOS",
        "Void",
        "WattOS",
        "Whonix",
        "Windows",
        "Zorin",
    ]


class cmd(Command):
    """A discord command instance."""

    name = "add"
    usage = "add <distribution>"
    description = f"Assigns user a role based on selected distro, max of {DistroRoles.max} distro roles per user."

    async def execute(self, arguments, message) -> None:
        distroroles = DistroRoles()
        embed = Embed(
            title="Distro", description=await distroroles.addRole(message, arguments[0])
        )
        await message.channel.send(embed=embed)

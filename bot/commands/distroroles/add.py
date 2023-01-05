from bot.config import Config, Embed
from bot.base import Command
from discord import Color


class cmd(Command):
    """ A discord command instance. """

    ### Allowed distros and max allowed distro roles per user ###
    distro_roles_color = Color.from_rgb(185, 137, 240)
    max_distro = 3
    whitelist = [
        'Alma',
        'Alpine',
        'Android',
        'Arch',
        'Arco',
        'Artix',
        'Bedrock',
        'CentOS',
        'Debian',
        'Elementary',
        'EndeavourOS',
        'Fedora',
        'FreeBSD',
        'Funtoo',
        'Garuda',
        'Gentoo',
        'GNUGuix',
        'Haiku',
        'iOS',
        'Kali',
        'Kubuntu',
        'Lubuntu',
        'MacOS',
        'Manjaro',
        'Mint',
        'MX',
        'NetBSD',
        'NixOS',
        'Nobara',
        'OpenBSD',
        'OpenMediaVault',
        'OpenSUSE',
        'Oracle',
        'Parrot',
        'Pop!OS',
        'ReactOS',
        'RedHat',
        'Rocky',
        'Slackware',
        'Solaris',
        'SUSE',
        'Tails',
        'TempleOS',
        'TrueNAS',
        'Ubuntu',
        'Ultramarine',
        'Void',
        'Whonix',
        'Windows',
        'Zorin',
    ]

    name = "add"
    usage = "add <distibution>"
    description = f"Assigns user a role based on selected distro, max of {max_distro} distro roles per user."

    ### Gets Role Object with from a given name ###
    def getRole(self, message, role_name):
        for role in message.guild.roles:
            if role.name == role_name:
                return role

    async def execute(self, arguments, message) -> None:
        user_roles_names = []
        server_roles_names = []
        name = message.author.name

        for role in message.author.roles:
            user_roles_names.append(role.name)
        for role in message.guild.roles:
            server_roles_names.append(role.name)

        # Checks if role exists ignoring capitalization
        if arguments[0] in (i.lower() for i in self.whitelist if (guess := i).lower() == arguments[0]):
            embed = Embed(title="Distro", description=f"**Invalid distro**\nDid you mean to type ``{guess}`` ? \n\n*To see valid distros, use:*\n`v!distro whitelist`")
            embed.set_color("red")
            await message.channel.send(embed=embed)
            return
        # Checks if role is whitelisted
        if arguments[0] not in self.whitelist:
            embed = Embed(title="Distro", description="**Invalid distro**\n\n*To see valid distros, use:*\n`v!distro whitelist`")
            embed.set_color("red")
            await message.channel.send(embed=embed)
            return
        # Checks if user already has the role
        if arguments[0] in user_roles_names:
            embed = Embed(title="Distro", description=f"**`{name}` already has that distro role**")
            embed.set_color("red")
            await message.channel.send(embed=embed)
            return
        # Checks if user has maximum distro roles
        max = 0
        for role in user_roles_names:
            if role in self.whitelist:
                max += 1
        if max >= self.max_distro:
            embed = Embed(title="Distro", description=f"**`{name}` has reached the max distro roles.**\n\n*To see your current distro roles, use:*\n`v!distro roles` \n\n*To remove a distro role, use:*\n`v!distro remove [Your distro]`")
            embed.set_color("red")
            await message.channel.send(embed=embed)
            return
        # Checks if role exists, if not, creates role
        if arguments[0] not in server_roles_names:
            await message.guild.create_role(name=arguments[0], mentionable=True, colour=self.distro_roles_color)
        # Adds user to role
        role = self.getRole(message, arguments[0])
        await message.author.add_roles(role)
        embed = Embed(title="Distro", description=f"**`{name}` has been added to the `{role.name}` distro role**")
        await message.channel.send(embed=embed)
        


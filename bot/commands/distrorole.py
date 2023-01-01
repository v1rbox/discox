from bot.config import Config, Embed
from bot.base import Command
from discord import Color


class cmd(Command):
    """ A discord command instance. """
    #
    ##
    ### Allowed distros and max allowed distro roles per user ###
    ##
    #
    distro_roles_color = Color.from_rgb(185, 137, 240)
    max_distro = 3
    whitelist = [
        'Alma',
        'Alpine',
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
    ]

    name = "distro"
    usage = "distro <command> [distro] \n\ncommands: add, remove, whitelist, roles, leaderboard, help"
    description = f"Assigns user a role based on selected distro, max of {max_distro} distro roles per user.\n"

    #
    ##
    ### Gets Role Object with from a given name ###
    ##
    #
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

        #
        ##
        ### "help" ARG: Replies with available commands and format ###
        ##
        #
        if len(arguments) == 1 and arguments[0] == 'help':
            embed = Embed(
                title="Distro", description="**Help:** \n\n*Add a distro role:*\n`v!distro add [Your distro]`\n\n*Remove a distro role:*\n`v!distro remove [Your distro]`\n\n*See available distro roles:*\n`v!distro whitelist`\n\n*Check your current distro roles:*\n`v!distro roles`\n\n*Check the distro leaderboard:*\n`v!distro leaderboard`")
            await message.channel.send(embed=embed)

        #
        ##
        ### "whitelist" ARG: Replies with available options for distro role ###
        ##
        #
        elif len(arguments) == 1 and arguments[0] == "whitelist":
            description = "**Available distro roles:**\n\n"
            for i in self.whitelist:
                description += f'`{i}`\n'
            embed = Embed(title="Distro", description=description)
            await message.channel.send(embed=embed)

        #
        ##
        ### "roles" ARG: Replies with users current distro roles ###
        ##
        #
        elif len(arguments) == 1 and arguments[0] == "roles":
            roles = []
            description = f"**`{name}`'s current distro roles:**\n\n"
            # Searches for users current distro roles
            for role in user_roles_names:
                if role in self.whitelist:
                    roles.append(role)
            # Checks if user has no distro roles
            if len(roles) == 0:
                embed = Embed(title="Distro",
                              description=f"**`{name}` has no distro roles**")
                await message.channel.send(embed=embed)
                return
            # Replies with current distro roles
            for role in roles:
                description += f'`{role}`\n\n'
            embed = Embed(title="Distro", description=description)
            await message.channel.send(embed=embed)

        #
        ##
        ### "leaderboard" ARG: Replies with each distros member count #
        ##
        #
        elif len(arguments) == 1 and arguments[0] == "leaderboard":
            leaderboard = []
            description = "**Leaderboard:**\n\n"
            # Checks current distro roles in server
            for role in server_roles_names:
                if role in self.whitelist:
                    leaderboard.append({"role": role, "count": len(
                        self.getRole(message, role).members)})
            # Returns if there are no distro roles
            if leaderboard == []:
                embed = Embed(title="Distro",
                              description="**No distro roles yet**")
                await message.channel.send(embed=embed)
                return
            # Sorts by highest member count
            leaderboard = sorted(
                leaderboard, key=lambda d: d['count'], reverse=True)
            # Returns distro role leaderboard
            for role in leaderboard:
                description += f"**Current `{role['role']}` Users: `{role['count']}`**\n\n"
            embed = Embed(title="Distro", description=description)
            await message.channel.send(embed=embed)

        #
        ##
        ### "justin" ARG: Totally factual information #
        ##
        #
        elif len(arguments) == 1 and arguments[0] == "justin":
            embed = Embed(
                title="Distro", description="**<@298308374590652416> is leet linux chad** \n\n ***Fedora > Any other distro***")
            await message.channel.send(embed=embed)

        #
        ##
        ### "add" ARG: adds user to role ###
        ##
        #
        elif len(arguments) == 2 and arguments[0] == "add":
            # Checks if role is whitelisted
            if arguments[1] not in self.whitelist:
                embed = Embed(
                    title="Distro", description="**Invalid distro**\n\n*To see valid distros, use:*\n`v!distro whitelist`")
                await message.channel.send(embed=embed)
                return
            # Checks if user already has the role
            if arguments[1] in user_roles_names:
                embed = Embed(
                    title="Distro", description=f"**`{name}` already has that distro role**")
                await message.channel.send(embed=embed)
                return
            # Checks if user has maximum distro roles
            max = 0
            for role in user_roles_names:
                if role in self.whitelist:
                    max += 1
            if max >= self.max_distro:
                embed = Embed(
                    title="Distro", description=f"**`{name}` has reached the max distro roles.**\n\n*To see your current distro roles, use:*\n`v!distro roles` \n\n*To remove a distro role, use:*\n`v!distro remove [Your distro]`")
                await message.channel.send(embed=embed)
                return
            # Checks if role exists, if not, creates role
            if arguments[1] not in server_roles_names:
                await message.guild.create_role(name=arguments[1], mentionable=True, colour=self.distro_roles_color)
            # Adds user to role
            role = self.getRole(message, arguments[1])
            await message.author.add_roles(role)
            embed = Embed(
                title="Distro", description=f"**`{name}` has been added to the `{role.name}` distro role**")
            await message.channel.send(embed=embed)

        #
        ##
        ### "remove" ARG: removes user from role ###
        ##
        #
        elif len(arguments) == 2 and arguments[0] == "remove":
            # Checks if user has role and role is whitelisted
            if arguments[1] not in self.whitelist or arguments[1] not in user_roles_names:
                embed = Embed(
                    title="Distro", description=f"**`{name}` does not have that distro role, or `{arguments[1]}` is not whitelisted**\n\n*To your see current distro roles, use:* \n`v!distro roles`\n\n*To see whitelisted distro roles, use:*\n`v!distro whitelist`")
                await message.channel.send(embed=embed)
                return
            # Removes role from user
            role = self.getRole(message, arguments[1])
            await message.author.remove_roles(role)
            embed = Embed(
                title="Distro", description=f"**`{name}` has been removed from the `{role.name}` distro role.**")
            await message.channel.send(embed=embed)

        #
        ##
        ### Recurses to help ARG Response for invalid syntax###
        ##
        #
        else:
            arguments = ['help']
            await self.execute(arguments, message)

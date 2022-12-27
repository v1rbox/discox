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
    distro_roles_color=Color.from_rgb(204, 255, 204)
    max_distro = 3
    whitelist = [
      'Alma',
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
    usage = "distro add <Your Unix-Like/Windows Distribution>\n\nv!distro remove <Your Unix-Like/Windows Distribution>\n\nv!distro whitelist\n\nv!distro roles"
    description = f"Assigns user a cosmetic only role based on selected whitelisted distro, max of {max_distro} distro roles per user."

    #
    ##
    ### Gets Role Object with from a given name ###
    ##
    #
    def getRole(self,message,role_name):
      for role in message.guild.roles:
        if role.name == role_name:
          return role

    async def execute(self, arguments, message) -> None:
        user_roles_names = []
        server_roles_names =[]

        for role in message.author.roles:
          user_roles_names.append(role.name)  
        for role in message.guild.roles:
          server_roles_names.append(role.name)

        # 
        ##
        ### No ARG Response ###
        ##
        #
        if len(arguments) == 0:
          embed = Embed(title="Distro", description="Usage: \n\n`v!distro add <Your Unix-Like/Windows Distribution>`\n\n`v!distro remove <Your Unix-Like/Windows Distribution>`\n\n`v!distro whitelist\n\nv!distro roles`")
          await message.channel.send(embed=embed)

        else:

          #
          ##
          ### "whitelist" ARG: Replies with available options for distro role ###
          ##
          #
          if arguments[0] == "whitelist":
            description = ""
            for i in self.whitelist:
              description += f'{i}\n'
            embed = Embed(title="Distro", description=description)
            await message.channel.send(embed=embed)

          #
          ##
          ### "roles" ARG: Replies with users current distro roles ###
          ##
          #
          elif arguments[0] == "roles":
            roles = []
            description = ""
            # Searches for users current distro roles
            for role in user_roles_names:
              if role in self.whitelist:
                roles.append(role)
            # Checks if user has no distro roles
            if len(roles) == 0:
              embed = Embed(title="Distro", description="You have no distro roles")
              await message.channel.send(embed=embed)
              return
            # Replies with current distro roles  
            for role in roles:
              description += f'{role}\n\n'
            embed = Embed(title="Distro", description=description)
            await message.channel.send(embed=embed)

          #
          ##
          ### "add" ARG: adds user to role ###
          ##
          #
          elif arguments[0] == "add":
            # Checks if role is whitelisted
            if arguments[1] not in self.whitelist:
              embed = Embed(title="Distro", description="Invalid distro.\n\nTo see valid distros, use:\n\n `v!distro whitelist`")
              await message.channel.send(embed=embed)
              return
            # Checks if user already has the role
            if arguments[1] in user_roles_names:
              embed = Embed(title="Distro", description="You already have that distro role.")
              await message.channel.send(embed=embed)
              return
            # Checks if user has maximum distro roles
            max = 0
            for role in user_roles_names:
              if role in self.whitelist:
                max += 1
            if max >= self.max_distro:
              embed = Embed(title="Distro", description="You have reached the max distro roles.\n\nTo see your current distro roles, use: \n\n`v!distro roles` \n\nTo remove a distro role, use:\n\n`v!distro remove <Your Unix-Like/Windows Distribution>`")
              await message.channel.send(embed=embed)
              return
            # Checks if role exists, if not, creates role
            if arguments[1] not in server_roles_names:
              await message.guild.create_role(name=arguments[1],mentionable=True,colour=self.distro_roles_color)
            # Adds user to role
            role = self.getRole(message, arguments[1])
            await message.author.add_roles(role)
            embed = Embed(title="Distro", description=f"You have been added to the {role.name} distro role.")
            await message.channel.send(embed=embed)

          #
          ##
          ### "remove" ARG: removes user from role ###
          ##
          #
          elif arguments[0] == "remove":
            # Checks if user has role and role is whitelisted
            if arguments[1] not in self.whitelist or arguments[1] not in user_roles_names:
              embed = Embed(title="Distro", description=f"You do not have that distro role, or distro is not whitelisted.\n\nTo your see current distro roles, use: \n\n`v!distro roles`\n\nTo see whitelisted distro roles, use:\n\n`v!distro whitelist`")
              await message.channel.send(embed=embed)
              return
            # Removes role from user
            role = self.getRole(message, arguments[1])
            await message.author.remove_roles(role)
            embed = Embed(title="Distro", description=f"You have been removed from the {role.name} distro role.")
            await message.channel.send(embed=embed)
          
          #
          ##
          ### Recurses to No ARG Response for invalid syntax###
          ##
          #
          else:
            arguments=[]
            await self.execute(arguments, message)
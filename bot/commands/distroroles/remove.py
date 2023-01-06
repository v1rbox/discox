from bot.config import Config, Embed
from bot.base import Command
from bot.commands.distroroles.add import cmd as Distro

class cmd(Command):
    """ A discord command instance. """
  
    name = "remove"
    usage = "remove <distibution>"
    description = f"Removes a distro role from user"

    async def execute(self, arguments, message) -> None:
        user_roles_names = []
        name = message.author.name

        for role in message.author.roles:
            user_roles_names.append(role.name)
            
        # Checks if user has role and role is whitelisted
        if arguments[0].lower() not in map(lambda distro: distro.lower(), Distro.whitelist) or arguments[0].lower() not in map(lambda role: role.lower(), user_roles_names):
            embed = Embed(title="Distro", description=f"**`{name}` does not have that distro role, or `{arguments[0]}` is not whitelisted**\n\n*To your see current distro roles, use:* \n`v!distro roles`\n\n*To see whitelisted distro roles, use:*\n`v!distro whitelist`")
            embed.set_color("red")
            await message.channel.send(embed=embed)
            return

        role_name = Distro.whitelist[
                list(map(lambda distro: distro.lower(), Distro.whitelist)).index(arguments[0].lower())
        ]
        # Removes role from user
        role = Distro.getRole(self,message, role_name)
        await message.author.remove_roles(role)
        # Removes role from server if role is empty
        if len(role.members) == 0:
            await role.delete()
        embed = Embed(
            title="Distro", description=f"**`{name}` has been removed from the `{role.name}` distro role.**")
        await message.channel.send(embed=embed)

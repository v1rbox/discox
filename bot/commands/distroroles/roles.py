from bot.config import Config, Embed
from bot.base import Command
from bot.commands.distroroles.add import cmd as Distro

class cmd(Command):
    """ A discord command instance. """
  
    name = "roles"
    usage = "distro roles"
    description = f"Shows user's current distro roles"

    async def execute(self, arguments, message) -> None:
        user_roles_names = []
        name = message.author.name

        for role in message.author.roles:
            user_roles_names.append(role.name)

        roles = []
        description = f"**`{name}`'s current distro roles:**\n\n"
        # Searches for users current distro roles
        for role in user_roles_names:
            if role in Distro.whitelist:
                roles.append(role)
        # Checks if user has no distro roles
        if len(roles) == 0:
            embed = Embed(title="Distro",description=f"**`{name}` has no distro roles**")
            embed.set_color("red")
            await message.channel.send(embed=embed)
            return
        # Replies with current distro roles
        for role in roles:
            description += f'`{role}`\n\n'
        embed = Embed(title="Distro", description=description)
        await message.channel.send(embed=embed)

        
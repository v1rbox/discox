from bot.base import Command
from bot.commands.coderoles.add import cmd as Code
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "roles"
    usage = "roles"
    description = f"Shows user's current code roles"

    async def execute(self, arguments, message) -> None:
        user_roles_names = []
        name = message.author.name

        for role in message.author.roles:
            user_roles_names.append(role.name)

        roles = []
        description = f"**`{name}`'s current code roles:**\n\n"
        # Searches for users current code roles
        for role in user_roles_names:
            if role in Code.whitelist:
                roles.append(role)
        # Checks if user has no code roles
        if len(roles) == 0:
            embed = Embed(title="Code", description=f"**`{name}` has no code roles**")
            embed.set_color("red")
            await message.channel.send(embed=embed)
            return
        # Replies with current code roles
        for role in roles:
            description += f"`{role}`\n\n"
        embed = Embed(title="Code", description=description)
        await message.channel.send(embed=embed)

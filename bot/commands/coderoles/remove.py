from bot.base import Command
from bot.commands.coderoles.add import cmd as Code
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "remove"
    usage = "remove <language>"
    description = f"Removes a code role from user"

    async def execute(self, arguments, message) -> None:
        user_roles_names = []
        name = message.author.name

        for role in message.author.roles:
            user_roles_names.append(role.name)

        # Checks if user has role and role is whitelisted
        if arguments[0].lower() not in map(
            lambda lang: lang.lower(), Code.whitelist
        ) or arguments[0].lower() not in map(
            lambda role: role.lower(), user_roles_names
        ):
            embed = Embed(
                title="Code",
                description=f"**`{name}` does not have that code role, or `{arguments[0]}` is not whitelisted**\n\n*To your see current code roles, use:* \n`v!code roles`\n\n*To see whitelisted languages, use:*\n`v!code whitelist`",
            )
            embed.set_color("red")
            await message.channel.send(embed=embed)
            return

        role_name = Code.whitelist[
            list(map(lambda lang: lang.lower(), Code.whitelist)).index(
                arguments[0].lower()
            )
        ]
        # Removes role from user
        role = Code.getRole(self, message, role_name)
        await message.author.remove_roles(role)
        # Removes role from server if role is empty
        if len(role.members) == 0:
            await role.delete()
        embed = Embed(
            title="Code",
            description=f"**`{name}` has been removed from the `{role.name}` code role.**",
        )
        await message.channel.send(embed=embed)

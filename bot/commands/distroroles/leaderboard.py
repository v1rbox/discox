from bot.base import Command
from bot.commands.distroroles.add import cmd as Distro
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "leaderboard"
    usage = "leaderboard"
    description = f"Leaderboard of most used distros in the server"

    async def execute(self, arguments, message) -> None:
        server_roles_names = []

        for role in message.guild.roles:
            server_roles_names.append(role.name)

        leaderboard = []
        description = "**Leaderboard:**\n\n"
        # Checks current distro roles in server
        for role in server_roles_names:
            if (
                role in Distro.whitelist
                and len(Distro.getRole(self, message, role).members) > 0
            ):
                leaderboard.append(
                    {
                        "role": role,
                        "count": len(Distro.getRole(self, message, role).members),
                    }
                )
        # Returns if there are no distro roles
        if leaderboard == []:
            embed = Embed(title="Distro", description="**No distro roles yet**")
            embed.set_color("red")
            await message.channel.send(embed=embed)
            return
        # Sorts by highest member count
        leaderboard = sorted(leaderboard, key=lambda d: d["count"], reverse=True)
        # Returns distro role leaderboard
        for role in leaderboard:
            description += f"**Current `{role['role']}` Users: `{role['count']}`**\n\n"
        embed = Embed(title="Distro", description=description)
        await message.channel.send(embed=embed)

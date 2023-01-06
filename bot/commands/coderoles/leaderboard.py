from bot.config import Config, Embed
from bot.base import Command
from bot.commands.coderoles.add import cmd as Code

class cmd(Command):
    """ A discord command instance. """

    name = "leaderboard"
    usage = "leaderboard"
    description = f"Leaderboard of most used languages in the server"

    async def execute(self, arguments, message) -> None:
        server_roles_names = []

        for role in message.guild.roles:
            server_roles_names.append(role.name)

        leaderboard = []
        description = "**Leaderboard:**\n\n"
        # Checks current code roles in server
        for role in server_roles_names:
            if role in Code.whitelist and len(Code.getRole(self, message, role).members) > 0:
                leaderboard.append({"role": role, "count": len(Code.getRole(self,message,role).members)})
        # Returns if there are no code roles
        if leaderboard == []:
            embed = Embed(title="Code",description="**No code roles yet**")
            embed.set_color("red")
            await message.channel.send(embed=embed)
            return
        # Sorts by highest member count
        leaderboard = sorted(leaderboard, key=lambda d: d['count'], reverse=True)
        # Returns code role leaderboard
        for role in leaderboard:
            description += f"**Current `{role['role']}` Users: `{role['count']}`**\n\n"
        embed = Embed(title="Code", description=description)
        await message.channel.send(embed=embed)
        

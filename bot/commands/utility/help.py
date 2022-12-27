from bot.config import Config, Embed
from bot.base import Command

class cmd(Command):
    """ Help command. """

    name = "help"
    usage = "help <command>"
    description = "The command you just ran, shows a help embed."

    async def execute(self, arguments, message) -> None:
        if len(arguments) == 0:
            embed = Embed(
                title=f"Help menu - {len(self.manager.commands)} commands",
                description=f"List of all commands and their description\nRun `{Config.prefix}{self.usage}` to get information about a specific command.",
            )

            for command in self.manager.commands:
                embed.add_field(
                    name=f"{Config.prefix}{command.name}",
                    value=f"{command.description}",
                    inline=False
                )

            await message.channel.send(embed=embed)
        else:
            try:
                cmd = self.manager.get(arguments[0])
            except KeyError:
                raise KeyError(f"Command {arguments[0]} not found.")
            
            embed = Embed(
                title=cmd.name.capitalize(),
                description=f"{cmd.description}\nUsage: `{Config.prefix}{cmd.usage}`",
            )

            await message.channel.send(embed=embed)

from mcstatus import JavaServer

from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):
    name = "status"
    usage = "status"
    description = "Get the status of the minecraft server"

    async def execute(self, arguments, message) -> None:
        server = JavaServer.lookup(f"{Config.minecraft_url}:{Config.minecraft_port}")
# 'query' has to be enabled in a server's server.properties file!
# It may give more information than a ping, such as a full player list or mod information.
        query = server.query()

        plugins = ' \n'.join(query.software.plugins)
        embed = Embed(
            title="Minecraft",
            description=f"""
**URL:** ```{Config.minecraft_url}:{Config.minecraft_port}```
**VERSION:** ```{query.software.version}({query.software.brand})```
**PLAYERS:** ```{query.players.online} online```
**PLUGINS:** ```{plugins}```
""",
        )
        embed.set_color("green")
        await message.channel.send(embed=embed)

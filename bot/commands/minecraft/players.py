from mcstatus import JavaServer

from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):
    name = "players"
    usage = "players"
    description = "Get the players of the minecraft server"

    async def execute(self, arguments, message) -> None:
        server = JavaServer.lookup(f"{Config.minecraft_url}:{Config.minecraft_port}")
# 'query' has to be enabled in a server's server.properties file!
# It may give more information than a ping, such as a full player list or mod information.
        query = server.query()

        players = ' \n'.join(query.players.names)
        embed = Embed(
            title="Minecraft",
            description=f"""
**CURRENTLY ONLINE ({query.players.online}/{query.players.max}):** ```{players}```
""",
        )
        embed.set_color("green")
        await message.channel.send(embed=embed)

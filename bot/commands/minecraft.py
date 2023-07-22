from bot.base import Command
from bot.config import Embed, Config
from mcstatus import JavaServer


class cmd(Command):
    name = "minecraft"
    usage = "minecraft"
    description = "Get the status of the minecraft server"

    async def execute(self, arguments, message) -> None:

        server = JavaServer.lookup(f"{Config.minecraft_url}:{Config.minecraft_port}")
        status = server.status()
        if Config.minecraft_port == "25565":
            url = Config.minecraft_url
        else:
            url = f"{Config.minecraft_url}:{Config.minecraft_port}"
        embed = Embed(
            title="Minecraft",
            description=f"""
            **URL:** ```{url}```
            **VERSION:** ```{status.version.name}```
            **MOTD:** ```{status.motd.to_plain()}```
            **CURRENT PLAYERS:** ```{status.players.online}```
            """ 
        )
        embed.set_color("green")
        await message.channel.send(embed=embed)

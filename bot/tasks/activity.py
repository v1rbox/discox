import discord
from discord.ext.tasks import loop
from bot.base import Task
from bot.config import Config
from mcstatus import JavaServer


class TaskLoop(Task):
    @loop(minutes=10)
    async def execute(self) -> None:
        server = JavaServer.lookup(f"{Config.minecraft_url}:{Config.minecraft_port}")
        status = server.status()
        if status.players.online > 6:
            activity = discord.Activity(
                type=discord.ActivityType.playing, name=f"Minecraft {status.players.online} Online"
            )
        else:
            activity = discord.Activity(
                type=discord.ActivityType.watching, name=f"Virbox videos"
            )
        await self.bot.change_presence(activity=activity)

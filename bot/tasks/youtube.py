import re

import aiohttp
from discord.ext import tasks

from bot.base import Task
from bot.config import Config, Embed


class TaskLoop(Task):
    """A discord Task instance."""

    @tasks.loop(minutes=2)
    async def execute(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://www.youtube.com/feeds/videos.xml?channel_id={Config.channel_id}"
            ) as resp:
                if resp.status == 404:
                    self.logger.error("Invalid youtube id")
                    return

                text = await resp.text()
                video_id = re.findall(r"<yt:videoId>([A-Za-z0-9-_]+)</yt:videoId>", text)[0]
                list_id = await self.db.raw_exec_select("SELECT video_id FROM latest_video")
                if len(list_id) == 0:
                    await self.db.raw_exec_commit(
                        "INSERT INTO latest_video(video_id) VALUES(?)", (video_id,)
                    )
                list_id = await self.db.raw_exec_select("SELECT video_id FROM latest_video")

                last_id = list_id[0]
                
                if video_id != (last_id := last_id[0]):
                    print("NEW VIDEO!")

                    channel = self.bot.get_channel(Config.youtube_announcement_id)

                    await channel.send(
                        f"New video! :0\nhttps://youtu.be/{video_id}"
                    )
                    print("sent")
                    await self.db.raw_exec_commit(
                        "UPDATE latest_video SET video_id = ?", (video_id,)
                    )

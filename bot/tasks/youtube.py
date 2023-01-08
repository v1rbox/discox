from bot.config import Config, Embed
from bot.base import Task

from discord.ext import tasks

import requests
import re


class TaskLoop(Task):
    """ A discord Task instance. """

    @tasks.loop(minutes=2.5)
    async def execute(self):
        response = requests.get(f"https://www.youtube.com/feeds/videos.xml?channel_id={Config.channel_id}")
        text = response.text

        video_id = re.findall(r"<yt:videoId>([A-Za-z0-9-_]+)</yt:videoId>", text)[0]

        cursor = await self.db.cursor()

        await cursor.execute("SELECT video_id FROM latest_video")
        last_id = await cursor.fetchone()

        if video_id != (last_id := last_id[0]):
            response = requests.post(
                    f"https://discord.com/api/channels/{Config.youtube_announcement_id}/messages", 
                    headers={"Authorization": f"Bot {Config.token}", "content-type": "application/json"},
                    json={"content": f"New video :0\nhttps://www.youtube.com/watch?v={video_id}"}
                )

            await cursor.execute("UPDATE latest_video SET video_id = ?", (video_id, ))
            await self.db.commit()

        await cursor.close()

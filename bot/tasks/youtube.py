import re

import requests
from discord.ext import tasks

from bot.base import Task
from bot.config import Config, Embed


class TaskLoop(Task):
    """A discord Task instance."""

    @tasks.loop(minutes=2.5)
    async def execute(self):
        response = requests.get(
            f"https://www.youtube.com/feeds/videos.xml?channel_id={Config.channel_id}"
        )

        if response.status_code == 404:
            self.logger.error("Invalid youtube id")
            return

        text = response.text

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
            response = requests.post(
                f"https://discord.com/api/channels/{Config.youtube_announcement_id}/messages",
                headers={
                    "Authorization": f"Bot {Config.token}",
                    "content-type": "application/json",
                },
                json={
                    "content": f"New video :0\nhttps://www.youtube.com/watch?v={video_id}"
                },
            )

            await self.db.raw_exec_commit(
                "UPDATE latest_video SET video_id = ?", (video_id,)
            )

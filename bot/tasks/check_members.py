from bot.base import Task
from discord.ext.tasks import loop

class TaskLoop(Task):
    
    previous_member_count = None # best way to not fetching db every minutes
    
    @loop(minutes=1)
    async def execute(self) -> None:
        if self.previous_member_count is None:
            self.previous_member_count = len([x for x in self.bot.get_all_members() if not x.bot])
        elif self.previous_member_count >= len([x for x in self.bot.get_all_members() if not x.bot]): # if member count changed
            return
        await self.bot.wait_until_ready()
        registered = [int(x[0]) for x in (await self.db.raw_exec_select("SELECT user_id FROM levels"))]
        for member in [x for x in self.bot.get_all_members() if not x.bot]:
            if member.id in registered:
                continue
            await self.db.raw_exec_commit("INSERT INTO levels VALUES (?, ?, ?, ?, ?)", (member.id, 0, 0, "255 255 255", None))
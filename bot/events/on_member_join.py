from bot.base import Event


class event(Event):
    name = "on_member_join"

    async def execute(self) -> None:
        await self.bot.wait_until_ready()
        registered = [
            int(x[0])
            for x in (await self.db.raw_exec_select("SELECT user_id FROM levels"))
        ]
        for member in [x for x in self.bot.get_all_members() if not x.bot]:
            if member.id in registered:
                continue
            await self.db.raw_exec_commit(
                "INSERT INTO levels VALUES (?, ?, ?, ?, ?)",
                (member.id, 0, 0, "255 255 255", None),
            )

from bot.base import Command
from bot.config import Config, Embed

from .utils.__level_generator import generate_profile

class cmd(Command):
    """A discord command instance."""

    name = "rank"
    usage = "rank [*user]"
    description = "Check the rank for another user, by default this is the author."

    async def get_bg(self, user: int) -> str | None:
        cursor = await self.db.cursor()
        await cursor.execute(f"SELECT bg FROM levels WHERE user_id = '{user}'")
        result = await cursor.fetchone()
        await cursor.close()
        try:
            return result[0]
        except (IndexError, TypeError):
            return None
    
    async def get_font_color(self, user: int) -> tuple[int, int, int] | tuple[255, 255 ,255]:
        cursor = await self.db.cursor()
        await cursor.execute(f"SELECT font_color FROM levels WHERE user_id = '{user}'")
        result = await cursor.fetchone()
        await cursor.close()
        try:
            return (result[0][0], result[0][1], result[0][2])
        except (IndexError, TypeError):
            return (255, 255, 255)

    async def execute(self, arguments, message) -> None:
        if arguments[0] == "":
            user = message.author
        else:
            user = message.guild.get_member_named(arguments[0])

        async with message.channel.typing():

            cursor = await self.db.cursor()
            await cursor.execute(
                f"SELECT exp, level FROM levels WHERE user_id = '{user.id}'"
            )
            result = await cursor.fetchone()

            if result is None:
                result = (0, 0)
                
            await cursor.execute(f"SELECT user_id FROM levels ORDER BY exp DESC")
            result2 = await cursor.fetchall()
            
            rank = 1
            for i in range(len(result2)):
                if result2[i][0] == user.id:
                    rank = i + 1
                    break
                rank = i + 1
            bg_image = await self.get_bg(user.id)

            pic = await generate_profile(
                bg_image=bg_image if bg_image else None,
                profile_image=user.avatar.url,
                level=result[1],
                user_xp=result[0],
                next_xp=result[1] * 25 + 100,
                server_position=rank,
                user_name=str(user),
                user_status=str(user.status),
                font_color=await self.get_font_color(user.id)
            )

            embed = Embed()
            embed.set_author(name = f"{user.display_name}'s ranking information", icon_url = user.avatar.url)
            embed.add_field(name = "**Level**", value = f"**```css\n{result[1]}```**")
            embed.add_field(name = "**Exp**", value = f"**```css\n{result[0]}```**")
            await message.channel.send(embed=embed, file=pic)

            await cursor.close()

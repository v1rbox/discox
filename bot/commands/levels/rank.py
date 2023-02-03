import discord

from bot.base import Command
from bot.config import Config, Embed

from .__level_generator import generate_profile


class cmd(Command):
    """A discord command instance."""

    name = "rank"
    usage = "rank [*user]"
    description = "Check the rank for another user, by default this is the author."

    async def get_bg(self, user: int) -> str | None:
        result = await self.db.raw_exec_select(
            "SELECT bg FROM levels WHERE user_id = ?", (user,)
        )
        try:
            return result[0][0] if result[0][0] else None
        except (IndexError, TypeError):
            return None

    async def get_font_color(
        self, user: int
    ) -> tuple[int, int, int] | tuple[255, 255, 255]:
        result = await self.db.raw_exec_select(
            "SELECT font_color FROM levels WHERE user_id = ?", (user,)
        )
        try:
            return tuple(int(i) for i in result[0][0].split(" "))
        except (IndexError, TypeError, AttributeError):
            return (255, 255, 255)

    async def execute(self, arguments, message) -> None:
        user = None
        if not arguments or arguments[0] == "":
            user = message.author
        else:
            try:
                user = message.guild.get_member_named(arguments[0])
                assert user is not None
            except AssertionError:
                try:
                    user = await message.guild.fetch_member(arguments[0])
                except (discord.NotFound, discord.HTTPException, discord.Forbidden):
                    try:
                        user = await message.guild.fetch_member(message.mentions[0].id)
                    except IndexError:
                        embed = Embed(
                            title="No mentions associated with any of users in this server.",
                            description=f"The user mentioned `{arguments[0]}` not found.\n*Note: This command is case sensitive. E.g use `Virbox#2050` instead of `virbox#2050`.*",
                        )
                        embed.set_color("red")
                        await message.channel.send(embed=embed)
                        return
                    except (discord.NotFound, discord.HTTPException, discord.Forbidden):
                        embed = Embed(
                            title="User not found",
                            description=f"The user named `{arguments[0]}` not found.\n*Note: This command is case sensitive. E.g use `Virbox#2050` instead of `virbox#2050`.*",
                        )
                        embed.set_color("red")
                        await message.channel.send(embed=embed)
                        return

        async with message.channel.typing():
            result = await self.db.raw_exec_select(
                f"SELECT exp, level FROM levels WHERE user_id = '{user.id}'"
            )

            if len(result) == 0:
                result = (0, 0)

            else:
                result = result[0]

            result2 = await self.db.raw_exec_select(
                "SELECT user_id, level FROM levels ORDER BY level DESC, exp DESC"
            )

            rank = 1
            for i in range(len(result2)):
                if result2[i][0] == user.id:
                    rank = i + 1
                    break
                rank = i + 1
            bg_image = await self.get_bg(user.id)
            pic = None
            level=result[1] - 1
            try:
                pic = await generate_profile(
                    bg_image=bg_image if bg_image else None,
                    profile_image=user.avatar.url,
                    level,
                    user_xp=result[0],
                    next_xp=result[1] * 25 + 100,
                    server_position=rank,
                    user_name=str(user),
                    user_status=str(user.status),
                    font_color=await self.get_font_color(user.id),
                )
            except:
                pic = await generate_profile(
                    bg_image=bg_image if bg_image else None,
                    profile_image=user.avatar.url,
                    level,
                    user_xp=result[0],
                    next_xp=result[1] * 25 + 100,
                    server_position=rank,
                    user_name=f"Unrenderable Username#{user.discriminator}",  # weird ass mf username
                    user_status=str(user.status),
                    font_color=await self.get_font_color(user.id),
                )
        await message.channel.send(file=pic)

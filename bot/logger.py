import discord
from .config import Embed

class Logger:
    def newline(self):
        print()

    def custom(self, prefix, *args, **kwargs) -> None:
        print(f"[{prefix}]", *args, **kwargs)

    def log(self, *args, **kwargs) -> None:
        print("[+]", *args, **kwargs)

    def error(self, *args, **kwargs) -> None:
        print("[!]", *args, **kwargs)

    async def send_error(self, err: str, message: discord.Message) -> None:
        embed = Embed(title="Whoops", description=f"Looks like an error occured, please contact a system administrator if you belive this to be a mistake.\n```{err}```")
        embed.set_color("red")
        await message.channel.send(embed=embed)

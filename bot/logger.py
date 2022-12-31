import discord
from .config import Embed
from rich.console import Console

from datetime import datetime


class Logger:
    rich_console = Console()

    def newline(self):
        print()

    def custom(self, prefix, *args, **kwargs) -> None:
        print(f"[{prefix}]", *args, **kwargs)

    def log(self, *args, **kwargs) -> None:
        print("[+]", *args, **kwargs)

    def error(self, *args, **kwargs) -> None:
        print("[!]", *args, **kwargs)

    def debug(self, msg: str, *args, **kwargs) -> None:
        self.rich_console.print(
            f"[[magenta][bold]DEBUG[/][/]] [bold]-[/] [bold][{self.get_time()}][/]: [bold]{msg}[/]", *args, **kwargs)

    def info(self, msg: str, *args, **kwargs) -> None:
        self.rich_console.print(
            f"[[blue][bold]INFOS[/][/]] [bold]-[/] [bold][{self.get_time()}][/]: [bold]{msg}[/]", *args, **kwargs)

    def get_time(self, formatting: str = "%m/%d/%Y  %H:%M:%S") -> str:
        """Get time function

        [Args]:
            formatting (str): date formatting. Default to  "%m/%d/%Y  %H:%M:%S"

        [Returns]:
            (str): formatted time
        """

        return datetime.now().strftime(formatting)

    async def send_error(self, err: str, message: discord.Message) -> None:
        embed = Embed(
            title="Whoops", description=f"Looks like an error occured, please contact a system administrator if you belive this to be a mistake.\n```{err}```")
        embed.set_color("red")
        await message.channel.send(embed=embed)


if __name__ == "__main__":
    print("Chuck Norris never lies. The truth lies")

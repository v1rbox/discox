from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    name = "avatar"
    usage = "avatar"
    description = "Returns the avatar of the user.."

    async def execute(self, arguments, message) -> None:
        url = message.author.avatar.url
        await message.reply(url)

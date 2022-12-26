import discord

from typing import List, Tuple

from rich.table import Table
from rich.console import Console

from .logger import Logger
from .config import Config
from .manager import CommandsManager

import traceback
import re
import os


def parse_user_input(user_input: str) -> Tuple[str, List[str]]:
    """ Parse user input. """
    command_name, *args = user_input.split()
    args = [tuple(group for group in tpl if group)[0] for tpl in re.findall(r'"([^"]+)"|\'([^\']+)\'|(\S+)', " ".join(args))]
    return command_name, list(args)


def main() -> None:
    """ Main setup function. """
    bot = discord.Client(intents=discord.Intents.all())
    logger = Logger()
    config = Config()

    manager = CommandsManager(bot)

    @bot.event
    async def on_ready():
        """ When the bot is connected. """
        if bot.user is None:
            raise RuntimeError("Bot user is None")

        logger.log("Bot is ready!")
        logger.log(f"Logged in as {bot.user}")

        logger.newline()
        logger.log("Username:", f"{bot.user.name}#{bot.user.discriminator}")
        logger.log("ID:", f"{bot.user.id}")
        logger.log("Guilds:", f"{len(bot.guilds)}")
        logger.log("Prefix:", config.prefix)
        logger.newline()

        commands = [i.split(".")[0] for i in os.listdir(os.path.join("bot", "commands")) if not i.startswith("__")]
        for cmd in commands:
            manager.register(__import__(f"bot.commands.{cmd}", globals(), locals(), ["cmd"], 0).cmd)

        logger.log("Registered commands")
        for idx, command in enumerate(manager.commands, 1):
            logger.custom(
                    str(idx), f"{config.prefix}{command.name} :", command.description
            )
        logger.newline()

        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Watching Virbox videos"))

    @bot.event
    async def on_message(message: discord.Message):
        """ Handle incoming messages. """
        if (
            message.author == bot.user
            or not message.content.startswith(config.prefix)
            or not bot.is_ready()
          ):
            return

        command, arguments = parse_user_input(message.content[len(config.prefix):])

        logger.log(
            f"'{message.author}' issued command '{command}'",
            f"with arguments: {arguments}"
        )

        if command not in manager.commands_map().keys():
            logger.error("Command not found")
            await logger.send_error(f"Commad {command} not found", message)
            return

        try:
            await manager[command].execute(arguments, message)
        except Exception as e:
            await logger.send_error(str(e), message)
            print(traceback.format_exc())

    bot.run(config.token)

if __name__ == "__main__":
    main()


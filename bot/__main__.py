import re
import os
import traceback
import aiosqlite

import discord

from typing import List, Tuple

from rich.table import Table
from rich.console import Console

from .logger import Logger
from .config import Config, Embed
from .manager import CommandsManager, EventsManager
from .base import Command


logger = Logger()
config = Config()


def parse_user_input(user_input: str) -> Tuple[str, List[str]]:
    """Parse user input

    [Args]:
        user_input (str): user input

    [Returns]:
        command_name (str): the command name
        args (List[str]): command args
    """

    command_name, *args = user_input.split()
    args = [
        tuple(group for group in tpl if group)[0]

        for tpl in re.findall(
            r'"([^"]+)"|\'([^\']+)\'|\`\`\`([^\']+)\`\`\`|(\S+)',
            " ".join(args)
        )
    ]

    return command_name, args


# TODO for 'args', do a struct 'Argument' with a 'required' bool field
async def parse_usage_text(usage: str, args: List[str], message: discord.Message) -> bool:
    """Get the usage of a command into a more workable format

    [Args]:
        usage (str): command usage (help)
        args (List[str]): command arguments
        message (discord.Message): discord message

    [Returns]:
        (bool): True if all went good, False otherwise
    """

    required: List[str] = re.findall(f'<([^"]+)>', usage)
    optional: List[str] = re.findall(f'\[([^"]+)\]', usage)

    usage_args: List[Tuple[str, str]] = re.findall(
        f'\[([^\[\]]+)\]|\<([^\<\>]+)\>', usage)
    args_raw: List[str] = [f"<{i[1]}>" if i[1]
                           else f"[{i[0]}]" for i in usage_args]

    # Check for missing required arguments
    if len(args) < len(required):
        missing = required[len(args)]
        indx = usage.index(missing)
        errmsg = f"{config.prefix}{usage}\n{' '*(indx+len(config.prefix)-1)}{'^'*(len(missing)+2)}"

        embed = Embed(title="Error in command syntax",
                      description=f"Missing required argument '{missing}'\n```{errmsg}```")
        embed.set_color("red")
        await message.channel.send(embed=embed)
        return False

    # Check if the given amount of arguments exceeds the expected amount
    if len(args) > len(required) + len(optional) and args_raw[-1][1] != "*":
        embed = Embed(title="Error in command syntax",
                      description=f"Expected `{len(required) + len(optional)}` argument{'s' if len(required) + len(optional) > 1 else ''} but got `{len(args)}`.\nCommand usage: ```{config.prefix}{usage}```")
        embed.set_color("red")
        await message.channel.send(embed=embed)
        return False

    return True


def main() -> None:
    """ Main setup function. """

    db = None
    bot = discord.Client(intents=discord.Intents.all())

    manager = CommandsManager(bot, db)
    event_manager = EventsManager(bot, db)

    @bot.event
    async def on_ready():
        """ When the bot is connected. """

        if bot.user is None:
            raise RuntimeError("Bot user is None")

        db = await aiosqlite.connect("bot/assets/main.db")
        manager.db = db
        event_manager.db = db

        logger.log("Bot is ready!")
        logger.log(f"Logged in as {bot.user}")

        logger.newline()
        logger.log("Username:", f"{bot.user.name}#{bot.user.discriminator}")
        logger.log("ID:", f"{bot.user.id}")
        logger.log("Guilds:", f"{len(bot.guilds)}")
        logger.log("Prefix:", config.prefix)
        logger.newline()

        # Load the commands
        entries = [i for i in os.listdir(os.path.join(
            "bot", "commands")) if not i.startswith("__")]
        for entry in entries:
            cmd = entry.split(".")[0]
            if os.path.isfile(os.path.join("bot", "commands", entry)):
                manager.register(__import__(
                    f"bot.commands.{cmd}", globals(), locals(), ["cmd"], 0).cmd)
            else:
                # Current entry is a category
                for cmd in [
                    i.split(".")[0] for i in
                    os.listdir(os.path.join("bot", "commands", entry))
                    if not i.startswith("__")
                ]:
                    manager.register(__import__(
                        f"bot.commands.{entry}.{cmd}", globals(), locals(), ["cmd"], 0).cmd, entry)

        logger.log("Registered commands")
        for idx, command in enumerate(manager.commands, 1):
            logger.custom(
                str(idx), f"{config.prefix}{command.name} :", command.description
            )

        logger.newline()
        logger.log("Registered events")
        entries = [i.split(".")[0] for i in os.listdir(
            os.path.join("bot", "events")) if not i.startswith("__")]
        for idx, entry in zip(range(1, len(entries) + 1, 1), entries):
            event = __import__(f"bot.events.{entry}", globals(), locals(), [
                               "event"], 0).event
            event_manager.register(event)
            logger.custom(str(idx), f"{event.name} ")

        logger.newline()

        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Virbox videos"))

    @bot.event
    async def on_message(message: discord.Message):
        """ Handle incoming messages. """
        if (
            message.author == bot.user
            or not message.content.startswith(config.prefix)
            or not bot.is_ready()
        ):
            return

        command, arguments = parse_user_input(
            message.content[len(config.prefix):])

        prefixes: List[str] = [i.prefix for i in manager.categories]
        if command in prefixes:
            print({i.prefix: i for i in manager.categories if i.prefix is not None})
            try:
                cmdobj = {i.prefix: i for i in manager.categories if i.prefix is not None}[command] \
                    .commands_map()[arguments[0]]
            except KeyError:
                await logger.send_error(f"Commad '{command} {arguments[0]}' not found", message)
                return
            except IndexError:
                await logger.send_error(f"No subcommand found, use '{config.prefix}help {command}' for more information", message)
                return

            command = arguments[0]
            arguments = arguments[1:]
        else:
            try:
                cmdobj = manager[command]
            except KeyError:
                await logger.send_error(f"Commad '{command}' not found", message)
                return

        logger.log(
            f"'{message.author}' issued command '{command}'",
            f"with arguments: {arguments}"
        )

        if cmdobj.category is not None:
            if not cmdobj.category.check_permissions(message):
                logger.error("Insufficient permissions.")
                await logger.send_error("Insufficient permissions.", message)
                return

        # Join args
        usage_args: List[Tuple[str, str]] = re.findall(
            f'\[([^\[\]]+)\]|\<([^\<\>]+)\>',
            cmdobj.usage
        )
        args_raw: List[str] = [f"<{i[1]}>" if i[1]
                               else f"[{i[0]}]" for i in usage_args]

        if len(args_raw) >= 1 and args_raw[-1][1] == "*":
            args, tmp = (arguments[:len(args_raw)-1],
                         arguments[len(args_raw)-1:])
            arguments = args + [" ".join(tmp)]

        # Check if a valid number of arguments have been passed
        if await parse_usage_text(cmdobj.usage, arguments, message):
            try:
                await cmdobj.execute(arguments, message)
            except Exception as e:
                await logger.send_error(str(e), message)
                print(traceback.format_exc())

    bot.run(config.token)


if __name__ == "__main__":
    main()

import os
import re
import threading
import traceback
from typing import List, Tuple

import discord

from .config import Config, Embed
from .logger import Logger
from .manager import (CommandsManager, EventsManager, PoolingManager,
                      TasksManager)
from .sql import SQLParser

logger = Logger()
config = Config()

CREATE_STATEMENTS = [
    """
<<<<<<< HEAD
    CREATE TABLE IF NOT EXISTS "polls" (
        "guild_id"	INTEGER,
        "channel_id"	INTEGER,
        "message_id"	INTEGER UNIQUE,
        "votes" STRING,
        "when_start" INTEGER,
        "is_active" BOOLEAN,
        "type" STRING,
        PRIMARY KEY("message_id")
    )
    """,
    """
        CREATE TABLE IF NOT EXISTS "levels" (
	        "user_id"	TEXT UNIQUE,
	        "level"	INTEGER,
	        "exp"	INTEGER,
            "font_color"	TEXT,
            "bg"	TEXT DEFAULT NULL,
	        PRIMARY KEY("user_id")
        )
=======
        CREATE DATABASE IF NOT EXISTS discox;
>>>>>>> 80aa46388ff8839591f580d5c24e28cfc5711f0f
    """,
    """
        CREATE TABLE IF NOT EXISTS discox.levels (
            user_id VARCHAR(100) PRIMARY KEY,
            level INTEGER,
            exp INTEGER,
            font_color VARCHAR(25),
            bg VARCHAR(2048) DEFAULT NULL
        );
    """,
    """
        CREATE TABLE IF NOT EXISTS discox.latest_video (
	        video_id VARCHAR(50) PRIMARY KEY
        );
    """,
    """
        CREATE TABLE IF NOT EXISTS discox.request (
            Number_id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
            Member_id VARCHAR(100) NOT NULL,
            Title VARCHAR(255) NOT NULL,
            Description VARCHAR(2048) NOT NULL
        );
    """,
    """
        CREATE TABLE IF NOT EXISTS discox.reminders (
            id INTEGER AUTO_INCREMENT PRIMARY KEY,
            User VARCHAR(100),
            Timestamp INTEGER,
            Reminder VARCHAR(2048),
            Channel VARCHAR(100),
            Message VARCHAR(100)
        );
    """,
    """
        CREATE TABLE IF NOT EXISTS discox.membercount (
            membercount INT PRIMARY KEY
        );
    """,
    """
    	CREATE TABLE IF NOT EXISTS discox.starboard (
	    message_id VARCHAR(100) PRIMARY KEY,
	    board_message_id VARCHAR(100)
	);
    """,
]


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
            r'"([^"]+)"|\'([^\']+)\'|\`\`\`([^\']+)\`\`\`|(\S+)', " ".join(args)
        )
    ]

    return command_name, args


# TODO for 'args', do a struct 'Argument' with a 'required' bool field
async def parse_usage_text(
    usage: str, args: List[str], message: discord.Message
) -> bool:
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
        f"\[([^\[\]]+)\]|\<([^\<\>]+)\>", usage
    )
    args_raw: List[str] = [f"<{i[1]}>" if i[1] else f"[{i[0]}]" for i in usage_args]

    # Check for missing required arguments
    if len(args) < len(required):
        missing = required[len(args)]
        indx = usage.index(missing)
        errmsg = f"{config.prefix}{usage}\n{' '*(indx+len(config.prefix)-1)}{'^'*(len(missing)+2)}"

        embed = Embed(
            title="Error in command syntax",
            description=f"Missing required argument '{missing}'\n```{errmsg}```",
        )
        embed.set_color("red")
        await message.channel.send(embed=embed)
        return False

    # Check if the given amount of arguments exceeds the expected amount
    if len(args) > len(required) + len(optional) and args_raw[-1][1] != "*":
        embed = Embed(
            title="Error in command syntax",
            description=f"Expected `{len(required) + len(optional)}` argument{'s' if len(required) + len(optional) > 1 else ''} but got `{len(args)}`.\nCommand usage: ```{config.prefix}{usage}```",
        )
        embed.set_color("red")
        await message.channel.send(embed=embed)
        return False

    return True


async def match_type(type: str, arg: str, message: discord.Message) -> any:
    match type:
        case "int":
            if arg.removeprefix("-").isdigit():
                return int(arg)
            else:
                await logger.send_error(f"'{arg}' is not an integer.", message)
                raise ValueError()

        case "float":
            if re.match("^-?\d+(?:\.\d+)$", arg) is not None:
                return float(arg)
            else:
                await logger.send_error(f"'{arg}' is not a float.", message)
                raise ValueError()

        case "bool":
            if arg.lower() == "true":
                return True
            elif arg.lower() == "false":
                return False
            else:
                await logger.send_error(f"'{arg}' is not a boolean.", message)
                raise ValueError()

        case "member":
            # temp fix
            if arg == "":
                arg = str(message.author.id)
            try:
                user = message.guild.get_member_named(arg)
                assert user is not None
            except AssertionError:
                try:
                    user = await message.guild.fetch_member(arg)
                except (discord.NotFound, discord.HTTPException, discord.Forbidden):
                    try:
                        user = await message.guild.fetch_member(message.mentions[0].id)
                    except IndexError:
                        await logger.send_error(
                            f"The user `{arg}` was not found.\nNote: This command is case sensitive. E.g use `Virbox#2050` instead of `virbox#2050`.",
                            message,
                        )
                        raise ValueError()
                    except (
                        discord.NotFound,
                        discord.HTTPException,
                        discord.Forbidden,
                    ):
                        logger.send_error(
                            f"The user `{arg}` was not found.\nNote: This command is case sensitive. E.g use `Virbox#2050` instead of `virbox#2050`.",
                            message,
                        )
                        raise ValueError()
            return user
        case _:
            return arg


async def parse_types(
    usage: str, arguments: List[str], message: discord.Message
) -> List:
    required_args: List[str] = re.findall("\<(.*?)\>", usage)
    optional_args: List[str] = re.findall("\[(.*?)\]", usage)
    usage_args = [*required_args, *optional_args]

    args_raw: List[str] = re.findall("\[.+\]|<.+>", usage)
    usage_types = []
    for i in usage_args:
        if i[1] is None:
            usage_types.append([i[0], "str"])
        else:
            usage_types.append([i[0], i[1]])
    result = []

    for i in range(len(arguments)):
        type = (
            "str" if len(usage_args[i].split(":")) == 1 else usage_args[i].split(":")[1]
        )
        try:
            typed = await match_type(type, arguments[i], message)
            result.append(typed)
        except ValueError:
            return False
    return result


def main() -> None:
    """Main setup function."""

    db = SQLParser("bot/assets/main.db", CREATE_STATEMENTS)
    bot = discord.Client(intents=discord.Intents.all())

    bot.manager = CommandsManager(bot, db)
    bot.event_manager = EventsManager(bot, db)
    tasks_manager = TasksManager(bot, db)

    # Start autoreloads
    threading.Thread(target=PoolingManager, args=(bot,)).start()

    async def register_all():
        # Stop the bot attempting to load the commands multiple times
        if len(bot.manager.commands) != 0:
            # bot.manager.reset()
            # bot.event_manager.reset()
            # tasks_manager.reset()
            return

        # Load the commands
        entries = [
            i
            for i in os.listdir(os.path.join("bot", "commands"))
            if not i.startswith("__")
        ]
        for entry in entries:
            cmd = entry.split(".")[0]
            if os.path.isfile(os.path.join("bot", "commands", entry)):
                bot.manager.register(
                    __import__(
                        f"bot.commands.{cmd}", globals(), locals(), ["cmd"], 0
                    ).cmd,
                    file=entry,
                )
            else:
                # Current entry is a category
                for cmd in [
                    i.split(".")[0]
                    for i in os.listdir(os.path.join("bot", "commands", entry))
                    if not i.startswith("__")
                ]:
                    bot.manager.register(
                        __import__(
                            f"bot.commands.{entry}.{cmd}",
                            globals(),
                            locals(),
                            ["cmd"],
                            0,
                        ).cmd,
                        entry,
                        file=os.path.join(entry, cmd + ".py"),
                    )

        # Setup events
        entries = [
            i.split(".")[0]
            for i in os.listdir(os.path.join("bot", "events"))
            if not i.startswith("__")
        ]
        for idx, entry in zip(range(1, len(entries) + 1, 1), entries):
            event = __import__(
                f"bot.events.{entry}", globals(), locals(), ["event"], 0
            ).event
            bot.event_manager.register(event)

        # Setup tasks
        entries = [
            i.split(".")[0]
            for i in os.listdir(os.path.join("bot", "tasks"))
            if not i.startswith("__")
        ]
        for idx, entry in zip(range(1, len(entries) + 1, 1), entries):
            imp = __import__(f"bot.tasks.{entry}", globals(), locals(), ["*"], 0)
            task = [getattr(imp, i) for i in dir(imp) if i.endswith("Loop")][0]

            tasks_manager.register(task)

    bot.register_all = register_all

    @bot.event
    async def on_ready():
        """When the bot is connected."""

        await db.initialise()

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

        activity = discord.Activity(
            type=discord.ActivityType.watching, name=f"Virbox videos"
        )

        await bot.register_all()

        await bot.change_presence(activity=activity)
        bot.current_activity = activity
        bot.current_status = discord.Status.online

    @bot.event
    async def on_message(message: discord.Message):
        """Handle incoming messages."""
        if (
            message.author == bot.user
            or not message.content.startswith(config.prefix)
            or not bot.is_ready()
        ):
            await bot.event_manager.event_map()["on_message"].execute(message)
            return

        command, arguments = parse_user_input(message.content[len(config.prefix) :])

        # Check for category
        prefixes: List[str] = [i.prefix for i in bot.manager.categories]
        if command in prefixes:
            try:
                cmdobj = {
                    i.prefix: i for i in bot.manager.categories if i.prefix is not None
                }[command].commands_map()[arguments[0]]
            except KeyError:
                await logger.send_error(
                    f"Command '{command} {arguments[0]}' not found", message
                )
                return
            except IndexError:
                await logger.send_error(
                    f"No subcommand found, use '{config.prefix}help {command}' for more information",
                    message,
                )
                return

            command = arguments[0]
            arguments = arguments[1:]
        else:
            try:
                cmdobj = bot.manager[command]
            except KeyError:
                try:
                    cmdobj = [
                        [c for c in i.commands if c.name == command]
                        for i in bot.manager.categories
                        if i.prefix is None
                    ]
                    cmdobj = [i for i in cmdobj if len(i) != 0][0][0]
                except IndexError:
                    await logger.send_error(f"Command '{command}' not found", message)
                    return

        logger.log(
            f"'{message.author}' issued command '{command}'",
            f"with arguments: {arguments}",
        )

        if cmdobj.category is not None:
            if not cmdobj.category.check_permissions(message):
                logger.error("Insufficient permissions.")
                await logger.send_error("Insufficient permissions.", message)
                return
            if (
                len(cmdobj.category.channels)
                and not message.channel.id in cmdobj.category.channels
            ):
                logger.error("Channel not allowed.")
                await logger.send_error("Channel not allowed.", message)
                return

        # Join args
        usage_args: List[Tuple[str, str]] = re.findall(
            f"\[([^\[\]]+)\]|\<([^\<\>]+)\>", cmdobj.usage
        )
        args_raw: List[str] = [f"<{i[1]}>" if i[1] else f"[{i[0]}]" for i in usage_args]

        if len(args_raw) >= 1 and args_raw[-1][1] == "*":
            args, tmp = (arguments[: len(args_raw) - 1], arguments[len(args_raw) - 1 :])
            arguments = args + [" ".join(tmp)]

        # Check if a valid number of arguments have been passed
        if await parse_usage_text(cmdobj.usage, arguments, message):
            arguments_typed = await parse_types(cmdobj.usage, arguments, message)
            if arguments_typed == False:
                return
            try:
                await cmdobj.execute(arguments_typed, message)
            except Exception as e:
                await logger.send_error(str(e), message)
                print(traceback.format_exc())

    bot.run(config.token)


if __name__ == "__main__":
    main()

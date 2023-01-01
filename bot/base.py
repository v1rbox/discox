import discord
import asyncio
import aiosqlite
import subprocess
import re

from abc import ABC, abstractmethod
from dataclasses import dataclass

from typing import Optional, List, Tuple

from .logger import Logger
from .manager import Manager


# @dataclass
class Command(ABC):
    """ Base abstract class for all commands. """

    name: Optional[str] = None
    usage: Optional[str] = None
    description: Optional[str] = None
    hidden: Optional[bool] = False
    category: Optional[str] = None
    file: Optional[str] = None

    db: Optional[aiosqlite.Connection] = None
    logger = Logger()

    def __init__(self, bot: discord.Client, manager: Manager, db: aiosqlite.Connection) -> None:
        """Initialize the command.

        [Args]:
            bot (discord.Client): bot on which we'll use the command
            manager: (Manager): ?
            db (aiosqlite.Connection): command database connection

        [Raises]:
            ValueError: if 'name' field is empty
            ValueError: if 'description' field is empty
            ValueError: if 'usage' field is empty
        """

        self.bot = bot
        self.manager = manager
        self.db = db

        if not self.name:
            raise ValueError("Command name is required")

        if not self.description:
            raise ValueError("Command description is required")

        if not self.usage:
            raise ValueError("Command usage is required")
        else:
            args: List[Tuple[str, str]] = re.findall(
                f'\[([^\[\]]+)\]|\<([^\<\>]+)\>', self.usage)
            args: List[str] = [f"<{i[1]}>" if i[1]
                               else f"[{i[0]}]" for i in args]

            # Verify the integredy of the usage arguments
            last_arg = "< "
            for arg in args:
                if arg[0] == "<" and last_arg[0] == "[":
                    raise ValueError(
                        "Cannot have a positional argument after an optional argument.")
                if last_arg[1] == "*":
                    raise ValueError(
                        "Cannot have a command argument after a *arg.")
                last_arg = arg

        if not asyncio.iscoroutinefunction(self.execute):
            raise TypeError("Command execute() method must be a coroutine")

    @abstractmethod
    async def execute(self, arguments: List[str], message: discord.Message) -> None:
        """Execute the command.

        [Args]:
            arguments (List[str]): command arguments
            message (discord.Message): message which called the command

        [Raises]:
            NotImplementedError: because this method is still not implemented
        """

        raise NotImplementedError("Command execute method is required")

    async def get_contribuders(self) -> str:
        users = subprocess.run(["git", "shortlog", "-n", "-s", "--", f"bot/commands/{self.file}"], capture_output=True).stdout.decode()
        return users.strip("\n")


class Event(ABC):
    """Base abstract class for all events."""

    name: Optional[str] = None

    db: Optional[aiosqlite.Connection] = None
    logger = Logger()

    def __init__(self, bot: discord.Client, manager: Manager, db: aiosqlite.Connection) -> None:
        """Initialize the command.

        [Args]:
            bot (discord.Client): discord client
            manager (Manager): ?
            db (aiosqlite.Connection): event database connection

        [Raises]:
            ValueError: if 'name' field is empty
        """

        self.bot = bot
        self.manager = manager
        self.db = db

        if not self.name:
            raise ValueError("Command name is required")

    @abstractmethod
    async def execute(self) -> None:
        """Execute the event.

        [Raises]:
            NotImplementedError: because this method is still not implemented
        """

        raise NotImplementedError("Event execute method is required")

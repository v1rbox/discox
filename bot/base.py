import discord
import asyncio

from abc import ABC, abstractmethod

from typing import Optional, List

from .logger import Logger
from .manager import Manager

class Command(ABC):
    """ Base abstrct class for all commands. """

    name: Optional[str] = None
    usage: Optional[str] = None
    description: Optional[str] = None
    hidden: bool = False

    logger = Logger()

    def __init__(self, bot: discord.Client, manager: Manager) -> None:
        """ Initialize the command. """

        self.bot = bot
        self.manager = manager

        if not self.name:
            raise ValueError("Command name is required")

        if not self.description:
            raise ValueError("Command description is required")

        if not self.usage:
            raise ValueError("Command usage is required")

        if not asyncio.iscoroutinefunction(self.execute):
            raise TypeError("Command execute() method must be a coroutine")

    @abstractmethod
    async def execute(self, arguments: List[str], message: discord.Message) -> None:
        """ Execute the command. """
        raise NotImplementedError("Command execute method is required")

import asyncio
import re
import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Tuple

import aiosqlite
import discord
from discord.ext import tasks

from .logger import Logger
from .sql import SQLParser

# from .manager import Manager
Manager = None  # FIX: circular imports :'((


# @dataclass
class Command(ABC):
    """Base abstract class for all commands."""

    name: Optional[str] = None
    usage: Optional[str] = None
    description: Optional[str] = None
    hidden: Optional[bool] = False
    category: Optional[str] = None
    file: Optional[str] = None

    db: Optional[SQLParser] = None
    logger = Logger()

    def __init__(self, bot: discord.Client, manager: Manager, db: SQLParser) -> None:
        """Initialize the command.

        [Args]:
            bot (discord.Client): bot on which we'll use the command
            manager: (Manager): ?
            db (SQLParser): command database connection

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
                f"\[([^\[\]]+)\]|\<([^\<\>]+)\>", self.usage
            )
            args: List[str] = [f"<{i[1]}>" if i[1] else f"[{i[0]}]" for i in args]

            # Verify the integredy of the usage arguments
            last_arg = "< "
            for arg in args:
                if arg[0] == "<" and last_arg[0] == "[":
                    raise ValueError(
                        "Cannot have a positional argument after an optional argument."
                    )
                if last_arg[1] == "*":
                    raise ValueError("Cannot have a command argument after a *arg.")
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

    async def get_contributers(self) -> str:
        res = (
            subprocess.run(
                [
                    "git",
                    "shortlog",
                    "-n",
                    "-s",
                    "HEAD",
                    "--",
                    f"bot/commands/{self.file}",
                ],
                capture_output=True,
            )
            .stdout.decode()
            .strip("\n")
        )
        lines = res.split("\n")
        colums = [i.strip().split() for i in lines]
        text = "\n".join([f"{i[0]:<9}{i[1]}" for i in colums])
        return text


class Event(ABC):
    """Base abstract class for all events."""

    name: Optional[str] = None

    db: Optional[SQLParser] = None
    logger = Logger()

    def __init__(self, bot: discord.Client, manager: Manager, db: SQLParser) -> None:
        """Initialize the command.

        [Args]:
            bot (discord.Client): discord client
            manager (Manager): ?
            db (SQLParser): event database connection

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


class Task(ABC):
    """Base abstract class for all events."""

    name: Optional[str] = None

    db: Optional[SQLParser] = None
    logger = Logger()

    def __init__(self, bot: discord.Client, manager: Manager, db: SQLParser) -> None:
        """Initialize the task.

        [Args]:
            bot (discord.Client): discord client
            manager (Manager): ?
            db (SQLParser): event database connection
        """

        self.bot = bot
        self.manager = manager
        self.db = db

    async def execute(self) -> None:
        """Execute the task.

        [Raises]:
            NotImplementedError: because this method is still not implemented
        """

        raise NotImplementedError("Task execute method is required")

class Roles:
    whitelist = None
    role_color = None
    max = None
    
    def getRoleByName(self, message, role_name):
        for role in message.guild.roles:
            if role.name == role_name:
                return role

    def getAuthorRolesNames(self, message):
        return [x.name for x in message.author.roles]

    def getGuildRolesNames(self, message):
        return [x.name for x in message.author.roles]

    def isWhitelisted(self,message,argument):
        if argument.lower() in map(lambda role: role.lower(), self.whitelist):
            return True
        return False

    def authorHasRole(self,message,argument): 
        if argument.lower() in map(lambda role: role.lower(), self.getAuthorRolesNames(message)):
            return True
        return False

    def guildHasRole(self,message,argument):
        if argument.lower() in map(lambda role: role.lower(), self.getGuildRolesNames(message)):
            return True
        return False

    def hasMaxRoles(self,message):
        if len([x for x in self.getAuthorRolesNames(message) if x in self.whitelist]) >= self.max:
            return True
        return False

    async def addRole(self,message,argument):
        has_max_roles = self.hasMaxRoles(message)
        author_has_role = self.authorHasRole(message, argument)
        guild_has_role = self.guildHasRole(message, argument)
        is_whitelisted = self.isWhitelisted(message, argument) 

        if is_whitelisted == False:
            print("Distro Not Whitelisted")
        elif has_max_roles == True:
            print("User has the max amount of roles of this type")
        elif author_has_role == True:
            print("User already has this role")
        elif guild_has_role == True:
            await message.author.add_roles(self.getRoleByName(message,argument)) 
            print("Added to Role")
        elif guild_has_role == False:
            argument = self.whitelist[list(map(lambda distro: distro.lower(), self.whitelist)).index(argument.lower())]
            await message.guild.create_role(name=argument, colour=self.role_color)
            await message.author.add_roles(self.getRoleByName(message,argument)) 
            print("Created role and added to Role")
        else:
            print("Cant Add")

    def getWhitelist(self):
       print(self.whitelist) 





if __name__ == "__main__":
    print("Chuck Norris learnt to read with a book")

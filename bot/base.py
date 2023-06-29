import asyncio
import re
import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Optional, Tuple

import aiosqlite
import discord
from discord.ext import tasks
from bot.config import Embed

from .logger import Logger
from .sql import SQLParser

if TYPE_CHECKING:
    from .manager import Manager


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

    def __init__(self, bot: discord.Client, manager: "Manager", db: SQLParser) -> None:
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

    def __init__(self, bot: discord.Client, manager: "Manager", db: SQLParser) -> None:
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

    def __init__(self, bot: discord.Client, manager: "Manager", db: SQLParser) -> None:
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

# class RoleLogic:
#     def __init__(self, message):
#         self.message = message
#
#     def addRole(self, whitelist,max):
#         if len([x for x in self.getAuthorRolesNames(message) if x in self.whitelist])
#     
class RoleMenu(discord.ui.Select):
        def __init__(self, whitelist, action):
            super().__init__()
            self.whitelist = sorted(whitelist)
            self.index = 0
            self.page = 1
            self.placeholder = f"Page {self.page}"
            self.action = action
            self.regenerateMenu()

        def regenerateMenu(self):
            options = []
            begin = True;
            end = False;
            if begin == True and self.index > 0:
                options.append(discord.SelectOption(label="<-- Previous Page", value="Previous Page"))
                begin = False
            for i in range(self.index, self.index+23):
                try:
                    role = self.whitelist[i]
                    options.append(discord.SelectOption(label=f"{i+1}. {role}", value=role))
                except IndexError:
                    end = True
                    pass
            if end == False:
                options.append(discord.SelectOption(label=f"Next Page -->", value="Next Page"))
            self.options = options  

        def NextPage(self):
            self.index += 23
            self.page += 1
            self.placeholder = f"Page {self.page}"
            self.regenerateMenu()

        def PreviousPage(self):
            self.index -= 23
            self.page -= 1
            self.placeholder = f"Page {self.page}"
            self.regenerateMenu()

        async def callback(self, interaction):
            if self.view.message.author.id != interaction.user.id:
                return
            if self.values[0] == "Next Page":
                self.NextPage()
                await interaction.message.edit(view=self.view)
                await interaction.response.defer()
            if self.values[0] == "Previous Page":
                self.PreviousPage()
                await interaction.message.edit(view=self.view)
                await interaction.response.defer()
            else:
                print(self.action)
                if self.action == "Add":
                    print("Add")
                elif self.action == "Remove":
                    print("Remove")
                elif self.action == "List":
                    print("List")
                elif self.action == "Your Roles":
                    print("Your Roles")
                elif self.action == "Leaderboard":
                    print("Leaderboard")
                elif self.action == "Info":
                    print("Info")

class BackButton(discord.ui.Button):
    def __init__(self):
        super().__init__()
        self.label = "Back"
        self.style = discord.ButtonStyle.red
    async def callback(self, interaction):
        if self.view.message.author.id != interaction.user.id:
            return
        self.view.regenerateMenu()
        await interaction.message.edit(view=self.view)
        await interaction.response.defer()

class RolesButton(discord.ui.Button):
    def __init__(self):
        super().__init__()
        self.style = discord.ButtonStyle.primary
        self.label = "None"
        self.action = self.label
    async def callback(self, interaction):
        if self.view.message.author.id != interaction.user.id:
            return
        self.view.clear_items()
        self.view.add_item(RoleMenu(self.view.whitelist,self.action))
        self.view.add_item(BackButton())
        await interaction.message.edit(view=self.view)
        await interaction.response.defer()

class AddRolesButton(RolesButton):
    def __init__(self):
        super().__init__()
        self.label = "Add"
        self.action = self.label
class RemoveRolesButton(RolesButton):
    def __init__(self):
        super().__init__()
        self.label = "Remove"
        self.action = self.label
class ListRolesButton(RolesButton):
    def __init__(self):
        super().__init__()
        self.label = "List"
        self.action = self.label
class YourRolesButton(RolesButton):
    def __init__(self):
        super().__init__()
        self.label = "Your Roles"
        self.action = self.label
class LeaderboardRolesButton(RolesButton):
    def __init__(self):
        super().__init__()
        self.label = "Leaderboard"
        self.action = self.label
class InfoRolesButton(RolesButton):
    def __init__(self):
        super().__init__()
        self.label = "Info"
        self.action = self.label

class RoleView(discord.ui.View):
    max = None
    role_color = None
    prefix = None
    whitelist = None

    def __init__(self,message):
        super().__init__()
        # self.message = message.author.id
        self.message = message
        self.regenerateMenu()

    def regenerateMenu(self):
        self.clear_items()
        self.add_item(AddRolesButton())
        self.add_item(RemoveRolesButton())
        self.add_item(ListRolesButton())
        self.add_item(YourRolesButton())
        self.add_item(LeaderboardRolesButton())
        self.add_item(InfoRolesButton())

class Roles:
    prefix = None
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
        return [x.name for x in message.guild.roles]

    def isWhitelisted(self, argument):
        return (
            True if argument.lower() in [x.lower() for x in self.whitelist] else False
        )

    def authorHasRole(self, message, argument):
        return (
            True
            if argument.lower()
            in [x.lower() for x in self.getAuthorRolesNames(message)]
            else False
        )

    def guildHasRole(self, message, argument):
        return (
            True
            if argument.lower() in [x.lower() for x in self.getGuildRolesNames(message)]
            else False
        )

    def hasMaxRoles(self, message):
        return (
            True
            if len(
                [x for x in self.getAuthorRolesNames(message) if x in self.whitelist]
            )
            >= self.max
            else False
        )

    async def addRole(self, message, argument):
        if not self.isWhitelisted(argument):
            return f"***{argument} is not a whitelisted {self.prefix} role***"
        elif self.hasMaxRoles(message):
            return (
                f"***{message.author.name} has the max amount of {self.prefix} roles***"
            )
        elif self.authorHasRole(message, argument):
            return f"***{message.author.name} already has the {argument} {self.prefix} role***"
        elif self.guildHasRole(message, argument):
            argument = self.whitelist[
                list(map(lambda distro: distro.lower(), self.whitelist)).index(
                    argument.lower()
                )
            ]
            await message.author.add_roles(self.getRoleByName(message, argument))
            return f"***{message.author.name} has been added to the {argument} {self.prefix} role***"
        # Creates role and adds to role if role does not exist yet
        elif not self.guildHasRole(message, argument):
            argument = self.whitelist[
                list(map(lambda distro: distro.lower(), self.whitelist)).index(
                    argument.lower()
                )
            ]
            await message.guild.create_role(name=argument, colour=self.role_color)
            await message.author.add_roles(self.getRoleByName(message, argument))
            return f"***{message.author.name} has been added to the {argument} {self.prefix} role***"
        else:
            return f"***Cannot add to {self.prefix} role***"

    async def removeRole(self, message, argument):
        if not self.isWhitelisted(argument):
            return f"***{argument} is not a whitelisted {self.prefix} role***"
        elif not self.authorHasRole(message, argument):
            return f"***{message.author.name} does not have the {argument} {self.prefix} role***"
        else:
            argument = self.whitelist[
                list(map(lambda distro: distro.lower(), self.whitelist)).index(
                    argument.lower()
                )
            ]
            role = self.getRoleByName(message, argument)
            await message.author.remove_roles(role)
            # Removes the role if the role is now empty
            if len(role.members) == 0:
                await role.delete()
            return f"***{message.author.name} has been removed from the {argument} {self.prefix} role***"

    def getRoles(self, message):
        roles = [x for x in self.getAuthorRolesNames(message) if x in self.whitelist]
        if len(roles) == 0:
            return f"***{message.author.name} has no {self.prefix} roles yet***"
        else:
            desc = ""
            for role in roles:
                desc += f"{role}\n"
            return f"***{message.author.name}'s {self.prefix} roles:\n\n{desc}***"

    def getWhitelist(self):
        if len(self.whitelist) == 0:
            return f"***There are currently no whitelisted {self.prefix} roles***"
        else:
            desc = ""
            for role in self.whitelist:
                desc += f"{role}\n"
            return f"***Whitelisted {self.prefix} roles:\n\n{desc}***"

    def getLeaderboard(self, message):
        leaderboard = []
        for role in self.getGuildRolesNames(message):
            if (
                role in self.whitelist
                and len(self.getRoleByName(message, role).members) > 0
            ):
                leaderboard.append(
                    {
                        "role": role,
                        "count": len(self.getRoleByName(message, role).members),
                    }
                )
        if leaderboard == []:
            return f"***Nobody has any {self.prefix} roles yet***"
        else:
            leaderboard = sorted(leaderboard, key=lambda d: d["count"], reverse=True)
            desc = ""
            for role in leaderboard:
                desc += f"Current {role['role']} users: {role['count']}\n"
            return f"***{self.prefix} roles leaderboard:\n\n{desc}***"


if __name__ == "__main__":
    print("Chuck Norris learnt to read with a book")

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

class RoleMenu(discord.ui.Select):
        def __init__(self, whitelist):
            super().__init__()
            self.whitelist = sorted(whitelist)
            self.index = 0
            self.page = 1
            self.placeholder = f"Page {self.page}"
            self.regenerateMenu()

        def regenerateMenu(self):
            options = []
            begin = True;
            end = False;
            if len(self.whitelist) == 0:
                options.append(discord.SelectOption(label="No Options Available", value="No Options Available"))
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
            message = self.view.message
            whitelist = self.view.whitelist
            selection = self.values[0]
            action = self.view.action

            if message.author.id != interaction.user.id:
                return
            if selection == "Next Page":
                self.NextPage()
                await interaction.message.edit(view=self.view)
                await interaction.response.defer()
                return
            if selection == "Previous Page":
                self.PreviousPage()
                await interaction.message.edit(view=self.view)
                await interaction.response.defer()
                return
            else:
                # Prevents empty select menu
                if selection == "No Options Available":
                        self.view.regenerateMenu()
                        await interaction.message.edit(embed=self.view.default_embed,view=self.view)
                        await interaction.response.defer()
                        return

                if action == "Remove":
                    #Removes the selected role
                    role = self.view.getRoleByName(self.view.message, self.values[0])
                    await message.author.remove_roles(role)
                    # Removes the role from the server if the role is now empty
                    if len(role.members) == 0:
                        await role.delete()
                    embed = Embed(title=f"{self.view.cap}", description=f"`{message.author.name}` has been removed from the `{selection}` {self.view.prefix} role")
                    self.view.regenerateMenu()
                    await interaction.message.edit(embed=embed,view=self.view)
                    await interaction.response.defer()
                    return

                elif action == "Add":
                    # Gets user's current bot given roles
                    user_roles = [x for x in message.author.roles if x.name.lower() in list(map(lambda role:role.lower(),whitelist))]
                    # Ensures roles dont exceed maximum amound of allowed roles
                    if len(user_roles) >= self.view.max:
                        embed = Embed(title=f"{self.view.cap}", description=f"`{message.author.name}` already has the max amount of {self.view.prefix} roles")
                        embed.set_color("red")
                        self.view.regenerateMenu()
                        await interaction.message.edit(embed=embed,view=self.view)
                        await interaction.response.defer()
                        return
                    # Checks if role already exists, if not, creates it
                    if selection.lower() not in [x.name.lower() for x in message.guild.roles]:
                        await message.guild.create_role(name=selection, colour=self.view.role_color)
                    # Adds user to selected role
                    try:
                        await message.author.add_roles(self.view.getRoleByName(message, selection))
                    except AttributeError: 
                        embed = Embed(title=f"{self.view.cap}", description=f"Something went wrong, lets try that again")
                        embed.set_color("red")
                        self.view.regenerateMenu()
                        await interaction.message.edit(embed=embed,view=self.view)
                        await interaction.response.defer()
                        return
                    embed = Embed(title=f"{self.view.cap}", description=f"`{message.author.name}` has been added to the `{selection}` {self.view.prefix} role")
                    self.view.regenerateMenu()
                    await interaction.message.edit(embed=embed,view=self.view)
                    await interaction.response.defer()
                    return

                elif action == "Users":
                    users = 0
                    if selection.lower() in [x.name.lower() for x in message.guild.roles]:
                        users = len(self.view.getRoleByName(message,selection).members)
                    embed = Embed(title=f"{self.view.cap}", description=f"`{selection}` has `{users}` users on this server")
                    self.view.regenerateMenu()
                    await interaction.message.edit(embed=embed,view=self.view)
                    await interaction.response.defer()
                    return

class BackButton(discord.ui.Button):
    def __init__(self):
        super().__init__()
        self.label = "Back"
        self.style = discord.ButtonStyle.red
    async def callback(self, interaction):
        if self.view.message.author.id != interaction.user.id:
            return
        self.view.regenerateMenu()
        await interaction.message.edit(embed=self.view.default_embed,view=self.view)
        await interaction.response.defer()

class RolesButton(discord.ui.Button):
    def __init__(self):
        super().__init__()
        self.style = discord.ButtonStyle.primary
        self.label = "None"
        self.action = self.label
    # self.view.* attributes are only available in the callback
    async def callback(self, interaction):
        if self.view.message.author.id != interaction.user.id:
            return
        self.whitelist = self.view.whitelist

        # Only gives a list of removable rolls to the select menu 
        if self.action == "Remove":
            self.whitelist = [x.name for x in self.view.message.author.roles if x.name.lower() in list(map(lambda role:role.lower(),self.view.whitelist))]

        # Only gives a list of available roles to the select menu
        if self.action == "Add":
            self.whitelist = [x for x in self.view.whitelist if x.lower() not in list(map(lambda role:role.name.lower(), self.view.message.author.roles))]

        self.view.action = self.action
        self.view.clear_items()
        self.view.add_item(RoleMenu(self.whitelist))
        self.view.add_item(BackButton())
        embed = Embed(title=f"{self.view.cap} {self.action}", description=f"Please select and option")
        await interaction.message.edit(embed=embed,view=self.view)
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
class UsersRolesButton(RolesButton):
    def __init__(self):
        super().__init__()
        self.label = "Users"
        self.action = self.label
class YourRolesButton(RolesButton):
    def __init__(self):
        super().__init__()
        self.label = "Your Roles"
        self.action = self.label
    async def callback(self, interaction):
        if self.view.message.author.id != interaction.user.id:
            return
        user_roles = [x.name for x in self.view.message.author.roles if x.name.lower() in list(map(lambda role:role.lower(),self.view.whitelist))]
        desc = ""
        for role in user_roles:
            desc += f"`{role}`\n"
        embed = Embed(title=f"Your {self.view.cap} Roles", description=f"{desc}")
        await interaction.message.edit(embed=embed,view=self.view)
        await interaction.response.defer()
class LeaderboardRolesButton(RolesButton):
    def __init__(self):
        super().__init__()
        self.label = "Leaderboard"
        self.action = self.label
    async def callback(self, interaction):
        if self.view.message.author.id != interaction.user.id:
            return

        leaderboard = []
        desc = ""
        roles = [x for x in self.view.message.guild.roles if x.name.lower() in list(map(lambda role:role.lower(), self.view.whitelist)) ]
        for role in roles:
            leaderboard.append({"role":role,"count":len(role.members)})
        leaderboard = sorted(leaderboard, key=lambda d: d["count"], reverse=True)
        for i,role in enumerate(leaderboard):
            if i == 10:
                break
            desc += f"**#{i+1}** `{role['role']}` users: {role['count']}\n"
        embed = Embed(title=f"{self.view.cap} Leaderboard", description=f"{desc}")
        await interaction.message.edit(embed=embed,view=self.view)
        await interaction.response.defer()

class RoleView(discord.ui.View):
    max = None
    role_color = None
    prefix = None
    whitelist = None

    def __init__(self,message):
        super().__init__()
        # self.message = message.author.id
        self.message = message
        self.selection = None
        self.action = None
        self.cap = self.prefix.capitalize()
        self.default_embed = Embed(title=f"{self.cap}",description="Please select an option")
        self.regenerateMenu()

    def regenerateMenu(self):
        self.clear_items()
        self.add_item(AddRolesButton())
        self.add_item(RemoveRolesButton())
        self.add_item(YourRolesButton())
        self.add_item(LeaderboardRolesButton())
        self.add_item(UsersRolesButton())

    def getRoleByName(self, message, role_name):
        for role in message.guild.roles:
            if role.name.lower() == role_name.lower():
                return role


if __name__ == "__main__":
    print("Chuck Norris learnt to read with a book")

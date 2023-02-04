from abc import ABC, abstractmethod
from typing import List, Optional

import discord

from .base import Command
from .config import Config

config = Config()


class Category(ABC):
    """Template for category classes."""

    name: Optional[str] = None
    prefix: Optional[str] = None
    commands: List[Command] = []
    channels: List[int] = []

    def __init__(self) -> None:
        """Initialize the category."""
        self.commands_map: Callable[..., Dict[str, Command]] = lambda: {
            command.name: command for command in self.commands if command.name
        }

        if not self.name:
            raise ValueError("Category name is required")

    @abstractmethod
    def check_permissions(self, message: discord.Message) -> bool:
        raise NotImplementedError("Check permissions method is required")


class FunCategory(Category):
    """A command category instance."""

    name = "fun"
    prefix = None
    commands: List[Command] = []

    def check_permissions(self, message: discord.Message) -> bool:
        return True


class UtilityCategory(Category):
    """A command category instance."""

    name = "utility"
    prefix = None
    commands: List[Command] = []

    def check_permissions(self, message: discord.Message) -> bool:
        return True


class DistroCategory(Category):
    """A command category instance."""

    name = "distroroles"
    prefix = "distro"
    commands: List[Command] = []
    channels = [config.role_channel]

    def check_permissions(self, message: discord.Message) -> bool:
        return True


class CodeCategory(Category):
    """A command category instance."""

    name = "coderoles"
    prefix = "code"
    commands: List[Command] = []
    channels = [config.role_channel]

    def check_permissions(self, message: discord.Message) -> bool:
        return True


class PresenceCategory(Category):
    """A command category instance."""

    name = "changePresence"
    prefix = "change"
    commands: List[Command] = []

    def check_permissions(self, message: discord.Message) -> bool:
        # Check for a specific role in the member
        return any([i.id == config.mod_role_id for i in message.author.roles])


class ModCategory(Category):
    """A command category instance."""

    name = "mod"
    prefix = None
    commands: List[Command] = []

    def check_permissions(self, message: discord.Message) -> bool:
        # Checking for everyone who are a mod in the server. Usually the server has more mod roles than just one
        return any([i.id in config.mod_role_id for i in message.author.roles])


class RemindCategory(Category):
    """A command category instance."""

    name = "reminders"
    prefix = "reminder"
    commands: List[Command] = []

    def check_permissions(self, message: discord.Message) -> bool:
        return True


class RequestCategory(Category):
    """A command category instance."""

    name = "request"
    prefix = "req"
    config = config

    def check_permissions(self, message: discord.Message) -> bool:
        return True


class LevelCategory(Category):
    """A command category instance."""

    name = "levels"
    prefix = None

    def check_permissions(self, message: discord.Message) -> bool:
        return True


class GameCategory(Category):
    """A command category instance."""

    name = "games"
    prefix = None
    commands: List[Command] = []

    def check_permissions(self, message: discord.Message) -> bool:
        return True


if __name__ == "__main__":
    print(
        "I had a dream where I was fighting Chuck Norris. That day I woke up with scars."
    )

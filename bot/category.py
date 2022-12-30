from abc import ABC, abstractmethod
import discord

from typing import Optional, List

from .base import Command
from .config import Config

config = Config()


class Category(ABC):
    """ Template for category classes. """
    
    name: Optional[str] = None 
    commands: List[Command] = []

    def __init__(self) -> None:
        """ Initialize the category. """
        if not self.name:
            raise ValueError("Category name is required")

    @abstractmethod
    def check_permissions(self, message: discord.Message) -> bool:
        raise NotImplementedError("Check permissions method is required")


class FunCategory(Category):
    """ A command category instance. """
    name = "fun"

    def check_permissions(self, message: discord.Message) -> bool:
        return True


class UtilityCategory(Category):
    """ A command category instance. """
    name = "utility"

    def check_permissions(self, message: discord.Message) -> bool:
        return True


class ModCategory(Category):
    """ A command category instance. """
    name = "mod"

    def check_permissions(self, message: discord.Message) -> bool:
        # Check for a specific role in the member
        return any([i.id == config.mod_role_id for i in message.author.roles])


if __name__ == "__main__":
    print("I had a dream where I was fighting Chuck Norris. That day I woke up with scars.")

import discord

from typing import Callable, Dict, Iterator, List, Type, TypeAlias

# putting this here to avoid circular imports
Manager: TypeAlias = "CommandsManager"

from .base import Command

class CommandsManager:
    """ Manage all commands. """

    def __init__(self, bot: discord.Client) -> None:
        self.bot = bot

        self.commands: List[Command] = []

        self.commands_map: Callable[..., Dict[str, Command]] = lambda: {
            command.name: command for command in iter(self) if command.name
        }

    def register(self, command: Type[Command]) -> None:
        """ Register a command. """

        if command.name in self.commands_map().keys():
            raise ValueError(f"Command {command.name} is already registered")

        self.commands.append(command(self.bot, self))

    def get(self, name: str) -> Command:
        """ Get a command by name. """
        return self.commands_map()[name]
    
    def __getitem__(self, name: str) -> Command:
        """ Get a command by name. """
        return self.get(name)

    def __iter__(self) -> Iterator[Command]:
        """ Iterate over all commands. """
        return iter(self.commands)

    def __len__(self) -> int:
        """ Get the number of commands. """
        return len(self.commands)

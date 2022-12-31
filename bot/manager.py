import discord
import aiosqlite

from typing import Callable, Dict, Iterator, List, Type, TypeAlias, Optional

# putting this here to avoid circular imports
Manager: TypeAlias = "CommandsManager"

from .base import Command, Event
from .category import Category

class CommandsManager:
    """ Manage all commands. """

    def __init__(self, bot: discord.Client, db: aiosqlite.Connection) -> None:
        self.bot = bot
        self.db = db

        pkg = __import__("bot.category", globals(), locals(), ["*"], 0)
        self.categories: List[Category] = [
            getattr(pkg, i)() for i in dir(pkg) 
            if i.endswith("Category") and i != "Category"]

        self.commands: List[Command] = []

        self.categories_map: Callable[..., Dict[str, Category]] = lambda: {
            category.name: category for category in self.categories if category.name
        }
        self.commands_map: Callable[..., Dict[str, Command]] = lambda: {
            command.name: command for command in iter(self) if command.name
        }

    def register(self, command: Type[Command], category: Optional[str] = None) -> None:
        """ Register a command. """

        if command.name in self.commands_map().keys():
            raise ValueError(f"Command {command.name} is already registered")

        cmd = command(self.bot, self, self.db)

        if category is not None:
            cat: Category = self.get_category(category)
            cat.commands.append(cmd)
            cmd.category = cat
        else:
            self.commands.append(cmd)

    def get(self, name: str) -> Command:
        """ Get a command by name. """
        return self.commands_map()[name]

    def get_category(self, name: str) -> List[Command]:
        """ Get a category by name. """
        return self.categories_map()[name]
    
    def __getitem__(self, name: str) -> Command:
        """ Get a command by name. """
        return self.get(name)

    def __iter__(self) -> Iterator[Command]:
        """ Iterate over all commands. """
        return iter(self.commands)

    def __len__(self) -> int:
        """ Get the number of commands. """
        return len(self.commands)


class EventsManager:
    """ Manage all event listneres. """

    def __init__(self, bot: discord.Client, db: aiosqlite.Connection) -> None:
        self.bot = bot
        self.db = db

        self.events: List[Event] = []

        self.event_map: Callable[..., Dict[str, Event]] = lambda: {
            event.name: event for event in iter(self) if event.name
        }

    def register(self, event: Event) -> discord.Client:
        if not event.name.startswith("on_"):
            raise NameError(f"Not a valid listner name '{event.name}'.")

        if event.name in self.event_map().keys():
            raise ValueError(f"Event {event.name} is already registered")

        event = event(self.bot, self, self.db)

        setattr(self.bot, event.name, event.execute)
        self.events.append(event)

        return self.bot

    def get(self, name: str) -> Event:
        """ Get a event by name. """
        return self.event_map()[name]

    def __getitem__(self, name: str) -> Event:
        """ Get a event by name. """
        return self.get(name)

    def __iter__(self) -> Iterator[Event]:
        """ Iterate over all events. """
        return iter(self.events)

    def __len__(self) -> int:
        """ Get the number of events. """
        return len(self.events)


if __name__ == "__main__":
    print("Jesus Christ was born in 1940 before Chuck Norris")

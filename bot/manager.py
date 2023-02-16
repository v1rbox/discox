import importlib
import os
import time
from threading import Thread
from typing import Callable, Dict, Iterator, List, Optional, Type, TypeAlias

import aiosqlite
import discord

from .logger import Logger
from .sql import SQLParser

# putting this here to avoid circular imports
Manager: TypeAlias = "CommandsManager"

from .base import Command, Event, Task
from .category import Category


class CommandsManager:
    """Manage all commands."""

    def __init__(self, bot: discord.Client, db: SQLParser) -> None:
        self.bot = bot
        self.db = db

        pkg = __import__("bot.category", globals(), locals(), ["*"], 0)
        self.categories: List[Category] = [
            getattr(pkg, i)()
            for i in dir(pkg)
            if i.endswith("Category") and i != "Category"
        ]

        self.commands: List[Command] = []

        self.categories_map: Callable[..., Dict[str, Category]] = lambda: {
            category.name: category for category in self.categories if category.name
        }
        self.commands_map: Callable[..., Dict[str, Command]] = lambda: {
            command.name: command for command in iter(self) if command.name
        }

    def register(
        self,
        command: Type[Command],
        category: Optional[str] = None,
        file: Optional[str] = None,
    ) -> None:
        """Register a command."""

        if command.name in self.commands_map().keys():
            raise ValueError(f"Command {command.name} is already registered")

        cmd = command(self.bot, self, self.db)
        cmd.file = file

        if category is not None:
            cat: Category = self.get_category(category)
            cat.commands.append(cmd)
            cmd.category = cat
        else:
            self.commands.append(cmd)

    def reset(self) -> None:
        """Reload the manager obj"""
        pkg = importlib.reload(
            __import__("bot.category", globals(), locals(), ["*"], 0)
        )
        self.categories: List[Category] = [
            getattr(pkg, i)()
            for i in dir(pkg)
            if i.endswith("Category") and i != "Category"
        ]

        self.commands: List[Command] = []

        self.categories_map: Callable[..., Dict[str, Category]] = lambda: {
            category.name: category for category in self.categories if category.name
        }
        self.commands_map: Callable[..., Dict[str, Command]] = lambda: {
            command.name: command for command in iter(self) if command.name
        }

    def get(self, name: str) -> Command:
        """Get a command by name."""
        return self.commands_map()[name]

    def get_category(self, name: str) -> List[Command]:
        """Get a category by name."""
        return self.categories_map()[name]

    def __getitem__(self, name: str) -> Command:
        """Get a command by name."""
        return self.get(name)

    def __iter__(self) -> Iterator[Command]:
        """Iterate over all commands."""
        return iter(self.commands)

    def __len__(self) -> int:
        """Get the number of commands."""
        return len(self.commands)


class EventsManager:
    """Manage all event listneres."""

    def __init__(self, bot: discord.Client, db: SQLParser) -> None:
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

        if event.name != "on_message":
            setattr(self.bot, event.name, event.execute)

        self.events.append(event)

        return self.bot

    def reset(self) -> None:
        self.events = []

    def get(self, name: str) -> Event:
        """Get a event by name."""
        return self.event_map()[name]

    def __getitem__(self, name: str) -> Event:
        """Get a event by name."""
        return self.get(name)

    def __iter__(self) -> Iterator[Event]:
        """Iterate over all events."""
        return iter(self.events)

    def __len__(self) -> int:
        """Get the number of events."""
        return len(self.events)


class TasksManager:
    """Manage all tasks."""

    def __init__(self, bot: discord.Client, db: SQLParser) -> None:
        self.bot = bot
        self.db = db

        self.tasks: List[Task] = []

        self.task_map: Callable[..., Dict[str, Event]] = lambda: {
            task.name: task for task in iter(self)
        }

    def register(self, task: Task) -> discord.Client:
        task = task(self.bot, self, self.db)
        task.execute.start()
        self.tasks.append(task)

        return self.bot

    def reset(self) -> None:
        for i in tasks:
            task.execute.cancel()

        self.tasks = []

    def get(self, name: str) -> Event:
        """Get a event by name."""
        return self.event_map()[name]

    def __getitem__(self, name: str) -> Event:
        """Get a event by name."""
        return self.get(name)

    def __iter__(self) -> Iterator[Event]:
        """Iterate over all events."""
        return iter(self.events)

    def __len__(self) -> int:
        """Get the number of events."""
        return len(self.events)


class PoolingManager:
    def __init__(self, bot) -> None:
        self.tracked: Dict[str, str] = self.get_dir()

        while True:
            if (res := self.cmp_tracker(self.get_dir())) is None:
                time.sleep(2)
            else:
                if res.startswith("bot/commands/"):
                    Logger.log(None, f"{res} Reloading commands...\n")

                    # Reset the current manager
                    bot.manager.reset()

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
                                importlib.reload(
                                    __import__(
                                        f"bot.commands.{cmd}",
                                        globals(),
                                        locals(),
                                        ["cmd"],
                                        0,
                                    )
                                ).cmd,
                                file=entry,
                            )
                        else:
                            # Current entry is a category
                            for cmd in [
                                i.split(".")[0]
                                for i in os.listdir(
                                    os.path.join("bot", "commands", entry)
                                )
                                if not i.startswith("__")
                            ]:
                                bot.manager.register(
                                    importlib.reload(
                                        __import__(
                                            f"bot.commands.{entry}.{cmd}",
                                            globals(),
                                            locals(),
                                            ["cmd"],
                                            0,
                                        )
                                    ).cmd,
                                    entry,
                                    file=os.path.join(entry, cmd + ".py"),
                                )
                elif res.startswith("bot/events/"):
                    Logger.log(None, f"{res} Reloading events...\n")
                    # Reset old event manager
                    bot.event_manager.reset()

                    # Setup events
                    entries = [
                        i.split(".")[0]
                        for i in os.listdir(os.path.join("bot", "events"))
                        if not i.startswith("__")
                    ]
                    for idx, entry in zip(range(1, len(entries) + 1, 1), entries):
                        event = importlib.reload(
                            __import__(
                                f"bot.events.{entry}", globals(), locals(), ["event"], 0
                            )
                        ).event
                        bot.event_manager.register(event)

                # bot.register_all()
                self.tracked = self.get_dir()

    def drive(self, c):
        """Run a curentine function outside loop"""
        while True:
            try:
                c.send(None)
            except StopIteration as e:
                return e.value

    def get_dir(self) -> Dict[str, str]:
        """Get all the directories and files, returns MD5 hash"""
        tracker: Dict[str, str] = {}
        for dirpath, dirnames, filenames in os.walk("bot"):
            for filename in filenames:
                if filename in ["main.db"] or filename.endswith(".pyc"):
                    continue

                # Get when the file was last edited
                edited = os.path.getctime(os.path.join(dirpath, filename))
                tracker[os.path.join(dirpath, filename)] = edited

        return tracker

    def cmp_tracker(self, tracker) -> Optional[str]:
        """Compare two tracker dicts to watch for changes, returns none if no change"""
        checked: List[str] = []

        for file, ts in self.tracked.items():
            cts = tracker.get(file)  # Changed timestamp
            if cts is None:
                return f"{file} was removed."
            elif ts != cts:
                return f"{file} was edited."

            checked.append(file)

        for file, ts in tracker.items():
            if file not in checked:
                return f"{file} was created."

        return None


if __name__ == "__main__":
    print("Jesus Christ was born in 1940 before Chuck Norris")

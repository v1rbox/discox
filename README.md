[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/badges/StandWithUkraine.svg)](https://stand-with-ukraine.pp.ua)

# Discox

Virbox Discord Bot community project ^\_^

Written in ~~blazingly fast~~ **effective** Python.

## Installation

1. Follow the instructions [here](https://discordpy.readthedocs.io/en/stable/discord.html) to add a Discord Bot to your test server.
2. After the bot is added clone the project repo.
3. Copy the Bot Token from Discord Developer Portal.
4. Create a environment variable and pass it in the config.py file under the token data member of the Config Class. You can also directly copy paste the token but be sure to remove it while committing.
5. Go to the project repo and run `python3 -m bot`

This will start the bot, you can now work with it in the test servers.

## Getting started

Want to add a command to the project? This is the best place to start!

The bot is written using a package called discord-py, you can find its documentation [here](https://discordpy.readthedocs.io/en/stable/api.html), A few changes have been made however and that is what we will be covering here.

Firstly to create a command lets look at a quickstart example

```py
# /bot/commands/ping.py
from bot.config import Config, Embed
from bot.base import Command

class Cmd(Command):
    """ A discord command instance. """

    name = "ping"
    usage = "ping"
    description = "Check the current latency of the bot."

    async def execute(self, arguments, message) -> None:
        embed = Embed(title="Hello world!", description="This is a test embed")
        await message.channel.send("Im alive!!", embed=embed)
```

In this example we create a class with the name ping, to execute the command we will use `<prefix>ping`

The usage attribude descirbes how to use the command, this is usefull info for our help system and argument parser. A element wrapped in `[]` is requred while `<>` is optional.

When the user gives an argument it is posible to wrap it in qoutes to input multiple words

### Accessing bot and command manager objects

All commands will be able to access `self.bot`, `self.manager` and `self.logger`

### Embeds

In the project we changed a bit how embeds work, we have a default format that of cause can be overwritten if nessesarry. You can use all the default attribudes and methods from [the pydis documentation](https://discordpy.readthedocs.io/en/stable/api.html?highlight=embed#discord.Embed).

As well as this we implemented a set color method to set the default color, by default embed colors are green. You need to use this to set the color of the embed, here is an example.

```py
embed = Embed(title="Hello world!")
embed.set_color("red")
```

The embed object will now be red. Supported colors currently are `green` and `red`.

### Using the inbuild logger module

Here are a few basic examples (all methods documentation are disponible in actual python file)

```py
self.logger.log("That worked!")
## [+] That worked!

self.logger.error("That didnt :(")
## [-] That didnt :(

self.logger.custom("?", "This is so cool omg")
## [?] This is so cool omg

self.logger.newline()
## \n

self.logger.send_error("That didnt work :(", message)
## Sends an emebed in the channel that the message was sent telling the user there was an error
## You can also use raise within a command to trigger this same event

raise ValueError("I am not happy!")
## Same result as above, an emebed will be sent in the channel the command was triggered
```

## Setting up events

All events live in /bot/events, the filename you use can be anything eg. `reaction_add`, `member_join` etc.

To register an event define a class within your file named `event`, here is an example

```py
# /bot/events/reaction_add.py
from bot.config import Config, Embed
from bot.base import Event

class event(Event):
    """ A discord event instance. """

    name = "on_raw_reaction_add"

    async def execute(self, payload) -> None:
        print(payload)
```

Here we define a `on_raw_reaction_add` event that gets triggered every time a reaction is added to a message.

The name is the name of the event that it should listen on.

In the object a `self.bot` and `self.manager` is also exposed in case you need to access those.

The execute function gets called every time the event name is triggered, you should add what ever arguments are listed in the documentation just remember to add self as the first argument.

[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/badges/StandWithUkraine.svg)](https://stand-with-ukraine.pp.ua)

# Discox
Virbox Discord Bot community project ^\_^

Written in ~~blazingly fast~~ **effective** Python.

## Getting started

Want to add a command to the project? This is the best place to start!

The bot is written using a package called discord-py, you can find its documentation [here](https://discordpy.readthedocs.io/en/stable/api.html), A few changes have been made however and that is what we will be covering here.

Firstly to create a command lets look at a quickstart example

```py
# bot/commands/ping.py
from bot.config import Config, Embed
from bot.base import Command

class cmd(Command):
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

Here are a few basic examples

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

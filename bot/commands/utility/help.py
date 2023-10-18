import asyncio

from bot.base import Command, Logger
from bot.config import Config, Embed


class cmd(Command):
    """Help command."""

    name = "help"
    usage = "help [*command]"
    description = "The command you just ran; shows a help embed."

    async def category_help(self, message, name="") -> None:
        categories = self.manager.categories
        prefixes = [i.prefix for i in categories]
        if not name:
            page = 0
        else:
            page = prefixes.index(name) + 1

        msg = await message.channel.send("Loading...")
        for i in ["◀️", "🔼", "🔽", "▶️", "🔍"]:
            await msg.add_reaction(i)

        indx = 0
        while True:
            print(page, indx)
            page = min(max(0, page), len(categories))

            # If we are on the first page (show all uncategorised commands)
            if page == 0:
                commands = self.manager.commands
                name = "Uncategorised commands"
                cat_tag = ""
            else:
                commands = categories[page - 1].commands
                name = categories[page - 1].name
                cat_tag = categories[page - 1].prefix
                cat_tag = cat_tag + " " if cat_tag else ""

            indx = min(max(0, indx), len(commands) - 1)

            embed = Embed(
                title=f"{name} - Page {page+1} / {len(categories)+1}",
                description=f"List of all commands and their description\nRun `{Config.prefix}{self.usage}` to get information about a specific command (still wip).\n\n",
            )
            embed.set_author(name=f"Help menu")

            for idx, command in zip(range(len(commands)), commands):
                print(command, idx)
                embed.description += (
                    f"`{Config.prefix}{cat_tag}{command.name}`\n"
                    if indx != idx
                    else f"**`{Config.prefix}{cat_tag}{command.usage}`**\n"
                )
                embed.description += f"{command.description.strip()}\n\n"

            await msg.edit(content="", embed=embed)

            def check(reaction, user):
                return user == message.author and str(reaction.emoji) in [
                    "◀️",
                    "▶️",
                    "🔼",
                    "🔽",
                    "🔍",
                ]

            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", timeout=120.0, check=check
                )
            except asyncio.TimeoutError:
                await msg.clear_reactions()
                return

            if str(reaction.emoji) == "◀️":
                page -= 1
            elif str(reaction.emoji) == "▶️":
                page += 1
            elif str(reaction.emoji) == "🔼":
                indx -= 1
            elif str(reaction.emoji) == "🔽":
                indx += 1
            elif str(reaction.emoji) == "🔍":
                # Get the command object
                if page == 0:
                    command = self.manager.commands[indx]
                    cat_tag = ""
                else:
                    command = categories[page - 1].commands[indx]
                    cat_tag = categories[page - 1].prefix
                    cat_tag = cat_tag + " " if cat_tag else ""

                data = await command.get_contributers()

                await msg.clear_reactions()
                embed = Embed(
                    title=f"{command.name.capitalize()} command",
                    description=f"Usage:\n`{Config.prefix}{cat_tag}{command.usage}`\n{command.description}\n\nContributors for this command```Commits  User\n{data}```",
                )
                await msg.edit(content="", embed=embed)
                await msg.add_reaction("↩️")

                def check(reaction, user):
                    return user == message.author and str(reaction.emoji) in ["↩️"]

                try:
                    reaction, user = await self.bot.wait_for(
                        "reaction_add", timeout=120.0, check=check
                    )
                except asyncio.TimeoutError:
                    await msg.clear_reactions()
                    return

                await msg.clear_reactions()
                for i in ["◀️", "🔼", "🔽", "▶️", "🔍"]:
                    await msg.add_reaction(i)

            await reaction.remove(message.author)

    async def command_help(self, message, command):
        if command.category and command.category.prefix:
            cat = command.category.prefix + " "
        else:
            cat = ""

        data = await command.get_contributers()
        embed = Embed(
            title=f"{command.name.capitalize()} command",
            description=f"Usage:\n`{Config.prefix}{cat}{command.usage}`\n{command.description}\n\nContributors for this command```Commits  User\n{data}```",
        )

        await message.channel.send(embed=embed)

    async def execute(self, arguments, message) -> None:
        args = arguments[0].split(" ")
        if not len(args) or args[0] == "":
            return await self.category_help(message)
        prefixes = [i.prefix for i in self.manager.categories]
        if args[0] in prefixes:
            try:
                cmdobj = {
                    i.prefix: i for i in self.manager.categories if i.prefix is not None
                }[args[0]].commands_map()[args[1]]
                return await self.command_help(message, cmdobj)
            except KeyError:
                raise KeyError(f"Command {args[0]} {args[1]} not found")
            except IndexError:
                return await self.category_help(message, args[0])
        else:
            try:
                cmdobj = self.manager.get(args[0])
            except KeyError:
                try:
                    cmdobj = [
                        [c for c in i.commands if c.name == args[0]]
                        for i in self.manager.categories
                        if i.prefix is None
                    ]
                    cmdobj = [i for i in cmdobj if len(i) != 0][0][0]
                    return await self.command_help(message, cmdobj)
                except IndexError:
                    return await Logger.send_error(
                        f"Command '{args[0]}' not found", message
                    )
            return await self.command_help(message, cmdobj)

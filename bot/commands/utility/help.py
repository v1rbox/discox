from bot.config import Config, Embed
from bot.base import Command
import asyncio


class cmd(Command):
    """ Help command. """

    name = "help"
    usage = "help [*command]"
    description = "The command you just ran, shows a help embed."

    async def execute(self, arguments, message) -> None:
        categories = self.manager.categories

        if len(arguments) == 0 or arguments[0] == "":
            msg = await message.channel.send("Loading...")
            for i in ['◀️', '🔼', '🔽', '▶️', '🔍']:
                await msg.add_reaction(i)

            page = 0
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
                    commands = categories[page-1].commands
                    name = categories[page-1].name 
                    cat_tag = categories[page-1].prefix
                    cat_tag = cat_tag + " " if cat_tag else ""

                indx = min(max(0, indx), len(commands)-1)

                embed = Embed(
                    title=f"{name} - Page {page+1} / {len(categories)+1}",
                    description=f"List of all commands and their description\nRun `{Config.prefix}{self.usage}` to get information about a specific command (still wip).\n\n",
                )
                embed.set_author(name=f"Help menu")

                for idx, command in zip(range(len(commands)), commands):
                    print(command, idx)
                    embed.description += f"`{Config.prefix}{cat_tag}{command.name}`\n" if indx != idx else f"**`{Config.prefix}{cat_tag}{command.usage}`**\n"
                    embed.description += f"{command.description.strip()}\n\n"

                await msg.edit(content="", embed=embed)

                def check(reaction, user):
                    return user == message.author and str(reaction.emoji) in ['◀️', '▶️', '🔼', '🔽', '🔍']

                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=120.0, check=check)
                except asyncio.TimeoutError:
                    await msg.clear_reactions()
                    return
                
                if str(reaction.emoji) == '◀️':
                    page -= 1
                elif str(reaction.emoji) == '▶️':
                    page += 1
                elif str(reaction.emoji) == '🔼':
                    indx -= 1
                elif str(reaction.emoji) == '🔽':
                    indx += 1
                elif str(reaction.emoji) == '🔍':
                    # Get the command object
                    if page == 0:
                        command = self.manager.commands[indx]
                        cat_tag = ""
                    else:
                        command = categories[page-1].commands[indx]
                        cat_tag = categories[page-1].prefix
                        cat_tag = cat_tag + " " if cat_tag else ""

                    data = await command.get_contribuders()

                    await msg.clear_reactions()
                    embed = Embed(title=f"{command.name.capitalize()} command", description=f"Usage:\n`{Config.prefix}{cat_tag}{command.usage}`\n{command.description}\n\nContributors for this command```Commits  User\n{data}```")
                    await msg.edit(content="", embed=embed)
                    await msg.add_reaction("↩️")

                    def check(reaction, user):
                        return user == message.author and str(reaction.emoji) in ['↩️']

                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=120.0, check=check)
                    except asyncio.TimeoutError:
                        await msg.clear_reactions()
                        return

                    await msg.clear_reactions()
                    for i in ['◀️', '🔼', '🔽', '▶️', '🔍']:
                        await msg.add_reaction(i)

                await reaction.remove(message.author)

        else:
            if len(arguments[0].split(" ")) == 1:
                cat = ""
                try:
                    cmd = self.manager.get(arguments[0])
                except KeyError:
                    raise KeyError(f"Command {arguments[0]} not found.")
            else:
                cat, command = arguments.split(" ")
                cmd = {i.prefix: i for i in self.manager.categories 
                          if i.prefix is not None}[cat] \
                          .commands_map()[command]

            data = await cmd.get_contribuders()

            embed = Embed(title=f"{cmd.name.capitalize()} command", description=f"Usage:\n`{Config.prefix}{cat}{cmd.usage}`\n{cmd.description}\n\nContributors for this command```Commits  User\n{data}```")

            await message.channel.send(embed=embed)

from bot.base import Command
from bot.config import Embed
import discord
from .__ui import PollButtons
class cmd(Command):
    name = "create"
    description = "Create a poll. Separate everything with commas. Question will be taken as the first argument. Description will be taken as the second argument (you can leave it alone with just give it blank value like this 'question,,a,b,c'). Else it is options."
    usage = "create <multiple_or_single> <*infos>"
    
    async def react_with_buttons(self, counts: int) -> None:
        return PollButtons(counts, self.when_clicked, self.when_timeout)
    
    async def when_clicked(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        cursor = await self.db.raw_exec_fetchone("SELECT * FROM polls WHERE message_id = ?", (interaction.message.id,))
    
    async def when_timeout(self, view: discord.ui.View) -> None:
        pass
    
    async def execute(self, arguments: list[str], message) -> None:
        arguments = arguments[0].split(",")
        question = arguments[0]
        assert question != "", "Question cannot be empty."
        assert len(arguments) > 2, "You need at least 2 options."
        description = arguments[1]
        options = arguments[2:]
        embed = Embed(title=question, description=description)
        embed.set_footer(text="Poll created by " + message.author.name)
        embed.set_thumbnail(url=message.author.avatar_url)
        for i in range(len(options)):
            embed.add_field(name=str(i), value=options[i], inline=False)
        view = None
        emoji = False
        if len(options) > 5:
            view = await self.react_with_buttons(len(options))
        elif len(options) > 10: 
            emoji = True
        msg = await message.channel.send(embed=embed, view=view)
        if emoji:
            for i in range(len(options)):
                await msg.add_reaction(str(i))
        else:
            await message.delete()
            raise NotImplementedError("Not implemented yet.")
        
from bot.config import Config, Embed
from bot.base import Command
import random

#rock paper scissor game
#self explanatory code
#contact @Chillax on discord for issues or @AhzDeveloperlol on github



class cmd(Command):
    """ A discord command instance. """

    name = "rps"
    usage = "rps <option>"
    description = "Play rock, paper, scissors with the bot."

    async def execute(self, arguments, message) -> None:
        option = arguments[0]
        rps = ['Rock', 'Paper', 'Scissors']
        bots_choice = random.choice(rps)
        if option == 'rock' and bots_choice == 'Paper':
            embed = Embed(title="Rock Paper Scissors", description=f"You choosed {option} and I choosed {bots_choice}")
            await message.channel.send("I win!", embed=embed)

        elif option == 'paper' and bots_choice == 'Rock':
            embed = Embed(title="Rock Paper Scissors", description=f"You choosed {option} and I choosed {bots_choice}")
            await message.channel.send("You win!", embed=embed)

        elif option == 'scissors' and bots_choice == 'Paper':
             embed = Embed(title="Rock Paper Scissors", description=f"You choosed {option} and I choosed {bots_choice}")
             await message.channel.send("You win!", embed=embed)

        elif option == 'paper' and bots_choice == 'Scissors':
            embed = Embed(title="Rock Paper Scissors", description=f"You choosed {option} and I choosed {bots_choice}")
            await message.channel.send("I win!", embed=embed)
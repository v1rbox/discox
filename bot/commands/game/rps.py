from bot.base import Command
from bot.config import Embed
import random # For the bot's choice.

# Rock paper scissors command.
# Pseudo-enum of the possible "choices"

# I probably should make these a cmd field but I'll keep them global
# because I can. THE BOYS
ROCK     = '🗿'
PAPER    = '📜'
SCISSORS = '✂️'

ROCK_NUM     = 0
PAPER_NUM    = 1
SCISSORS_NUM = 2

RPS_TABLE = {
    ROCK     : ROCK_NUM,
    PAPER    : PAPER_NUM,
    SCISSORS : SCISSORS_NUM,
}

RPS_TABLE_REVERSE = {
    ROCK_NUM    : ROCK,
    PAPER_NUM   : PAPER,
    SCISSORS_NUM: SCISSORS
}

class cmd(Command):
    # Our command instance.

    # I think having to type "v!rock-paper-scissors" every time
    # is kind of annoying.
    
    name = "rps"
    usage = "rps"
    description = "Play Rock Paper Scissors with the bot!"

    def won(self, player, opponent) -> bool:
        # Checks between integers to see which one has won.
        # We're really comparing 0, 1 and 2, and it sounds silly.
        # But it's RPS.
        if player == opponent:
            return None # Tie.

        if player == ROCK_NUM:
            return opponent == SCISSORS_NUM

        if player == PAPER_NUM:
            return opponent == ROCK_NUM

        if player == SCISSORS_NUM:
            return opponent == PAPER_NUM

        # I'm sure there is a better way to do this, but I'll keep it simple right now.

    def check_reaction(self, reaction, reactee: int, expected_reactee: int) -> int:
        if reactee != expected_reactee:
            # Keep in mind that reactee and expected_reactee are message IDs.
            return -1

        return RPS_TABLE.get(reaction.emoji)

    async def execute(self, arguments, message) -> None:
        # Before anything happens - choose the opponent's weapon.
        opponent_weapon = random.randint(ROCK_NUM, SCISSORS_NUM)
        embed = Embed(
            title="Rock Paper Scissors",
            
            # Yes, I did have to look up these emojis' code.
            description="""
            Choose your weapon! :crossed_swords:
            ------------------------------ 
            :moyai:    = Rock
            :scroll:   = Paper
            :scissors: = Scissors
            """
        )

        embed.set_color("red")
        
        embed_msg = await message.channel.send(embed=embed)
        # ILY Emojipedia.
        # Add emojis for the user's reaction.
        await embed_msg.add_reaction(ROCK)
        await embed_msg.add_reaction(PAPER)
        await embed_msg.add_reaction(SCISSORS)

        # Wait for user input (reaction)
        # It's a do-while loop
        # do {
        #   ...
        # } while (weapon == -1)
        while True:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=20, check=None)
            
            # Get the number (ROCK, PAPER, SCISSORS (0, 1, 2))
            # Type-hinting it to make it clear that we are returning an
            # integer.
            weapon: int = self.check_reaction(reaction, reaction.message.id, embed_msg.id)
            
            if weapon != -1:
                break

        await embed_msg.clear_reactions()

        if weapon == None:
            raise KeyError("Unexpected weapon - please choose a valid one.")
        
        player_won = self.won(weapon, opponent_weapon)
        # The new embed - after the user's choice
        new_embed = Embed(
            title="Rock Paper Scissors",
            description=f"""
            You chose {RPS_TABLE_REVERSE[weapon]}, I chose {RPS_TABLE_REVERSE[opponent_weapon]}.
            {'**You won!** :trophy:' if player_won else ("**I won!** :medal:" if player_won is not None else "**It's a tie!**")}
            """
        )

        new_embed.set_color("red")
        # Now edit the embed
        await embed_msg.edit(embed=new_embed)

        # Done.
        

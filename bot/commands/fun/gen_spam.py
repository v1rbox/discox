import math
import random

from bot.base import Command
from bot.config import Embed


class cmd(Command):
    """
    INFO: This is a spamming function. Very cool j4f.
    Original authors: imindMan + demir.
    """

    name = "gen_spam"
    usage = "gen_spam <algo> [spam_string]"
    description = (
        "Generate spamming messages. For fun. Type `v!gen_spam ? ?` for more help"
    )

    def general_spam(self, string: str):
        """This function will spam by squaring the string"""
        output = ""
        for i in range(len(string)):
            for j in range(len(string)):
                output += string
        return output

    def drill_spam(self, string: str, num: int):
        """This function is exactly the same as general_spam, but support random num"""
        output = ""
        for i in range(num):
            for j in range(num):
                output += string
        return output

    def addict_spam(self, string: str):
        # Generate a god number between 1000 to 3000
        rand_int = random.randint(10, 30)
        # Craziest algorithm ever
        """
            Algorithm generated when I was drunk

            Base on the len(string), let's call it l. With the rand_int can be called n
            We have the following output o 
            So, the algorithm is 
            (bullshit numbers)
            len(o) = round(sqrt(n) * l**3 * len(o) * 12281969*n)

            You may ask, what is the len(o) inside this algorithm means?
            The len(o) here means the "addicted length" of the output. It's hard to really understand it so let's take a look 
            at this example:
                We have a string "he", hence the output is "" (because we haven't updated the output yet)
                Now, we're gonna apply the algorithm, but, we haven't had the len(o) yet, so, this is where the computer will
                generate a bullshit number applying as a length of the output (the computer is drunk!). The bullshit number here
                isn't a random number, it will have a specific algorithm, based on the addicted stack frame of the program.

                By default, the addicted stack frame will look like this: [[], [], []] -- only 3 slots
                Computer will get the first addicted number - round(l * rand(0, 1989) * sqrt(l)). If the number is greater than 
                20009, the all the remained points of the result will be overflowed to the next slot, and then tracing the algorithm like that
                If 3 slots is all overflowed, then the computer will get the last remained overflowed points and apply as len(o). If it's enough to handle, then the computer will get 20009 - the current points inside the last filled slot = len(o)
            That's it! 
        """
        l = len(string)
        n = rand_int

        addicted_stack_frame = [[], [], []]
        len_o = round(l * random.randint(0, 1989) * math.sqrt(l))

        if len_o > 20009:
            addicted_stack_frame[0].append(20009)
            addicted_stack_frame[1].append(len_o - 20009)
            if addicted_stack_frame[1][0] > 20009:
                addicted_stack_frame[1].clear()
                addicted_stack_frame[1].append(20009)
                addicted_stack_frame[2].append(addicted_stack_frame[1][0] - 20009)
                if addicted_stack_frame[2][0] > 20009:
                    len_o = addicted_stack_frame[2][0] - 20009
                else:
                    len_o = 20009 - addicted_stack_frame[2][0]
            else:
                len_o = 20009 - addicted_stack_frame[1][0]
        else:
            len_o = 20009 - len_o

        final_len_o = round(math.sqrt(n) * l**3 * len_o * 12281969 * n)
        # main execution, the final_len_o will be shorten enuf

        final_len_o = int(str(final_len_o)[:2]) + 69  # why not?
        output = ""
        for i in range(final_len_o):
            output += string

        return output

    def literal_spam(self, string: str):
        # Generate spam till the end of the universe (message length limit)
        output = ""
        for x in range(0, 4000):
            output += string
        output = output[:4000]
        return output

    async def execute(self, arguments, message) -> None:
        if arguments[0] == "?" and arguments[1] == "?":
            await message.channel.send(
                """ ```Usage: v!gen_spam <algo> <spam_string>
This method supports a variety of cool algorithms you can choose:
    1. General spamming: (algo input: gen_spam).
            This is the basic algorithm to generate spam string.
                e.g: v!gen_spam gen_spam hi
    2. General spamming with "Drillenissen extra taste": (algo input: drill_spam_<rand-num>)
            This is also in general, but Drillenissen's taste for extra.
                e.g: v!gen_spam drill_spam_4 hi
    3. Addicted spam: this is the most craziest spamming algorithm. (algo input: addict_spam)
                e.g: v!gen_spam addict_spam hi
    4. Literal spam: spam till the end of message limit (algo input: literal_spam)
                e.g: v!gen_spam literal_spam Hehehe```
                    """
            )
            return
        if arguments[0] == "gen_spam":
            output = self.general_spam(arguments[1])
            await message.channel.send(output)

        elif arguments[0][:10] == "drill_spam" and len(arguments[0]) >= 12:
            output = self.drill_spam(arguments[1], int(arguments[0][11:]))
            await message.channel.send(output)

        elif arguments[0] == "addict_spam":
            output = self.addict_spam(arguments[1])
            await message.channel.send(output)

        elif arguments[0] == "literal_spam":
            output = self.literal_spam(arguments[1])
            await message.channel.send(output)

        else:
            embed = Embed(title="Invalid argument detected!")
            embed.set_color("red")
            await message.channel.send(embed=embed)

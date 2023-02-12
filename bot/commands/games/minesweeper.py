from bot.base import Command
from bot.config import Config, Embed

import random
import time
import discord
from queue import Queue


class MineButton(discord.ui.Button):
    def __init__(self,view):
        super().__init__()
        self.label="​"
        self.style=discord.ButtonStyle.primary

        self.board = view
        self.mine = False
        self.x = None
        self.y = None
        self.neighbors = []
        self.near_mines = 0
            
    
    #On Click
    async def callback(self,interaction):

        if self.board.player != interaction.user.id:
            return

        if self.board.moves == 0:
            self.board.assignButtons(self)

        self.board.moves += 1
        if self.mine:
            self.board.revealBoard()
            #Blast Emoji
            self.emoji = "💥"
            self.label = None
            for butt in self.board.butts:
                butt.disabled = True
            await interaction.message.edit(view=self.board)
            embed = Embed(title="Minesweeper",description=f"BOOM!!!\n {interaction.user.name} got rekt in {round(time.time()-self.board.start_time,1)} seconds using {self.board.moves} moves")
            await interaction.response.send_message(embed=embed)
            return

        else:
            self.board.clearSurroundingTiles(self)
            if self.board.remaining_tiles == self.board.mines:
                self.board.revealBoard()
                for butt in self.board.butts:
                    if butt.mine:
                        #Flag Emoji
                        butt.emoji = "🚩"
                        butt.label = None
                    butt.disabled = True
                await interaction.message.edit(view=self.board)
                embed = Embed(title="Minesweeper",description=f"Nice!\n {interaction.user.name} won in {round(time.time()-self.board.start_time,1)} seconds using {self.board.moves} moves")
                await interaction.response.send_message(embed=embed)
                return

        await interaction.message.edit(view=self.board)
        await interaction.response.defer()



class MineBoard(discord.ui.View):
    def __init__(self,mines,message):
        super().__init__()
        self.butts = []
        self.mines = mines
        self.moves = 0
        self.start_time = None
        self.grid = []
        self.player = message.author.id
        self.remaining_tiles = 25 
         
        #Creates Grid
        for y in range(5):
            row = []
            for x in range (5):
                butt = MineButton(self)
                butt.x = x
                butt.y = y
                self.butts.append(butt)
                self.add_item(butt)
                row.append(butt)
            self.grid.append(row)
    
    #Assigns mines afterwards to ensure you dont lose on the first click
    def assignButtons(self,initial_button):
        #Generates set of non repeating random numbers
        rand = set()
        #Mines variable must be 24 or less or it will be stuck forever in a while loop
        while len(rand) < self.mines:
            x = random.randint(0,4)
            y = random.randint(0,4)
            if x != initial_button.x or y != initial_button.y:
                rand.add((x,y))
        
        #Sets random mines
        for i in rand:
            self.grid[i[1]][i[0]].mine = True
        
        for butt in self.butts:
            self.getNeighbors(butt)

        #start timer once assigned
        self.start_time = time.time()

    def revealBoard(self):
        for butt in self.butts:
            if butt.mine:
                #Bomb Emoji
                butt.emoji = "💣"
                butt.label = None
            elif butt.near_mines > 0:
                butt.label = butt.near_mines

    def getNeighbors(self,button):
        coords = [
                {"x": button.x+1,  "y": button.y-1}, #top right 
                {"x": button.x,    "y": button.y-1}, #top middle 
                {"x": button.x-1,  "y": button.y-1}, #top left 
                {"x": button.x-1,  "y": button.y},   #left 
                {"x": button.x+1,  "y": button.y},   #right 
                {"x": button.x+1,  "y": button.y+1}, #bottom right 
                {"x": button.x,    "y": button.y+1}, #bottom middle 
                {"x": button.x-1,  "y": button.y+1}, #bottom left 
            ]
        for c in coords:
            try:
                if c["x"] > -1 and c["y"] > -1:
                    button.neighbors.append(self.grid[c["y"]][c["x"]])
            except IndexError:
                pass

        for n in button.neighbors:
            if n.mine:
                button.near_mines += 1
    

    def clearSurroundingTiles(self, button):
        q = Queue() 
        q.put((button))
        visited = set()
        button.disabled = True
        self.remaining_tiles -= 1
        if button.near_mines > 0:
            button.label = button.near_mines
            return
        while not q.empty():
            current = q.get()
            for butt in current.neighbors:
                if butt in visited:
                    continue
                if butt.mine:
                    visited.add(butt)
                    continue
                if butt.near_mines == 0:
                    q.put(butt)
                else:
                   butt.label = butt.near_mines
                if butt.disabled == False:
                    butt.disabled = True
                    self.remaining_tiles -= 1
                visited.add(butt)

class cmd(Command):
    """A discord command instance."""

    name = "minesweeper"
    usage = "minesweeper <number of mines>"
    description = "Minesweeper custom amount of mines"

    async def execute(self, arguments, message) -> None:
        try:
            int(arguments[0])
        except:
            embed = Embed(title="Minesweeper",description="Number of mines must be an int")
            await message.reply(embed=embed)
            return
        if int(arguments[0]) > 24:
            embed = Embed(title="Minesweeper",description="Number of mines must be smaller than 25")
            await message.reply(embed=embed)
            return
        embed = Embed(title="Minesweeper",description=f"Dont get rekt! {arguments[0]} mines have been placed!")
        await message.reply(embed=embed,view=MineBoard(int(arguments[0]),message))

 

from discord.ui import Button, View
import discord

class Yes(Button):
    def __init__(self, **kwargs):
        super().__init__(label="Yes", custom_id="yes", **kwargs, style=discord.ButtonStyle.green, emoji="✅")
        self.clicked = True
    async def callback(self, interaction: discord.Interaction):
        self.clicked = True
        
class No(Button):
    def __init__(self, **kwargs):
        super().__init__(label="No", custom_id="no", **kwargs, style=discord.ButtonStyle.red, emoji="❌")
        self.clicked = False
        
    async def callback(self, interaction: discord.Interaction):
        self.clicked = False
        
class OptionView(View):
    def __init__(self):
        super().__init__()
        self.yes = Yes()
        self.no = No()
        self.add_item(self.yes)
        self.add_item(self.no)
        
    async def get_answer(self):
        if not await self.wait(): # successfully waited
            return self.yes.clicked if self.yes.clicked else self.no.clicked
        return False
            
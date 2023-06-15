import discord


class Confirm(discord.ui.View):
    def __init__(self, intended: discord.Member | discord.User):
        super().__init__()
        self.value = None
        self.intended = intended

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user.id != self.intended.id:
            await interaction.response.send_message(
                "What are you doing here. This is not for you. ඞ", ephemeral=True
            )
            return
        await interaction.response.send_message("Confirming", ephemeral=True)
        self.value = True
        button.disabled = True
        self.cancel.disabled = True
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.intended.id:
            await interaction.response.send_message(
                "What are you doing here. This is not for you. ඞ", ephemeral=True
            )
            return
        await interaction.response.send_message("Cancelling", ephemeral=True)
        self.value = False
        button.disabled = True
        self.confirm.disabled = True
        self.stopper()

    def stopper(self):
        self.stop()

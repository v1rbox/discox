import typing

import discord


class Button(discord.ui.Button):
    def __init__(self, label: str, callback: typing.Awaitable[None]):
        self.label = label
        self.callback = callback
        super().__init__(label=label)


class PollButtons(discord.ui.View):
    def __init__(
        self,
        amounts: int,
        when_clicked: typing.Awaitable[None],
        when_timeout: typing.Awaitable[None],
    ):
        self.amounts = amounts
        super().__init__(timeout=None)  # do not
        self.on_click = when_clicked
        self.on_timeout = when_timeout
        for i in range(amounts):
            self.add_item(Button(label=str(i), callback=self.on_click))

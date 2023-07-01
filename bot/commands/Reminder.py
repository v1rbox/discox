from bot.base import Command

class Reminder:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reminders = {}

    async def on_message(self, message):
        if message.content.startswith("v!remind"):
            time_str, message = message.content.split(" ", 1)
            try:
                time_in_seconds = int(time_str)
            except ValueError:
                await message.channel.send("Please specify the time in seconds.")
                return

            reminder = {
                "time": time_in_seconds,
                "message": message,
            }
            self.reminders[message.author.id] = reminder
            await message.channel.send(f"I will remind you about {message} in {time_str} seconds.")

    async def on_ready(self):
        print("Reminder is ready!")

    async def run(self):
        await self.login()
        await self.start()

if __name__ == "__main__":
    bot = ReminderBot()
    bot.run()
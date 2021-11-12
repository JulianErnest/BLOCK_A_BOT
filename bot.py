# bot.py
import os
import discord

TOKEN = os.getenv('DISCORD_TOKEN')


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message: discord.Message):
        # * Stops the bot from replying to itself
        if message.author.id == self.user.id:
            return

        if message.content.starsWith('BA'):
            await message.reply(f"Hello ${message.author}")

client = MyClient()

client.run(os.environ['DISCORD_TOKEN'])
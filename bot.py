# bot.py
import os
import discord

TOKEN = os.getenv('DISCORD_TOKEN')


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message: discord.Message):
        if message.content.starsWith('BA'):
            channel = message.channel
            author = message.author.display_name
            await channel.send(f"Hello ${author}")

client = MyClient()

client.run(os.environ['DISCORD_TOKEN'])
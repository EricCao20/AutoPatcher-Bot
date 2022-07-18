#Start of Discord Bot - AutoPatcher

import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv()
#print(os.environ["BOT_TOKEN"])

#client = discord.Client()
bot = commands.Bot(command_prefix="$")

#@client.event
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command(name="start", help="I'm not sure yet, starts a timer?")
async def on_message(message):
    await message.send("Timer started")
    """
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    """
bot.run(os.environ["BOT_TOKEN"])



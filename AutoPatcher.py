#Start of Discord Bot - AutoPatcher

import os
#from tracemalloc import start
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
from matplotlib.pyplot import title

load_dotenv()
#print(os.environ["BOT_TOKEN"])

#client = discord.Client()
bot = commands.Bot(command_prefix="$")

#@client.event
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command(name="start", help="I'm not sure yet, starts a timer?")
async def timer_start(message):
    start_timer_embedd = discord.Embed(title="Timer start!", color = 0x7FFF00)
    end_timer_embedd = discord.Embed(title="Timer's up!", color = 0x7FFF00)
    await message.send(embed = start_timer_embedd)
    await asyncio.sleep(0.1)
    await message.send(embed = end_timer_embedd)
1
@bot.command(name="end", help="I'm not sure yet, ends a timer?")
async def timer_end(message):
    end_timer_embedd = discord.Embed(title="Timer's up!", color = 0xFF4040)

    await message.send(embed = end_timer_embedd)


    """
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    """
bot.run(os.environ["BOT_TOKEN"])



#Start of Discord Bot - AutoTicker

import discord
import os
from cogs.timer import Timer
from cogs.stock import Stock
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

#client = discord.Client(command_prefix="$",)
#intents = discord.Intents(messages=True, message_content = True)
bot = commands.Bot(command_prefix="$")

@bot.event
async def on_ready():

    print('We have logged in as {0.user}'.format(bot))

#@bot.command(name="help")

bot.add_cog(Stock(bot))

bot.add_cog(Timer(bot))

bot.run(os.environ["BOT_TOKEN"])



#Start of Discord Bot - AutoTicker, developed using yfinance 0.2.4, discord.py 1.7.3, pandas 1.4.4

import discord
import os
from cogs.timer import Timer
from cogs.stock import Stock
from cogs.game import Games
from dotenv import load_dotenv
from discord.ext import commands
#from cogs.general import Help

load_dotenv()

bot = commands.Bot(command_prefix="$")

@bot.event
async def on_ready():

    print('We have logged in as {}'.format(bot.user))

#bot.add_cog(Help(bot))

bot.add_cog(Stock(bot))

bot.add_cog(Games(bot))

bot.add_cog(Timer(bot))

bot.run(os.environ["BOT_TOKEN"])



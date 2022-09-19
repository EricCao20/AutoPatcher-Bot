#Start of Discord Bot - AutoTicker

import discord
import os
from cogs.timer import Timer
from cogs.stock import Stock
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

bot.add_cog(Timer(bot))

bot.run(os.environ["BOT_TOKEN"])



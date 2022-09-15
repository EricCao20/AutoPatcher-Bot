#Start of Discord Bot - AutoTicker

from email import message
from tabnanny import check
import yfinance as yf
import os
import discord
import asyncio
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

@bot.command(name="stock", help="Search up the price of a stock")
async def stock_price(ctx):
    stock_name = ""
    await ctx.send("What stock would you like to check?")
    def check_author(msg): 
        return msg.author == ctx.author and msg.channel ==ctx.channel #
    msg = await bot.wait_for("message", check=check_author, timeout=10)
    if msg.content.upper():
        stock_name += msg.content
        stock = yf.Ticker(stock_name)
        await ctx.send (stock.info["regularMarketPrice"])
    else:
        await ctx.send ("sorry you took too long!")

   # def stock_name(name):
   #     name = yf.Ticker("AMD")
    #await stock.send (stock.info["open"])

@bot.command(name="start", help="Starts a timer?")
async def timer_start(message):
    start_timer_embedd = discord.Embed(title="Timer start!", color = 0x7FFF00)
    end_timer_embedd = discord.Embed(title="Timer's up!", color = 0x7FFF00)
    await message.send(embed = start_timer_embedd)
    await asyncio.sleep(0.1) #maybe after starting the count down use import time to start counting and can use that to return the time left.
    await message.send(embed = end_timer_embedd)

@bot.command(name="end", help="Ends the current timer")
async def timer_end(message):
    end_timer_embedd = discord.Embed(title="Timer's up!", color = 0xFF4040)

    await message.send(embed = end_timer_embedd)

    """
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    """

@bot.command(name ="yallo")
async def test(message):
    print (message.author)
    await message.channel.send('@{.author}!'.format(message))
    await message.send("@")

#timer = time.clock()

bot.run(os.environ["BOT_TOKEN"])



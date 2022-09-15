#Start of Discord Bot - AutoTicker

from email import message
from tabnanny import check
from dotenv import load_dotenv
from discord.ext import commands
import yfinance as yf
import os
import discord
import asyncio

load_dotenv()
#print(os.environ["BOT_TOKEN"])

#client = discord.Client()
intents = discord.Intents(messages=True, message_content = True)
bot = commands.Bot(command_prefix="$", intents=intents)

#@client.event
@bot.event
async def on_ready():

    print('We have logged in as {0.user}'.format(bot))

@bot.command(name="price", help="Which stock would you like to search?")
async def stock_price(ctx):

    stock_name = ""
    await ctx.send("What stock would you like to check?")

    def check_author(msg): #this function checks to ensure that the following input will be from the same author in the same channel
        return msg.author == ctx.author and msg.channel == ctx.channel 

    msg = await bot.wait_for("message", check=check_author, timeout=10)

    if msg.content.upper():
        stock_name += msg.content.upper() # capitalize the user input as yf.Ticker output is a dictionary and keys are in all caps
        split = stock_name.split()
        ticker_name = yf.Ticker(split[0]) 
        
        # try using match split[0] instead of if statements when refactoring

        if msg.content.upper() == split[0] + " OPEN":
            await ctx.send (f"'{split[0]}' opened at ${ticker_name.info['regularMarketOpen']:.2f}")
            return

        if msg.content.upper() == split[0] + " CLOSE":
            await ctx.send (f"'{split[0]}' previously closed at ${ticker_name.info['previousClose']:.2f}")
            return

        else:
            await ctx.send (f"The price of '{split[0]}' is ${ticker_name.info['regularMarketPrice']:.2f}")

    else:
        await ctx.send ("sorry you took too long!")

@bot.command(name="start", help="Starts a timer")
async def timer_start(channel):
    await channel.send("How long would you like the timer to last?")

    def check_author(msg): #this function checks to ensure that the following input will be from the same author in the same channel
        return msg.author == channel.author and msg.channel == channel.channel 

    msg = await bot.wait_for("message", check=check_author, timeout=10)

    start_timer_embedd = discord.Embed(title="Timer start!", color = 0x7FFF00)
    end_timer_embedd = discord.Embed(title="Timer's up!", color = 0x7FFF00)
    await channel.send(embed = start_timer_embedd)
    await asyncio.sleep(int(msg.content)) #maybe after starting the count down use import time to start counting and can use that to return the time left.
    await channel.send(embed = end_timer_embedd)

@bot.command(name="end", help="COMMAND INCOMPLETE")
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



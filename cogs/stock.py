import asyncio
import discord
import yfinance as yf
from discord.ext import commands
from decimal import Decimal

#client = discord.Client()

class Stock(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.user_input = ""
        self.ticker = ""
        self.split = []
        self.stock_price = 0
        
    async def get_input(self, ctx, key):
        self.user_input = ""
        
        def check_author(msg): #this function checks to ensure that the following input will be from the same author in the same channel
            return msg.author == ctx.author and msg.channel == ctx.channel 

        try:

            msg = await self.bot.wait_for("message", check=check_author, timeout=10)

            if msg.content.upper()!= ("STOP"):
                self.user_input += msg.content.upper()
                self.split = self.user_input.split()
                self.ticker = yf.Ticker(self.split[0])
                self.stock_price = self.ticker.info[key]

            else:
                return await ctx.send("the command has been canceled")

        except asyncio.TimeoutError:
            return await ctx.send ("Sorry you took too long!")

        except:
            return await ctx.send ("Search has been canceled")
            
    @commands.command()
    async def price (self, ctx):
        stock_class = self.bot.get_cog('Stock')
        await ctx.send(f"{ctx.message.author}, what stock would you like to check?")
        await stock_class.get_input(ctx, "regularMarketPrice")
        await ctx.send (f"The price of '{self.split[0]}' is ${self.stock_price:.2f}")

    @commands.command()
    async def open (self, ctx):
        stock_class = self.bot.get_cog('Stock')
        await ctx.send(f"{ctx.message.author}, what stock would you like to check?")
        await stock_class.get_input(ctx, "regularMarketOpen")
        await ctx.send (f"'{self.split[0]}' last opened at ${self.stock_price:.2f}")

    @commands.command()
    async def close (self, ctx):
        stock_class = self.bot.get_cog('Stock')
        await ctx.send(f"{ctx.message.author}, what stock would you like to check?")
        await stock_class.get_input(ctx, "previousClose")
        await ctx.send (f"'{self.split[0]}' previously closed at ${self.stock_price:.2f}")

    @commands.command()
    async def higher(self, ctx):
        stock_class = self.bot.get_cog('Stock')
        await ctx.send(f"{ctx.message.author}, please input stock and price target, do not include a '$'.")
        await stock_class.get_input(ctx, "regularMarketPrice")
        await ctx.send("The alert has been set!")
        alert_price = float(self.split[1])
      
        while self.stock_price < alert_price:    # while the stock's price is less than the alert price                  #76.51    <    80  
            self.stock_price = self.ticker.info['regularMarketPrice']                                                       #price     split[1]                                        
            await asyncio.sleep(13)
            self.stock_price = 80
            print (alert_price)

        await ctx.send(f"{ctx.author.mention} your stock has reached or beaten the targeted price of ${alert_price:.2f}!")  

    @commands.command()
    async def lower(self, ctx):
        stock_class = self.bot.get_cog('Stock')
        await ctx.send(f"{ctx.message.author}, please input stock and price target, do not include a '$'.")
        await stock_class.get_input(ctx, "regularMarketPrice")
        await ctx.send("The alert has been set!")
        alert_price = float(self.split[1])

        while self.stock_price > float(alert_price):    # while the stock's price is greater than the alert price                  #76.51    >    80  
            self.stock_price = self.ticker.info['regularMarketPrice']                                                          #price     split[1]                                        
            await asyncio.sleep(13)
            self.stock_price = 70

        await ctx.send(f"{ctx.author.mention} your stock has reached or fallen below the targeted price of ${alert_price:.2f}!")  
        
    
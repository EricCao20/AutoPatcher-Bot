import asyncio
import discord
import yfinance as yf
from discord.ext import commands, tasks
from decimal import Decimal

class Stock(commands.Cog): # every command or function related to the value or information of the stocks are here

    def __init__(self, bot):
        self.bot = bot
        self.user_input = ""
        self.ticker_name = ""
        self.split = []
        self.ticker_price = 0
        self.tasks = []

    async def static_loop(self, *args):
        print(args)
    
    def task_launcher(self, *args, **interval):
        new_task = tasks.loop(**interval)(self.static_loop)
        new_task.start(*args)
        self.tasks.append(new_task)
    
    async def stock_input(self, ctx, key):
        self.user_input = ""
        self.ticker_name = ""
        self.split = []
        self.ticker_price = 0

        def check_author(msg): #this function checks to ensure that the following input will be from the same author in the same channel
            return msg.author == ctx.author and msg.channel == ctx.channel 

        try:
            msg = await self.bot.wait_for("message", check=check_author, timeout=10)

            if msg.content.upper()!= ("STOP"):
                self.user_input += msg.content.upper()
                self.split = self.user_input.split() 
                self.ticker_name = yf.Ticker(self.split[0])              # using a ticker that doesn't exist causes the dictonary when you do object.info to be 
                if self.ticker_name.info.get("regularMarketPrice") != None:  # {'regularMarketPrice': None, 'preMarketPrice': None, 'logo_url': ''} -- Cause of the none issue headache
                    print(self.split[0], key)
                    self.ticker_price = self.ticker_name.info.get(key)
                    print ("after if", self.ticker_price)

                else:
                    await ctx.send("You entered an invalid input.")
                    return self.ticker_price

            else:
                return await ctx.send("the command has been canceled.")

        except asyncio.TimeoutError:
            return await ctx.send ("Sorry you took too long!")

        except IndexError:
            return await ctx.send ("You did not enter an alert price.")

    @commands.command()
    async def price (self, ctx):
        stock_class = self.bot.get_cog('Stock')
        await ctx.send(f"{ctx.message.author}, what stock would you like to check?")
        await stock_class.stock_input(ctx, 'regularMarketPrice')
        print("reached here", self.ticker_price, self.split[0])
        if self.ticker_price != 0:
            await ctx.send (f"The price of '{self.split[0]}' is ${self.ticker_price:.2f}")

    @commands.command()
    async def open (self, ctx):
        stock_class = self.bot.get_cog('Stock')
        await ctx.send(f"{ctx.message.author}, what stock would you like to check?")
        await stock_class.stock_input(ctx, "regularMarketOpen")
        print("reached here", self.ticker_price, self.split[0])
        if self.ticker_price != 0:
            await ctx.send (f"'{self.split[0]}' last opened at ${self.ticker_price:.2f}")

    @commands.command()
    async def close (self, ctx): # returns the close price of the PREVIOUS trading session
        stock_class = self.bot.get_cog('Stock')
        await ctx.send(f"{ctx.message.author}, what stock would you like to check?")
        await stock_class.stock_input(ctx, "previousClose")
        print("reached here", self.ticker_price, self.split[0])
        if self.ticker_price != 0:
            await ctx.send (f"'{self.split[0]}' previously closed at ${self.ticker_price:.2f}")

    @commands.command()
    async def higher(self, ctx):
        global higher_loop

        try:
            stock_class = self.bot.get_cog('Stock')
            await ctx.send(f"{ctx.message.author}, please input stock and price target, do not include a '$'.")
            await stock_class.stock_input(ctx, "regularMarketPrice")

            @tasks.loop(seconds = 45.0)
            async def higher_loop(ctx, ticker, alert_price, stock_price):
                alert_price = float(alert_price)
                ticker = yf.Ticker(ticker)
                if stock_price < alert_price:    # while the stock's price is less than the alert price                  #76.51    <    80  
                    stock_price = ticker.info['regularMarketPrice']                                                   #price     split[1], input       
                    print (ticker)                                 
                    print (stock_price, alert_price)

                if stock_price >= alert_price:
                    await ctx.send(f"{ctx.author.mention} your stock has reached or beaten the targeted price of ${alert_price:.2f}!")  
                    higher_loop.cancel()
            
            if self.ticker_price != 0:
                await ctx.send("The alert has been set!")
                higher_loop.start(ctx, self.split[0], self.split[1], self.ticker_price)

        except RuntimeError:
            await ctx.send("A high alert has already been set.")

    @commands.command()
    async def lower(self, ctx):
        global lower_loop

        try:
            stock_class = self.bot.get_cog('Stock')
            await ctx.send(f"{ctx.message.author}, please input stock and price target, do not include a '$'.")
            await stock_class.stock_input(ctx, "regularMarketPrice")

            @tasks.loop(seconds = 45.0)
            async def lower_loop(ctx, ticker, alert_price, stock_price):
                alert_price = float(alert_price)
                ticker = yf.Ticker(ticker)
                
                if stock_price > alert_price:    # while the stock's price is less than the alert price                  #76.51    <    80  
                    stock_price = ticker.info['regularMarketPrice']                                                     #price     split[1], input                                        
                    print (stock_price, alert_price)

                if stock_price <= alert_price:
                    await ctx.send(f"{ctx.author.mention} your stock has reached or beaten the targeted price of ${alert_price:.2f}!")  
                    lower_loop.cancel()
            
            if self.ticker_price != 0:
                await ctx.send("The alert has been set!")
                lower_loop.start(ctx, self.split[0], self.split[1], self.ticker_price)
        
        except RuntimeError:
            await ctx.send("A low alert has already been set.")

    @commands.command()
    async def cancelhigher(self, ctx):
        higher_loop.cancel()
        await ctx.send("worked")

    @commands.command()
    async def cancellower(self, ctx):
        lower_loop.cancel()
        await ctx.send("worked")

from discord.ext import commands
import yfinance as yf
import asyncio

#client = discord.Client()

class Stock(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.stock_name = ""
        self.ticker_name = ""
        self.split = []
        self.stock_price = 0
        
    @commands.command()
    async def price(self, ctx):
        
        self.stock_name = ""
        await ctx.send("What stock would you like to check?")

        def check_author(msg): #this function checks to ensure that the following input will be from the same author in the same channel
            return msg.author == ctx.author and msg.channel == ctx.channel 

        try:
            msg = await self.bot.wait_for("message", check=check_author, timeout=10)
        
            if msg.content.upper() != ("STOP"):
                self.stock_name += msg.content.upper() # capitalize the user input as yf.Ticker output is a dictionary and keys are in all caps
                self.split = self.stock_name.split()
                self.ticker_name = yf.Ticker(self.split[0]) 

                if msg.content.upper() == self.split[0] + " OPEN":
                    await ctx.send (f"'{self.split[0]}' last opened at ${self.ticker_name.info['regularMarketOpen']:.2f}")
                    return

                elif msg.content.upper() == self.split[0] + " CLOSE":
                    await ctx.send (f"'{self.split[0]}' previously closed at ${self.ticker_name.info['previousClose']:.2f}")
                    return

                else:
                    await ctx.send (f"The price of '{self.split[0]}' is ${self.ticker_name.info['regularMarketPrice']:.2f}")
            else:
                return await ctx.send ("Search has been canceled.")

        except asyncio.TimeoutError:
            return await ctx.send ("Sorry you took too long!")

        except:
            return await ctx.send ("You entered an invaild stock.")
            

    #@commands.command()
    async def alert(self, ctx):
        self.stock_name = ""
        await ctx.send("Please input stock and price target, do not include a '$'.")

        def check_author(msg): #this function checks to ensure that the following input will be from the same author in the same channel
            return msg.author == ctx.author and msg.channel == ctx.channel 

        def check_bot(msg):
            return msg.author == self.bot and msg.channel == ctx.channel
        try:

            msg = await self.bot.wait_for("message", check=check_author, timeout=7)

            if msg.content.upper()!= ("STOP"):
                self.stock_name += msg.content.upper()
                self.split = self.stock_name.split()
                self.ticker_name = yf.Ticker(self.split[0])
                self.stock_price = self.ticker_name.info['regularMarketPrice']
                return self.stock_price
                """
                    elif price < float(split[1]):  #76.51   <    80
                        await ctx.send("smaller")
                        print("smaller")
                        break
                        """
                    #await self.bot.wait_for(price, check=check_bot)
            else:
                return await ctx.send("Alert placement has been canceled")

        except asyncio.TimeoutError:
            return await ctx.send ("Sorry you took too long!")

        except:
            return await ctx.send ("You entered an invaild stock.")

    @commands.command()
    async def higher(self, ctx):
        stock = self.bot.get_cog('Stock')
        await stock.alert(ctx)
        while True:
            self.stock_price = self.ticker_name.info['regularMarketPrice']

            if self.stock_price > float(self.split[1]):   #76.51    >    80  
                await ctx.send("bigger")  #price     split[1]
                print("bigger")
                break
        print(self.stock_price)

    @commands.command()
    async def lower(self, ctx):
        stock = self.bot.get_cog('Stock')
        await stock.alert(ctx)
        print(self.stock_price)
        
from discord.ext import commands
import yfinance as yf
import asyncio

#client = discord.Client()

class Stock(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def price(self, ctx):
        
        stock_name = ""
        await ctx.send("What stock would you like to check?")

        def check_author(msg): #this function checks to ensure that the following input will be from the same author in the same channel
            return msg.author == ctx.author and msg.channel == ctx.channel 

        try:
            msg = await self.bot.wait_for("message", check=check_author, timeout=7)
        
            if msg.content.upper() != ("STOP"):
                stock_name += msg.content.upper() # capitalize the user input as yf.Ticker output is a dictionary and keys are in all caps
                split = stock_name.split()
                ticker_name = yf.Ticker(split[0]) 

                if msg.content.upper() == split[0] + " OPEN":
                    await ctx.send (f"'{split[0]}' opened at ${ticker_name.info['regularMarketOpen']:.2f}")
                    return

                elif msg.content.upper() == split[0] + " CLOSE":
                    await ctx.send (f"'{split[0]}' previously closed at ${ticker_name.info['previousClose']:.2f}")
                    return

                else:
                    await ctx.send (f"The price of '{split[0]}' is ${ticker_name.info['regularMarketPrice']:.2f}")
            else:
                return await ctx.send ("Search has been canceled.")

        except asyncio.TimeoutError:
            return await ctx.send ("Sorry you took too long!")

        except:
            return await ctx.send ("You entered an invaild stock.")

    @commands.command()
    async def alert(self, ctx):
        stock_alert = ""
        price = 0
        await ctx.send("Please input stock and price target, do not include a '$'.")

        def check_author(msg): #this function checks to ensure that the following input will be from the same author in the same channel
            return msg.author == ctx.author and msg.channel == ctx.channel 

        def check_bot(msg):
            return msg.author == self.bot and msg.channel == ctx.channel
        try:

            msg = await self.bot.wait_for("message", check=check_author, timeout=7)

            if msg.content.upper() != ("STOP"):
                stock_alert += msg.content.upper()
                split = stock_alert.split()
                ticker_name = yf.Ticker(split[0])
                while True:
                    price = ticker_name.info['regularMarketPrice']

                    if price > float(split[1]):   #76.51    >    80  
                        await ctx.send("bigger")  #price     split[1]
                        print("bigger")
                        break

                    elif price < float(split[1]):  #
                        await ctx.send("smaller")
                        print("smaller")
                        break

                    #await self.bot.wait_for(price, check=check_bot)

        except:
            return await ctx.send("done")

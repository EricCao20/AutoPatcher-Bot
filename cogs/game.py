import asyncio
import random
import pandas as pd
import yfinance as yf
from discord.ext import commands
from cogs.stock import Stock
from pathlib import Path

class Games(commands.Cog):

    def __init__ (self, bot):
        self.bot = bot
        self.list_of_tickers = []
        self.ticker_name = ""
        self.ticker_price = 0
        self.historical_price = 0
        #self.balance = 10000

    def read_file (self, want_single_number): # randomly select a ticker from tickers.txt and get 3 months of close price data.
        self.ticker_name = ""

        with open ("tickers.txt", "r") as tickers:
            self.list_of_tickers = tickers.readlines()
            self.ticker_name = random.choice(self.list_of_tickers)
            self.ticker_name = self.ticker_name.splitlines() #.split("\n")

            historical_data = yf.download(self.ticker_name[0], period="3mo", interval="1d")
            historical_data['ticker'] = self.ticker_name[0]  # add this column because dataframe doesn't contain a column with the ticker
            historical_data.to_csv(f'GameCsv/ticker_{self.ticker_name[0]}.csv')  # ticker_AAPL.csv for example
            
            path = Path(f'GameCsv/ticker_{self.ticker_name[0]}.csv')
            dataframe = pd.concat([pd.read_csv(path)]) #have to send as a list

            if want_single_number == True:
                self.historical_price = dataframe.iloc[0,4]
                print (random.choice(dataframe.iloc[0,4]))

            else:
                self.historical_price = random.choice(dataframe.iloc[:,4])

    async def high_low_input(self, ctx): #use old price to compare to current one
        ticker = yf.Ticker(self.ticker_name)
        self.ticker_price = ticker.info.get(self.ticker_name)

        def check_author(msg): #this function checks to ensure that the following input will be from the same author in the same channel
            return msg.author == ctx.author and msg.channel == ctx.channel 

        try:
            msg = await self.bot.wait_for("message", check=check_author, timeout=10)

            if msg.content.upper() != ("STOP"):

                if msg.content.upper() == "H":
                    
                    if self.ticker_name > self.historical_price:
                        await ctx.send(f"You guessed right! the current price of '{self.ticker_name}' is greater than it was 3 months ago. (${self.ticker_name:.2f} > ${self.historical_price:.2f})")

                    else:
                        await ctx.send(f"Too bad! the current price of '{self.ticker_name}' is less than it was 3 months ago. (${self.ticker_name:.2f} < ${self.historical_price:.2f})")
                    
                elif msg.content.upper() == "L":
                    
                    if self.ticker_name < self.historical_price:
                        await ctx.send(f"You guessed right! the current price of '{self.ticker_name}' is less than it was 3 months ago. (${self.ticker_name:.2f} < ${self.historical_price:.2f})")
           
                    else:
                        await ctx.send(f"Too bad! the current price of '{self.ticker_name}' is greater than it was 3 months ago. (${self.ticker_name:.2f} > ${self.historical_price:.2f})")

                else:
                    return await ctx.send("You entered an invalid answer.")
            
            else:
                return await ctx.send("the command has been canceled.")

        except asyncio.TimeoutError:
            return await ctx.send ("Sorry you took too long!")

        except IndexError:
            return await ctx.send ("You did not enter an alert price.")

        else:
            return
            
    @commands.command()
    async def guessprice(self, ctx):
        games_class = self.bot.get_cog('Games')
        stock_class = self.bot.get_cog('Stock')
        historical_value = games_class.read_file(True)

        await ctx.send (f"The price of '{self.ticker_name}' 3 months ago was {historical_value}. Is the price now higher or lower? (h/l)") 

        def check_author(msg):      #this function checks to ensure that the following input will be from the same author in the same channel
            return msg.author == ctx.author and msg.channel == ctx.channel 

        try:
            msg = await self.bot.wait_for("message", check=check_author, timeout=10)

            if msg.content.upper()!= ("STOP"):
                return
                
            else:
                return await ctx.send("the command has been canceled.")

        except:
            return


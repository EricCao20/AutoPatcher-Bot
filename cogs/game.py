#WORK ON GUESS THE PRICE USING THE PERIOD DATA FROM TODAY AND ASKING USER IF ITS HIGHER OR LOWER THAN THE PRICE
import pandas as pd
import random
import yfinance as yf
from discord.ext import commands
from cogs.stock import Stock

class Games(commands.Cog):

    def __init__ (self, bot):
        self.bot = bot
        self.name_list = []
        self.ticker = ""
        #self.balance = 10000

    def read_file (self):
        self.ticker = ""

        with open ("ticker.txt", "r") as tickers:
            self.name_list = tickers.readlines()
            self.ticker = random.choice(self.name_list)
    
    @commands.command()
    async def higherlower(self, ctx):
        stock_class = self.bot.get_cog('Stock')




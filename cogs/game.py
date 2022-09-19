#WORK ON GUESS THE PRICE USING THE PERIOD DATA FROM TODAY AND ASKING USER IF ITS HIGHER OR LOWER THAN THE PRICE
import yfinance as yf
from discord.ext import commands
from cogs.stock import Stock
class Market(commands.Cog):

    def __init__ (self, bot):
        self.bot = bot
        #self.balance = 10000

    @commands.command()
    async def higherlower (self, ctx):
        return

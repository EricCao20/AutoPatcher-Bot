import asyncio
import altair as alt
import discord
import os
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from discord import Select
from discord.ext import commands
from pathlib import Path

class Plot (commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.user_input = ""
        self.ticker_name = ""
        self.split = []
        self.ticker_price = 0
        self.period = ""
        self.historical_price = 0

    async def plot_input(self, ctx):
        self.user_input = ""
        self.ticker_name = ""
        self.split = []
        self.ticker_price = None
        self.period = ""

        def check_author(msg): #this function checks to ensure that the following input will be from the same author in the same channel
            return msg.author == ctx.author and msg.channel == ctx.channel 

        try:
            msg = await self.bot.wait_for("message", check=check_author, timeout=10)

            if msg.content.upper()!= ("STOP"):
                self.user_input += msg.content.upper()
                self.split = self.user_input.split() 
                self.ticker_name = yf.Ticker(self.split[0])              # using a ticker that doesn't exist causes the dictonary when you do object.info to be 
                if self.ticker_name.info != None:  # {'regularMarketPrice': None, 'preMarketPrice': None, 'logo_url': ''} -- Cause of the none issue headache

                    historical_data = yf.download(self.ticker_name[0], period="3mo", interval="1d")
                    historical_data['ticker'] = self.ticker_name[0]  # add this column because dataframe doesn't contain a column with the ticker
                    historical_data.to_csv(f"GameCsv/ticker_{self.ticker_name[0]}.csv")  # ticker_AAPL.csv for example
                    
                    path = Path(f"GameCsv/ticker_{self.ticker_name[0]}.csv")
                    dataframe = pd.concat([pd.read_csv(path)]) #have to send as a list
                    self.historical_price = dataframe.iloc[0,4]
                    os.remove(f"GameCsv/ticker_{self.ticker_name[0]}.csv")
                    return self.historical_price
                    
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
    async def plot(self, ctx):
        plot_class = self.bot.get_cog('Plot')
        await ctx.send(f"{ctx.message.author}, which equities chart for what period would you like to see?")
        await plot_class.plot_input(ctx)


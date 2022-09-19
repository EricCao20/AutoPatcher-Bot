import discord
from discord.ext import commands
from cogs.stock import Stock

class Help(commands.Cog, commands.MinimalHelpCommand):

    def __init__ (self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embedd = discord.Embed(title = "AutoTicker Bot")
        embedd.add_field(name = "price"), embedd.add_field(name="open")
        await ctx.send(embed = embedd)


    
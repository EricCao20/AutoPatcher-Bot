from multiprocessing.dummy import active_children
import discord
import asyncio
from discord.ext import commands

class Foo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print ("Foo cog loaded")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game("Online"))
        print ("works good")

    @commands.command()
    async def random(self, ctx):
        await ctx.send("Face of Zed")

#def setup(bot):
#    bot.add_cog(Foo(bot))

#zed = Foo(25)

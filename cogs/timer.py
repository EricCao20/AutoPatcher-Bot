from multiprocessing.dummy import active_children
from time import time
import discord
import asyncio
from discord.ext import commands

class Timer(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game("Online"))

    @commands.command()
    async def timer_start(self, channel):
        await channel.send("How many minutes would you like the timer to last?")

        def check_author(msg): #this function checks to ensure that the following input will be from the same author in the same channel
            return msg.author == channel.author and msg.channel == channel.channel 
        try:

            msg = await self.bot.wait_for("message", check=check_author, timeout=10)

            time_value = (float(msg.content) * 60)
        
            start_timer_embedd = discord.Embed(title="Timer start!", color = 0x7FFF00)
            end_timer_embedd = discord.Embed(title="Timer's up!", color = 0x7FFF00)
            await channel.send(embed = start_timer_embedd)
            await asyncio.sleep(time_value) #maybe after starting the count down use import time to start counting and can use that to return the time left.
            await channel.send(f"{channel.author.mention} {end_timer_embedd}")
            await channel.send(embed = end_timer_embedd)
            
        except ValueError:
            await channel.send ("That's not a number...")
        
        except:
            await channel.send ("Sorry you took too long.")

    @commands.command()
    async def timer_end(self, channel):
        end_timer_embedd = discord.Embed(title="Timer's up!", color = 0xFF4040)
        await channel.send(embed = end_timer_embedd)

        """
        if message.author == bot.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')
        """
    @commands.command()
    async def dm (self, ctx):
        await ctx.author.send("face of zed")


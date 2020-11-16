"""
By Nihal - https://gist.github.com/Nihalgaming/7b2db40e6bd03d5cf4be39ec18d282e1
Please don't remove this i would love to be credited as the original creator.
Do suggest changes/fixes ;)
"""

import discord
from discord.ext import commands
import os
import random
import asyncio
import traceback
import sys

class admin(commands.Cog):


    def __init__(self, bot, *args, **Kwargs):
        self.bot = bot


    @commands.command(hidden = True)
    @commands.is_owner()
    async def pm(self ,ctx, member: discord.Member, *, content):

        try:
            channel = await member.create_dm()
            await channel.send(content)
            await ctx.send(f'Direct Message send to "{member}" with content "{content}"')
        except:
            await ctx.send('Some error occured :(')

    @commands.command(hidden = True)
    @commands.is_owner()
    async def guild_leave(self , ctx ):
        await ctx.send("Are you sure that you want me to leave from this guild?")
        message = ctx.message

        def is_correct(m):
            return m.author == message.author

        try:
            response = await self.bot.wait_for("message" , check=is_correct, timeout=5.0)
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you took too long")

        if response.content == "yes":
            await message.channel.send("Will miss you")
            await ctx.guild.leave()

        if response.content == "no":
            await ctx.send("Okai!")


    @commands.command(hidden = True)
    @commands.is_owner()
    async def say(self , ctx , * , content):
        await ctx.send(content)

    @commands.command(hidden = True)
    @commands.is_owner()
    async def mc(self , ctx , id = 0 , * , content):
        if id == 0:
            await ctx.send("Mention a channel id")

        try:
            channel = self.bot.get_channel(id)
            await channel.send(content)
            await ctx.message.add_reaction("\U00002705")
            return
        except:
            await ctx.message.add_reaction("\U0000274c")


    @commands.command(hidden = True)
    @commands.is_owner()
    async def sam(self , ctx , id = 0 , * , content):
        if id == 0:
            await ctx.send("Mention a channel id")
        try:
            channel = self.bot.get_channel(id)
            embed = discord.Embed(description=content)
            await channel.send(embed=embed)
            await ctx.message.add_reaction("\U00002705")
            return
        except:
            await ctx.message.add_reaction("\U0000274c")

    @commands.command(hidden = True)
    @commands.is_owner()
    async def reloadall(self, ctx):
        error_collection = []
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                name = file[:-3]
                try:
                    self.bot.reload_extension(f"cogs.{name}")
                except Exception as e:
                    await ctx.send(f"\U0000274c {e}")

        await ctx.send("\U00002705 Successfully reloaded all extensions")

    @commands.command(hidden = True)
    @commands.is_owner()
    async def reload(self, ctx , module):
        try:
            self.bot.reload_extension(f"cogs.{module}")
            await ctx.send(f"\U00002705 Successfully reloaded {module}")
        except Exception as e:
            await ctx.send(f"\U0000274c {e}")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, module):
        try:
            self.bot.load_extension(f'cogs.{module}')
            await ctx.send(f"\U00002705 Cog {module} loaded successfully")
        except Exception as e:
            await ctx.send(f"\U0000274c {e}")


    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx , module):
        try:
            self.bot.unload_extension(f'cogs.{module}')
            await ctx.send(f"\U00002705 Cog {module} unloaded successfully")
        except Exception as e:
            await ctx.send(f"\U0000274c {e}")

    @commands.command(aliases = ['name' , 'changename'] , hidden = True)
    @commands.is_owner()
    async def changenick(self, ctx, *, name: str):
        try:
            await ctx.guild.me.edit(nick=name)
            await ctx.send(f"Successfully changed username to **{name}**")
        except discord.HTTPException as err:
            await ctx.send(f"```{err}```")

    @commands.command(aliases = ['resetnick' , 'namereset'] , hidden = True)
    @commands.is_owner()
    async def nr(self, ctx,):
        try:
            await ctx.guild.me.edit(nick=None)
            await ctx.send(f"Successfully reseted the nickname")
        except discord.HTTPException as err:
            await ctx.send(err)


def setup(bot):
    bot.add_cog(admin(bot))
    print("Extenion admin is loaded")

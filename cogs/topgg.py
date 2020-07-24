import dbl
from discord.ext import commands
import os

dbl_token = os.getenv('DBL_TOKEN')
if dbl_token == None:
    dbl_token = input('Please enter the DBL Token:')

class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = dbl_token # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True) # Autopost will post your guild count every 30 minutes

    async def on_guild_post():
        print("Server count posted successfully")

def setup(bot):
    bot.add_cog(TopGG(bot))

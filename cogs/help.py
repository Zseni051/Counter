import discord
from discord.ext import commands
from datetime import datetime

client = discord.Client

class help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("help.py Loaded!")

    async def cog_check(self, ctx):
        try: 
            if not ctx.author.bot: return True
        except: pass

    

#####################################################################################################################################
def setup(client):
    client.add_cog(help(client))

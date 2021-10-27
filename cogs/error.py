from discord.ext import commands
from discord.ext.commands import CommandNotFound

from .functions import basic_embed

class error(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("error.py Loaded!")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
            if isinstance(error, CommandNotFound):
                return
            if self.client.user.id != 862604561515937813:
                raise error
                return
            channel = self.client.get_channel(902010999312379905)
            await channel.send(embed = await basic_embed(f"", f"```{error}```",self.client.Red,""))
            raise error

#####################################################################################################################################
def setup(client):
    client.add_cog(error(client))
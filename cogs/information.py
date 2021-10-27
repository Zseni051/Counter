import discord
from discord.ext import commands

from datetime import datetime
from typing import Optional

from discord import Embed, Member

from .functions import basic_embed

import psutil
import platform

class information(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("information.py Loaded!")

    async def cog_check(self, ctx):
        try: 
            if ctx.guild is not None and not ctx.author.bot: return True
        except: pass

############################################################## Bot Info #############################################################
    # tinvite
    @commands.command()
    async def invite(self, ctx):
        em = discord.Embed(title = "",
                           description = "",
                           colour = self.client.Blue,
                           timestamp=datetime.utcnow())
        admin_invitelink = f"[admin_perms](https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=8&scope=bot%20applications.commands)"
        choice_invitelink = f"[choose_perms](https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=4294967287&scope=bot%20applications.commands)"
        em.add_field(name= f"**Add {self.client.user.name}**", value = f"{admin_invitelink}\n{choice_invitelink}", inline=False)
        em.add_field(name= "**SupportServer**", value = "[here](https://discord.gg/E8DnTgMvMW)", inline=False)

        await ctx.send(embed = em)

    # tupvote
    @commands.command(aliases=['vote'])
    async def upvote(self, ctx):
        em = discord.Embed(title = "Upvote TimelyBot",
                           description = "",
                           colour = self.client.Blue,
                           timestamp=datetime.utcnow())
        em.set_thumbnail(url="https://emoji.gg/assets/emoji/BirdUpvote.gif")

        em.add_field(name= "__discordbotlist.com__", value = "[Upvote](https://discord.ly/timely-3816)", inline=False)
        em.add_field(name= "__voidbots.net__", value = "[Upvote](https://voidbots.net/bot/836198930873057290/)", inline=False)
        em.add_field(name= "Rewards", value = "-Double Points", inline=False)

        await ctx.send(embed = em)
    
    # ping pong (test latency)
    @commands.command()
    async def ping(self, ctx):
        em = discord.Embed(title = "<a:pingpongparrot:849455355222425630>Pong!",
                           description = f"Latency: {round(self.client.latency * 1000)}ms",
                           colour = self.client.Blue)
        t = await ctx.send(embed = em)

    # tinfo
    @commands.command(aliases=['bi'])
    async def info(self, ctx):
        memory_total = psutil.virtual_memory()._asdict()["total"]
        memory_used = psutil.virtual_memory()._asdict()["used"]
        cpu_percent = psutil.cpu_percent()

        shard_id = ctx.guild.shard_id
        shard = self.client.get_shard(shard_id)
        shard_servers_count = len([guild for guild in self.client.guilds if guild.shard_id == shard_id])
        shard_users_count = 0
        for guild in self.client.guilds:
            if guild.shard_id == shard_id:
                shard_users_count += len([m for m in guild.members if not m.bot])

        user_count = 0
        for x in self.client.guilds: user_count += len([m for m in x.members if not m.bot])

        Vars = [f"{round(memory_used/1000000000, 1)}/{round(memory_total/1000000000, 1)}GB",
                f"[admin_perms](https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=8&scope=bot%20applications.commands)",
                f"[choose_perms](https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=4294967287&scope=bot%20applications.commands)"]

        em = Embed(title=f"Bot Information - {self.client.user}",
                   description=f'{self.client.user.name} is an advanced counting bot which can manage a counting channel in your guild. With a simple setup, your channel is ready.',
                   colour=self.client.Blue)

        em.add_field(name=f"💠 Host", value=f"**OS**: `{platform.system()} ({platform.release()})`\n**Library**: `Pycord {discord.__version__}`\n**Memory Usage**: `{Vars[0]}`\n**CPU**: `{cpu_percent}%`", inline=True)
        em.add_field(name=f"🌀 Stats", value=f"**Owner**: <@!416508283528937472>\n**Guilds**: `{len(self.client.guilds)}`\n**Users**: `{user_count}`\n**Shard Count**: `{self.client.shard_count}`", inline=True)
        em.add_field(name=f"🔷 This Shard ({shard_id})", value=f"**Guilds**: `{shard_servers_count}`\n**Users**: `{shard_users_count}`\n**Ping**: `{round(shard.latency * 1000, 2)}ms`", inline=True)
        
        em.add_field(name=f"🌐 Links", value=f"**Invite me**: {Vars[1]}－{Vars[2]}\n**SupportServer**: https://discord.gg/E8DnTgMvMW", inline=False)

        em.set_footer(text=f"ID: {self.client.user.id}")
        em.timestamp = datetime.utcnow()
        await ctx.reply(embed = em,mention_author=False)

################################################################ Zseni ##############################################################
    # tcreator
    @commands.command(aliases=['zseni'])
    async def creator(self, ctx):
        user = await self.client.fetch_user(416508283528937472)
        em = discord.Embed(title = f"{user} is my creator.",
                           description = "Yep, i made the bot.",
                           colour = self.client.Blue,
                           timestamp=datetime.utcnow())
        em.set_thumbnail(url=user.avatar_url)

        em.add_field(name= "Youtube", value = f"[here]({self.client.youtube})", inline=True)
        em.add_field(name= "Discord", value = f"[here](https://discord.gg/SXng95f)", inline=True)
        em.add_field(name= "Twitter", value = f"[here](https://twitter.com/Zseni10)", inline=True)

        await ctx.send(embed = em)
    
#####################################################################################################################################
def setup(client):
    client.add_cog(information(client))
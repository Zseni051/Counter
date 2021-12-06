import discord
import json

from discord.ext import commands
from datetime import datetime
from discord import Embed

from .functions import user_avatar_url

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
    
    def cmd_aliases(command):
        with open("./json/help.json","r") as f: 
            help_json = json.load(f)
        return str(help_json[command]['aliases']).replace(f'{command}, ','').split(', ')

############################################################## Bot Info #############################################################
    # tinvite
    @commands.command(aliases=['support','server','links'])
    async def invite(self, ctx):
        user = ctx.author
        admin_invitelink = f"[admin_perms](https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=8&scope=bot%20applications.commands)"
        choice_invitelink = f"[choose_perms](https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=4294967287&scope=bot%20applications.commands)"
        
        em = discord.Embed(title = "",
                           description = "",
                           colour = self.client.Blue,
                           timestamp=datetime.utcnow())
        em.add_field(name= f"**Add {self.client.user.name}**", value = f"{admin_invitelink}\n{choice_invitelink}", inline=False)
        em.add_field(name= "**SupportServer**", value = "[here](https://discord.gg/E8DnTgMvMW)", inline=False)

        await ctx.reply(embed = em, mention_author=False)

    # tvote
    @commands.command(aliases=['upvote'])
    async def vote(self, ctx):
        em = discord.Embed(title = f"Vote for {self.client.user.name}",
                           description = "",
                           colour = self.client.Blue)
        em.set_thumbnail(url="https://emoji.gg/assets/emoji/BirdUpvote.gif")
        em.add_field(name= "**Rewards**", value = ":test_tube: Point multiplier", inline=False)
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label='dbl.com', url='https://discordbotlist.com/bots/counter-2122', style=discord.ButtonStyle.url))
        view.add_item(discord.ui.Button(label='VoidBots.net', url='https://voidbots.net/bot/862604561515937813/', style=discord.ButtonStyle.url))
        await ctx.reply(embed = em, mention_author=False, view = view)
    
    # ping pong (test latency)
    @commands.command(aliases=['ping'])
    async def latency(self, ctx):
        user = ctx.author
        shard = self.client.get_shard(ctx.guild.shard_id)
        em = discord.Embed(title = "<a:pingpongparrot:849455355222425630>Pong!",
                           description = f"**Latency**: {round(self.client.latency * 1000)}ms\n**Shard latency**: {round(shard.latency * 1000)}ms",
                           colour = self.client.Blue,
                           timestamp=datetime.utcnow())
        
        await ctx.reply(embed = em, mention_author=False)

    # tinfo
    @commands.command(aliases=['bi','info'])
    async def botinfo(self, ctx):
        user = ctx.author

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
                   description=f'{self.client.user.name} is an advanced counting bot that can manage a counting channel in your guild. With a simple setup, your channel is ready.',
                   colour=self.client.Blue,
                   timestamp = datetime.utcnow())
        em.set_footer(text="Requested by {}".format(user.name), icon_url = user_avatar_url(user))

        em.add_field(name=f"💠 Host", value=f"**OS**: `{platform.system()} ({platform.release()})`\n**Library**: `Pycord {discord.__version__}`\n**Memory Usage**: `{Vars[0]}`\n**CPU**: `{cpu_percent}%`", inline=True)
        em.add_field(name=f"🌀 Stats", value=f"**Owner**: <@!416508283528937472>\n**Guilds**: `{len(self.client.guilds)}`\n**Users**: `{user_count}`\n**Shard Count**: `{self.client.shard_count}`", inline=True)
        em.add_field(name=f"🔷 This Shard ({shard_id})", value=f"**Guilds**: `{shard_servers_count}`\n**Users**: `{shard_users_count}`\n**Ping**: `{round(shard.latency * 1000)}ms`", inline=True)
        em.add_field(name=f"🌐 Links", value=f"**Invite me**: {Vars[1]} - {Vars[2]}\n**SupportServer**: https://discord.gg/E8DnTgMvMW", inline=False)

        await ctx.reply(embed = em, mention_author=False)

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

        await ctx.reply(embed = em, mention_author=False)
    
#####################################################################################################################################
def setup(client):
    client.add_cog(information(client))
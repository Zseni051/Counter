import discord
from discord.ext import commands
from datetime import datetime

from .functions import user_avatar_url, page_button

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

    @commands.Cog.listener()
    async def on_message(self, ctx):
        p = str(self.client.serverprefix)
        content = str(ctx.content).lower()
        if not content.startswith(f"{p.lower()}help"): return 
        content = content.replace(f"{p.lower()}help ", "")
        iscmd = False
        # Check if `help <command>`
        for x in self.client.helpcmd: #Check is help command
            if content == x:
                iscmd = True
                break
            else: 
                if content in self.client.helpfile[x]['aliases'].split(', '):  #Check if is an aliase maybe
                    content = x
                    iscmd = True
                    break
        if iscmd == False: 
            # list of help commands
            def help_embed(self, page, arg):
                p = self.client.serverprefix
                description = f"• To get started with the bot, do `{p}setup`."
                description += f"\n• If you need help with a command, do `{p}help <command>`."
                description += f"\n• If you have any questions/queries feel free to join the [support server](https://discord.gg/E8DnTgMvMW)\n"
                for x in self.client.helpcmd[((page*8) - 8):(page*8)]: 
                    description += f"\n**[{x}]({self.client.youtube})**\n{self.client.Emojis['reply']}{self.client.helpfile[x]['desc_short']}"
                em = discord.Embed(title = "Counter Help",
                                description = description,
                               colour = self.client.Blue)
                em.set_footer(text=f"{p}help <command> to see more details－Page {page} of 2")
                return em
            await page_button(self, ctx, 1, 2, help_embed, None)
            return
        # help for each command in json file
        em = discord.Embed(title = f"{content.capitalize()}",
                           description = f"**Description:**\n{self.client.helpfile[content]['desc_long']}",
                           colour = self.client.Blue,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Usage**",value=f"`{p}{self.client.helpfile[content]['usage']}`", inline=False)
        em.add_field(name="**Aliases**",value=f"{self.client.helpfile[content]['aliases']}", inline=False)
        em.set_footer(text="Requested by {}".format(ctx.author.name), icon_url = user_avatar_url(ctx.author))
        await ctx.reply(embed = em, mention_author = False)



#####################################################################################################################################
def setup(client):
    client.add_cog(help(client))

import discord
from discord.ext import commands
from datetime import datetime

from .functions import basic_embed, user_avatar_url

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
        if not content.startswith(f"{p.lower()}help"):
            return
        content = content.replace(f"{p.lower()}help ", "")
        iscmd = False
        for x in self.client.help_json_cmds:
            if content == x:
                iscmd = True
                break
            else: 
                if content in self.client.help_json[x]['aliases'].split(', '): 
                    content = x
                    iscmd = True
                    break
        if iscmd == False:
            view = help_buttons(self)
            view.message = await ctx.reply(embed = help_embed(self, 1), mention_author = False, view = view)
            return
        em = discord.Embed(title = f"{content.capitalize()}",
                           description = f"**Description:**\n{self.client.help_json[content]['desc_long']}",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Usage**",value=f"`{p}{self.client.help_json[content]['usage']}`", inline=False)
        em.add_field(name="**Aliases**",value=f"{self.client.help_json[content]['aliases']}", inline=False)
        em.set_footer(text="Requested by {}".format(ctx.author.name), icon_url = user_avatar_url(ctx.author))
        await ctx.reply(embed = em, mention_author = False)

class help_buttons(discord.ui.View):
    def __init__(self, self2):
        super().__init__(timeout=5)
        self.self2 = self2
        self.page = 1
    
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)

    @discord.ui.button(emoji="<:arrow_left:903485598415876116>", style=discord.ButtonStyle.primary)
    async def left_arrow(self, buttons, interaction):
        self.page = self.page - 1
        if self.page == 0: self.page = 1 #min page
        if self.page == 3: self.page = 2 #max page
        await interaction.response.edit_message(embed = help_embed(self.self2, self.page), view = self)

    @discord.ui.button(emoji="<:arrow_right:903485554660868166>", style=discord.ButtonStyle.primary)
    async def right_arrow(self, buttons, interaction):
        self.page = self.page + 1
        if self.page == 0: self.page = 1 #min page
        if self.page == 3: self.page = 2 #max page
        await interaction.response.edit_message(embed = help_embed(self.self2, self.page), view = self)

def help_embed(self, page):
    p = self.client.serverprefix
    description = f"• To get started with the bot, do `{p}setup`."
    description += f"\n• If you need help with a command, do `{p}help <command>`."
    description += f"\n• If you have any questions/queries feel free to join the [support server](https://discord.gg/E8DnTgMvMW)\n"
    for x in self.client.help_json_cmds[((page*8) - 8):(page*8)]: 
        description += f"\n[**{x}**]({self.client.youtube})\n<:reply:897010400934105139>{self.client.help_json[x]['desc_short']}"
    em = discord.Embed(title = "Counter Help",
                    description = description,
                   colour = self.client.Green)
    em.set_footer(text=f"{p}help <command> to see more details－Page {page} of 2")
    return em

#####################################################################################################################################
def setup(client):
    client.add_cog(help(client))

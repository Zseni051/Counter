import discord
from discord.ext import commands
from datetime import datetime

from .functions import basic_embed, user_avatar_url

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

    # thelp
    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        view = help_buttons(self)
        view.message = await ctx.reply(embed = help_embed(self, 1), mention_author = False, view = view)

############################################################## Counting #############################################################
    # thelp setup
    @help.command()
    async def setup(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Setup",
                           description = "Setup a channel to be used for counting. The bot will replace the users message with a webhook version. This prevents users from editing their message or deleting it.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}setup`")
        em.set_footer(text="Requested by {}".format(ctx.author.name), icon_url = user_avatar_url(ctx.author))
        await ctx.reply(embed = em, mention_author = False)
    
    # thelp count
    @help.command()
    async def count(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Count",
                           description = "Returns your count and the fonts you own. You can obtain counts by counting which is then used to buy fonts.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}count [user]`")
        em.set_footer(text="Requested by {}".format(ctx.author.name), icon_url = user_avatar_url(ctx.author))
        await ctx.reply(embed = em, mention_author = False)
    
    # thelp buy
    @help.command()
    async def buy(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Buy",
                           description = "This command is used to buy a font from the shop.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}buy <font>`")
        em.set_footer(text="Requested by {}".format(ctx.author.name), icon_url = user_avatar_url(ctx.author))
        await ctx.reply(embed = em, mention_author = False)

    # thelp shop
    @help.command()
    async def shop(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Shop",
                           description = "Shows Fonts that are up for sale.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}shop`")
        em.set_footer(text="Requested by {}".format(ctx.author.name), icon_url = user_avatar_url(ctx.author))
        await ctx.reply(embed = em, mention_author = False)
    
    # thelp use
    @help.command()
    async def use(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Use",
                           description = "Select a font to use for when you count",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}use <font>`")
        em.set_footer(text="Requested by {}".format(ctx.author.name), icon_url = user_avatar_url(ctx.author))
        await ctx.reply(embed = em, mention_author = False)

############################################################## Settings #############################################################
    # thelp changeprefix
    @help.command()
    async def changeprefix(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Change Prefix",
                           description = "changes the prefx for the server.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}changeprefix <newprefix>`")
        em.set_footer(text="Requested by {}".format(ctx.author.name), icon_url = user_avatar_url(ctx.author))
        await ctx.reply(embed = em, mention_author = False)

############################################################## Bot Info #############################################################
    # thelp prefix
    @help.command()
    async def prefix(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Prefix",
                           description = "Returns the prefix for the server.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}prefix`")
        em.set_footer(text="Requested by {}".format(ctx.author.name), icon_url = user_avatar_url(ctx.author))
        await ctx.reply(embed = em, mention_author = False)
    
    # thelp ping (test latency)
    @help.command()
    async def ping(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Ping",
                           description = "Test latency of the bot's ping.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}ping`")
        em.set_footer(text="Requested by {}".format(ctx.author.name), icon_url = user_avatar_url(ctx.author))
        await ctx.reply(embed = em, mention_author = False)
    
    # thelp invite
    @help.command()
    async def invite(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "Invite links",
                           description = "Returns a link for the bot, its support server, and some other links",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}invite`")
        em.set_footer(text="Requested by {}".format(ctx.author.name), icon_url = user_avatar_url(ctx.author))
        await ctx.reply(embed = em, mention_author = False)
    
    # thelp upvote
    @help.command(aliases=['vote'])
    async def upvote(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = f"Upvote {self.client.user.name}",
                           description = "Gives you the link to upvote the bot in exchange for cool rewards",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}upvote`")
        em.add_field(name="**Aliases**",value=f"`{p}upvote`, `{p}vote`")
        em.set_footer(text="Requested by {}".format(ctx.author.name), icon_url = user_avatar_url(ctx.author))
        await ctx.reply(embed = em, mention_author = False)
    
    # thelp botinfo
    @help.command()
    async def botinfo(self, ctx):
        p = self.client.serverprefix
        em = discord.Embed(title = "BotInfo",
                           description = "Returns general and system information on the bot.",
                           colour = self.client.Green,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Syntax**",value=f"`{p}botinfo`")
        em.add_field(name="**Aliases**",value=f"`{p}botinfo`, `{p}bi`")
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
    commands = sorted(["setup", "count", "buy", "shop", "use", "changeprefix", "prefix", "ping", "invite", "upvote", "botinfo"])
    i = 0
    for x in commands: 
        i = i + 1
        if i > ((page*8) - 8) or page == 1:
            description += f"\n[**{x}**]({self.client.youtube})\n<:reply:897010400934105139>{self.client.help_json[x]['desc_short']}"
        if i == int(page*8): break

    em = discord.Embed(title = "Counter Help",
                    description = description,
                   colour = self.client.Green)
    em.set_footer(text=f"{p}help <command> to see more details－Page {page} of 2")
    return em

#####################################################################################################################################
def setup(client):
    client.add_cog(help(client))

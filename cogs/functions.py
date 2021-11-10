import discord
from datetime import datetime

def user_avatar_url(user):
    try: user_avatar_url = user.avatar.url
    except: user_avatar_url = "https://cdn.discordapp.com/embed/avatars/0.png"
    return user_avatar_url

def basic_embed(title, description,color, footer: str=""):
    em = discord.Embed(title = title,
                       description = description,
                       color = color)
    if footer is not None:
        em.set_footer(text=footer)
    em.timestamp = datetime.utcnow()
    return em

async def page_button(self, ctx, page, max, function, arg):
    view = page_buttons(self, page, max, function, arg)
    view.message = await ctx.reply(embed = function(self, page, arg), mention_author = False, view = view)
    return

class page_buttons(discord.ui.View):
    def __init__(self, self2, page, max, function, arg):
        super().__init__(timeout=5)
        self.self2 = self2
        self.page = page
        self.max = max
        self.function = function
        self.arg = arg
    
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)

    @discord.ui.button(emoji="<:arrow_left:903485598415876116>", style=discord.ButtonStyle.primary)
    async def left_arrow(self, buttons, interaction):
        self.page = self.page - 1
        if self.page < 1: 
            self.page = 1
            return
        if self.page > self.max: 
            self.page = self.max
            return
        await interaction.response.edit_message(embed = self.function(self.self2, self.page, self.arg), view = self)

    @discord.ui.button(emoji="<:arrow_right:903485554660868166>", style=discord.ButtonStyle.primary)
    async def right_arrow(self, buttons, interaction):
        self.page = self.page + 1
        if self.page < 1: 
            self.page = 1
            return
        if self.page > self.max: 
            self.page = self.max
            return
        await interaction.response.edit_message(embed = self.function(self.self2, self.page, self.arg), view = self)
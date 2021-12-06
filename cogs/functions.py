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

class View_Timeout(discord.ui.View):
    def __init__(self, timeout):
        super().__init__(timeout=timeout)
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)

class ButtonItem(discord.ui.Button):
    """Create a basic button.
    
    Function must look like:
        1: :code:`function(self, self2, interaction, arg)`
            2: :code:`do stuff here`
            3: :code:`return arg`"""
    def __init__(self, self2, emoji, function, arg):
        self.self2 = self2
        self.function = function
        self.arg = arg
        super().__init__(emoji=emoji, style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        self.arg = await self.function(self.self2, self, interaction, self.arg)

class DropdownItem(discord.ui.Select):
    """Create a basic dropdown menu.
    
    Function must look like:
        1: :code:`function(self, self2, interaction, arg)`
            2: :code:`do stuff here`
            3: :code:`return arg`"""
    def __init__(self, self2, placeholder, min, max, selects, function, arg):
        self.self2 = self2
        self.function = function
        self.arg = arg
        options = []
        for x in selects:
            options.append(discord.SelectOption(label=x))
        super().__init__(placeholder=placeholder, min_values=min, max_values=max, options=options)

    async def callback(self, interaction: discord.Interaction):
        self.arg = await self.function(self.self2, self, interaction, self.arg)
import discord
import math
from discord.ext import commands
from datetime import datetime

from .functions import View_Timeout, ButtonItem, DropdownItem, user_avatar_url

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
    @commands.command()
    async def help(self, ctx, command: str="na"):
        async def help_embed(self, self2, interaction, arg):
            if self2 is not None: #Exclude first run
                    if str(self2.emoji) == str(self.client.Emojis['arrow_left2']):
                        arg[0] = 1
                    if str(self2.emoji) == str(self.client.Emojis['arrow_left']):
                        if arg[0] != 1: 
                            arg[0] = arg[0] - 1
                    if str(self2.emoji) == str(self.client.Emojis['arrow_right']):
                        if arg[0] != arg[1]: 
                            arg[0] = arg[0] + 1
                    if str(self2.emoji) == str(self.client.Emojis['arrow_right2']):
                        arg[0] = arg[1]
            description = f"\n• If you need help with a command, do `{p}help <command>`."
            description += f"\n• If you have any questions/queries feel free to join the [support server](https://discord.gg/E8DnTgMvMW)\n"
            for x in arg[2][((arg[0]*8) - 8):(arg[0]*8)]: 
                description += f"\n**[{x}]({self.client.youtube})**\n{self.client.Emojis['reply_2']}{self.client.helpfile[x]['desc_short']}"
            em = discord.Embed(title = "Timely Help",
                               description = description,
                               colour = self.client.Blue)
            em.set_footer(text=f"{p}help <command> to see more details－Page {arg[0]} of {arg[1]}")
            if interaction is None: view.message = await ctx.reply(embed=em, mention_author = False, view = view)
            else: await interaction.response.edit_message(embed=em)
            return arg

        p = self.client.serverprefix
        cmd = False
        if command != "na":
            command = str(command).lower()
            for x in self.client.helpfile: #Check is a command
                if command == x: 
                    cmd = x
                    break
                else: #Check if is an aliase
                    if command in self.client.helpfile[x]['aliases'].split(', '):
                        cmd = x
                        break
        if cmd == False:
            arg = [1, math.ceil(len(self.client.helpfile)/8), self.client.helpcmd]
            view = View_Timeout(10)
            view.add_item(ButtonItem(self, f"{self.client.Emojis['arrow_left2']}", help_embed, arg))
            view.add_item(ButtonItem(self, f"{self.client.Emojis['arrow_left']}", help_embed, arg))
            view.add_item(ButtonItem(self, f"{self.client.Emojis['arrow_right']}", help_embed, arg))
            view.add_item(ButtonItem(self, f"{self.client.Emojis['arrow_right2']}", help_embed, arg))
            await help_embed(self, None, None, arg)
            return
        
        em = discord.Embed(title = f"{cmd.capitalize()}",
                           description = f"**Description:**\n{self.client.helpfile[cmd]['desc_long']}",
                           colour = self.client.Blue,
                           timestamp=datetime.utcnow())
        em.add_field(name="**Usage:**",value=f"`{p}{self.client.helpfile[cmd]['usage']}`", inline=False)
        em.add_field(name="**Aliases:**",value=f"{self.client.helpfile[cmd]['aliases']}", inline=False)
        try: em.add_field(name="**Cooldown:**",value=f"{self.client.helpfile[cmd]['cooldown']}", inline=False)
        except: pass
        em.set_footer(text="Requested by {}".format(ctx.author.name), icon_url = user_avatar_url(ctx.author))
        await ctx.reply(embed=em, mention_author=False)



#####################################################################################################################################
def setup(client):
    client.add_cog(help(client))

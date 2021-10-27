import asyncio
import discord
import json

from discord.ext import commands
from discord import Webhook
from datetime import datetime
from typing import Optional
from discord import Member

from .functions import basic_embed

class counting(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("counting.py Loaded!")
    
    async def cog_check(self, ctx):
        try: 
            if ctx.guild is not None and not ctx.author.bot: return True
        except: pass

    # tsetupcounting
    @commands.command()
    async def setup(self, ctx):
        if not ctx.author.guild_permissions.administrator:
            await ctx.reply(embed = await basic_embed(f"", f"{self.client.Emojis['danger']} You are missing the permission `administrator`.",self.client.Red,""))
            return

        #Setup Vars
        guild = ctx.guild
        channel = ctx.channel
        user = ctx.author
        cluster = self.client.mongodb["Counting"]["Main"]
        insert = False
        
        guilds = cluster.find_one({"channel": channel.id})
        if guilds is not None: #if command was sent in an active counting channel
            return

        embed_field1 = [f"{self.client.Emojis['cogs']} **Setting up counting.**",
                        f"{self.client.Emojis['empty_checkbox']} Channel: NA",
                        f"{self.client.Emojis['empty_checkbox']} Starting number: NA",
                        f"{self.client.Emojis['empty_checkbox']} Interval: NA",
                        f"{self.client.Emojis['empty_checkbox']} Alternate: NA",
                        f"{self.client.Emojis['empty_checkbox']} Emoji: NA",
                        f"{self.client.Emojis['info']} Please reply with the desired **channel**."]
        response_timeout = f"{self.client.Emojis['danger']} Setup Canceled."
        message = await ctx.reply(embed = await basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n \n{embed_field1[6]}",self.client.Blue,f"15 secconds to respond"))
        try:
            #Channel
            def check(m):
                return m.channel == ctx.channel and m.author == user and len(m.channel_mentions) != 0
            try:
                response = await self.client.wait_for('message', check=check, timeout=15)
            except asyncio.TimeoutError:
                embed_field1[0] = f"{self.client.Emojis['static_cog']} **Counting Setup Canceled**"
                embed_field1[6] = f"{response_timeout}"
                await message.edit(embed = await basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n \n{embed_field1[6]}",self.client.Blue,f""))
                return
            await asyncio.sleep(0.25)
            await response.delete()
            channel = response.channel_mentions[0]

            guilds = cluster.find_one({"channel": channel.id})
            if guilds is None: insert = True
            elif channel.id == guilds["channel"]:
                embed_field1[6] = f"{self.client.Emojis['warning']} {channel.mention} has already been **set**.\n{self.client.Emojis['question_mark']} Remove counting from {channel.mention}? `[Yes/No]`"
                await message.edit(embed = await basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n \n{embed_field1[6]}",self.client.Blue,f"15 secconds to respond"))

                def check(m):
                    return m.channel == ctx.channel and m.author == user and m.content.lower() in ("yes","no")
                try:
                    response = await self.client.wait_for('message', check=check, timeout=15)
                except asyncio.TimeoutError:
                    embed_field1[0] = f"{self.client.Emojis['static_cog']} **Counting Setup Canceled**"
                    embed_field1[6] = f"{response_timeout}"
                    await message.edit(embed = await basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n \n{embed_field1[6]}",self.client.Blue,f""))
                    return
                if response.content.lower() != "yes":
                    await asyncio.sleep(0.25)
                    await response.delete()
                    embed_field1[0] = f"{self.client.Emojis['static_cog']} **Counting Setup Canceled**"
                    embed_field1[6] = f"{self.client.Emojis['danger']} Removement of counting from {channel.mention} is Canceled."
                    await message.edit(embed = await basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n \n{embed_field1[6]}",self.client.Blue,f""))
                cluster.delete_one({"channel": channel.id})
                await asyncio.sleep(0.25)
                await response.delete()
                embed_field1[0] = f"{self.client.Emojis['static_cog']}** Counting Setup**"
                embed_field1[6] = f"{self.client.Emojis['info']} Counting has been removed from {channel.mention}."
                await message.edit(embed = await basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n \n{embed_field1[6]}",self.client.Blue,f""))
                return

            #Starting number
            embed_field1[1] = f"{self.client.Emojis['marked_checkbox']} Channel: {channel.mention}"
            embed_field1[6] = f"{self.client.Emojis['info']} Please reply with the desired **starting number**."
            await message.edit(embed = await basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n \n{embed_field1[6]}",self.client.Blue,f"15 secconds to respond"))

            def check(m):
                if m.channel == ctx.channel and m.author == user:
                    if m.content[0] == "-" and m.content[1::].isdigit():
                        return True
                    else:
                        if m.content.isdigit():
                            return True
                return False
            try:
                response = await self.client.wait_for('message', check=check, timeout=15)
            except asyncio.TimeoutError:
                embed_field1[0] = f"{self.client.Emojis['static_cog']} **Counting Setup Canceled**"
                embed_field1[6] = f"{response_timeout}"
                await message.edit(embed = await basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n \n{embed_field1[6]}",self.client.Blue,f""))
                return
            await asyncio.sleep(0.25)
            await response.delete()
            starting_number = int(response.content)

            #Interval
            embed_field1[2] = f"{self.client.Emojis['marked_checkbox']} Starting number: {starting_number}"
            embed_field1[6] = f"{self.client.Emojis['info']} Please reply with the desired **Interval**."
            await message.edit(embed = await basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n \n{embed_field1[6]}",self.client.Blue,f"15 secconds to respond"))

            def check(m):
                if m.channel == ctx.channel and m.author == user:
                    if m.content[0] == "-" and m.content[1::].isdigit():
                        return True
                    else:
                        if m.content.isdigit():
                            return True
                return False
            try:
                response = await self.client.wait_for('message', check=check, timeout=15)
            except asyncio.TimeoutError:
                embed_field1[0] = f"{self.client.Emojis['static_cog']} **Counting Setup Canceled**"
                embed_field1[6] = f"{response_timeout}"
                await message.edit(embed = await basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n \n{embed_field1[6]}",self.client.Blue,f""))
                return
            await asyncio.sleep(0.25)
            await response.delete()
            interval = int(response.content)

            #Alternate
            embed_field1[3] = f"{self.client.Emojis['marked_checkbox']} Interval: {interval}"
            embed_field1[6] = f"{self.client.Emojis['info']} Please reply for **Alternate** with `[True/False]`."
            temp = f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n \n{embed_field1[6]}"
            await message.edit(embed = await basic_embed(f"", f"{temp}",self.client.Blue,f"15 secconds to respond"))

            def check(m):
                return m.channel == ctx.channel and m.author == user and m.content.lower() in ("true","false")
            try:
                response = await self.client.wait_for('message', check=check, timeout=15)
            except asyncio.TimeoutError:
                embed_field1[0] = f"{self.client.Emojis['marked_checkbox']} **Counting Setup Canceled**"
                embed_field1[6] = f"{response_timeout}"
                await message.edit(embed = await basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n \n{embed_field1[6]}",self.client.Blue,f""))
                return
            await asyncio.sleep(0.25)
            await response.delete()
            alternate = str(response.content).lower()

            #Emoji
            embed_field1[4] = f"{self.client.Emojis['marked_checkbox']} Alternate: {alternate}"
            embed_field1[6] = f"{self.client.Emojis['info']} Please reply for **Emoji** with `[True/False]`."
            await message.edit(embed = await basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n \n{embed_field1[6]}",self.client.Blue,f"15 secconds to respond"))

            def check(m):
                return m.channel == ctx.channel and m.author == user and m.content.lower() in ("true","false")
            try:
                response = await self.client.wait_for('message', check=check, timeout=15)
            except asyncio.TimeoutError:
                embed_field1[0] = f"{self.client.Emojis['marked_checkbox']} **Counting Setup Canceled**"
                embed_field1[6] = f"{response_timeout}"
                await message.edit(embed = await basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n \n{embed_field1[6]}",self.client.Blue,f""))
                return
            await asyncio.sleep(0.25)
            await response.delete()
            emoji = str(response.content).lower()


            #Completed setup
            embed_field1[0] = f"{self.client.Emojis['static_cog']} **Counting Setup**"
            embed_field1[5] = f"{self.client.Emojis['marked_checkbox']} Emoji: {emoji}"
            embed_field1[6] = f"{self.client.Emojis['green_check1']} Setup Complete."
            await message.edit(embed = await basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n \n{embed_field1[6]}",self.client.Blue,f""))

            #Update or insert values to MongoDB
            if insert == True:
                guilds = {"guild": guild.id, "channel": channel.id, "number": starting_number, "interval": interval, "alternate": alternate, "emoji": emoji,"last_user": user.id}
                cluster.insert_one(guilds)

            #Delete channel that cant be found in guild
            list_of_guild = cluster.find({"guild": guild.id})
            for x in list_of_guild:
                channel_id = x["channel"]
                found = False
                for xx in guild.channels:
                    if channel_id == xx.id:
                        found = True
                if found == False:
                    cluster.delete_one({"channel": channel_id})
        except:
            embed_field1[0] = f"{self.client.Emojis['static_cog']} **Counting Setup Canceled**"
            embed_field1[6] = f"{self.client.Emojis['danger']} an ERROR occurred."
            await message.edit(embed = await basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n \n{embed_field1[6]}",self.client.Blue,f""))

    #on_message counting
    @commands.Cog.listener()
    async def on_message(self, ctx):
        user = ctx.author
        try: user_avatar_url = user.avatar.url
        except: user_avatar_url = "https://cdn.discordapp.com/embed/avatars/0.png"
        channel = ctx.channel
        cluster = self.client.mongodb["Counting"]["Main"]
        channels = cluster.find_one({"channel": channel.id})

        # Check if it is the correct channel
        if channels is None: return
        # Check if its a bot
        if user.bot:
            # Filter out webhook from actualy bots
            if user not in list(filter(lambda m: m.bot, ctx.guild.members)):
                return
        await asyncio.sleep(0.25)
        new_number = channels["number"] + channels["interval"]
        # Check if its the correct number
        if ctx.content != str(new_number):
            await ctx.delete()
            return
        # Check if user was previous user
        if channels["alternate"] == "true":
            if channels["last_user"] == user.id:
                await ctx.delete()
                return

        #Delete original message
        await ctx.delete()
        
        # Get webhook
        webhook = ""
        found_webhook = False
        for x in await ctx.channel.webhooks():
            if x.user == self.client.user:
                webhook = x
                found_webhook = True
                break
        if found_webhook == False:
            webhook = await ctx.channel.create_webhook(name=self.client.user, avatar=None, reason=None)
        
        cluster_user = self.client.mongodb["Counting"]["User"]
        users = cluster_user.find_one({"id": user.id})

        # Send webhook
        if channels["emoji"] == "true":
            await webhook.send(content=f'{await convert_num2emoji(self, new_number, users["font"])}', username=f"{ctx.author.name}", avatar_url=user_avatar_url)
        else:
            await webhook.send(content=f'{new_number}', username=f"{ctx.author.name}", avatar_url=user_avatar_url)

        #update values for main
        cluster.update_one({"channel":channel.id},{"$set":{"number":new_number}})
        cluster.update_one({"channel":channel.id},{"$set":{"last_user":user.id}})
        
        #update values for user
        if users is None:
            users = {"id": user.id, "count": 1, "fonts": "Default", "font": "Default"}
            cluster_user.insert_one(users)
        cluster_user.update_one({"id": user.id},{"$set":{"count":users["count"]+1}})

    # tshop
    @commands.command()
    async def shop(self, ctx, page: int=1):
        page = 1
        data = self.client.Count_Emojis
        
        n = ""
        description = ""
        for name in ["Alarm_Clock","Blob","Rainbow","Black_Marker","Magenta","Minecraft","White"]: 
            description += f"{n}➤ **{name}** － [+{data[name]['Cost']}]({self.client.youtube})"
            description += f'\n{data[name]["Emoji_0"]}{data[name]["Emoji_1"]}{data[name]["Emoji_2"]}{data[name]["Emoji_3"]}{data[name]["Emoji_4"]}{data[name]["Emoji_5"]}{data[name]["Emoji_6"]}{data[name]["Emoji_7"]}{data[name]["Emoji_8"]}{data[name]["Emoji_9"]}'
            n = "\n\n"

        await ctx.send(embed= await basic_embed("Font Shop",description,self.client.Blue,f"Page: {page}"))

    # tcount <user>
    @commands.command()
    async def count(self, ctx, target: Optional[Member]):
        cluster = self.client.mongodb["Counting"]["User"]
        user = target or ctx.author
        try: user_avatar_url = user.avatar.url
        except: user_avatar_url = "https://cdn.discordapp.com/embed/avatars/0.png"
        users = cluster.find_one({"id": user.id})
        
        if users is None: 
            description = f"**Count:** [+0]({self.client.youtube})\n **Fonts:** [0]({self.client.youtube}) \nNone"
        else: 
            count_amt = users["count"]
            data = self.client.Count_Emojis
            if users["fonts"] == "Default":
                fonts = "None"
            else:
                n = ""
                fonts = ""
                for name in users["fonts"].split():
                    if name == "Default": 
                        fonts += f"{n}➤ **Default**\n0 1 2 3 4 5 6 7 8 9"
                    else:
                        fonts += f"{n}➤ **{name}**"
                        fonts += f'\n{data[name]["Emoji_0"]}{data[name]["Emoji_1"]}{data[name]["Emoji_2"]}{data[name]["Emoji_3"]}{data[name]["Emoji_4"]}{data[name]["Emoji_5"]}{data[name]["Emoji_6"]}{data[name]["Emoji_7"]}{data[name]["Emoji_8"]}{data[name]["Emoji_9"]}'
                    n = "\n\n"
            description = f"**Count:** [+{count_amt}]({self.client.youtube})\n **Fonts:** [{len(users['fonts'].split())}]({self.client.youtube}) \n{fonts}"

        em = discord.Embed(description=description,
                           color = self.client.Blue,
                           timestamp=datetime.utcnow())
        em.set_author(name=f"{user.name}'s count", icon_url = user_avatar_url)
        await ctx.reply(embed= em)

    # tbuy <font>
    @commands.command()
    async def buy(self, ctx, font: str="None"):
        command_syntax = f"Syntax: {self.client.serverprefix}countbuy <font>"
        font = font.lower() 
        if font not in ("white","minecraft","magenta","black_marker","alarm_clock","rainbow","blob"):
            await ctx.reply(embed = await basic_embed("", f"{self.client.Emojis['danger']} Not an existing font.",self.client.Red,f"{command_syntax}"))
            return
        try:
            font = font.split("_")
            font = f"{font[0].capitalize()}_{font[1].capitalize()}"
        except:
            font = font[0].capitalize()
        cluster = self.client.mongodb["Counting"]["User"]
        users = cluster.find_one({"id": ctx.author.id})
        
        if users is None: 
            await ctx.reply(embed = await basic_embed("", f"{self.client.Emojis['danger']} Insufficient balance.",self.client.Red,f"{command_syntax}"))
            return
        if font in users["fonts"]:
            await ctx.reply(embed = await basic_embed("", f"{self.client.Emojis['danger']} You already have this font.",self.client.Red,f"{command_syntax}"))
            return
        
        data = self.client.Count_Emojis
        if int(users["count"]) >= int(data[font]['Cost']):
            new_count_amt = int(users["count"]) - int(data[font]['Cost'])
            cluster.update_one({"id": ctx.author.id},{"$set":{"count": new_count_amt}})
            cluster.update_one({"id": ctx.author.id},{"$set":{"fonts": f"{users['fonts']} {font}"}})
            cluster.update_one({"id": ctx.author.id},{"$set":{"font": font}})
            await ctx.reply(embed = await basic_embed("Purchased", f"{ctx.author.mention} bought **{font}**\n**New count:** +{new_count_amt}",self.client.Blue,f"{command_syntax}"))
        else:
            await ctx.reply(embed = await basic_embed("", f"{self.client.Emojis['danger']} Insufficient balance.",self.client.Red,f"{command_syntax}"))

    # tuse <font>
    @commands.command()
    async def use(self, ctx, font: str="None"):
        command_syntax = f"Syntax: {self.client.serverprefix}countuse <font>"
        font = font.lower() 
        if font not in ("default","white","minecraft","magenta","black_marker","alarm_clock","rainbow","blob"):
            await ctx.reply(embed = await basic_embed("", f"{self.client.Emojis['danger']} Not an existing font.",self.client.Red,f"{command_syntax}"))
            return
        try:
            font = font.split("_")
            font = f"{font[0].capitalize()}_{font[1].capitalize()}"
        except:
            font = font[0].capitalize()
        cluster = self.client.mongodb["Counting"]["User"]
        users = cluster.find_one({"id": ctx.author.id})

        if users is None: 
            await ctx.reply(embed = await basic_embed("", f"{self.client.Emojis['danger']} You don't have this font.",self.client.Red,f"{command_syntax}"))
            return
        if font in users["fonts"]:
            cluster.update_one({"id": ctx.author.id},{"$set":{"font": font}})
            if font == "Default":
                await ctx.reply(embed = await basic_embed("Equipped!", f"You're now using the **Default** Font\n0 1 2 3 4 5 6 7 8 9",self.client.Blue,f"{command_syntax}"))
                return
            data = self.client.Count_Emojis
            emojis = f'{data[font]["Emoji_0"]}{data[font]["Emoji_1"]}{data[font]["Emoji_2"]}{data[font]["Emoji_3"]}{data[font]["Emoji_4"]}{data[font]["Emoji_5"]}{data[font]["Emoji_6"]}{data[font]["Emoji_7"]}{data[font]["Emoji_8"]}{data[font]["Emoji_9"]}'
            await ctx.reply(embed = await basic_embed("Equipped!", f"You're now using the font: **{font}**\n{emojis}",self.client.Blue,f"{command_syntax}"))
        else:
            await ctx.reply(embed = await basic_embed("", f"{self.client.Emojis['danger']} You don't have this font.",self.client.Red,f"{command_syntax}"))

#####################################################################################################################################
async def convert_num2emoji(self, number,emoji):
    data = self.client.Count_Emojis
    output = "+"
    if str(number)[0] == "-":
        number = str(number)[1::]
        output = "-"
    if emoji == "Default":
        return f"{output}{number}"
    for x in str(number):
        output += data[emoji][f'Emoji_{x}']
    return output

#####################################################################################################################################
def setup(client):
    client.add_cog(counting(client))

import asyncio
import discord

from discord.ext import commands
from datetime import datetime
from typing import Optional
from discord import Member

from .functions import basic_embed, user_avatar_url

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
            await ctx.reply(embed = basic_embed(f"", f"{self.client.Emojis['danger']} You are missing the permission `administrator`.",self.client.Red,""))
            return

        #Setup Vars
        guild = ctx.guild
        channel = ctx.channel
        user = ctx.author
        cluster = self.client.mongodb["Counting"]["Setup"]
        insert = False
        Emojis = self.client.Emojis
        
        guilds = cluster.find_one({"channel": channel.id})
        if guilds is not None: #if command was sent in an active counting channel
            return

        embed_field1 = [f"{Emojis['cogs']} **Setting up counting.**",
                        f"{Emojis['empty_checkbox_2']} **[Channel:]({self.client.youtube})** NA",
                        f"{Emojis['empty_checkbox_2']} **[Starting number:]({self.client.youtube})** NA",
                        f"{Emojis['empty_checkbox_2']} **[Interval:]({self.client.youtube})** NA",
                        f"{Emojis['empty_checkbox_2']} **[Alternate:]({self.client.youtube})** NA",
                        f"{Emojis['empty_checkbox_2']} **[Emoji:]({self.client.youtube})** NA",
                        f"{Emojis['empty_checkbox_2']} **[Talking:]({self.client.youtube})** NA",
                        f"{Emojis['empty_checkbox_2']} **[GameMode:]({self.client.youtube})** NA",
                        f"{Emojis['info']} Please reply with the desired **channel**."]
        response_timeout = f"{Emojis['danger']} Setup Canceled."
        message = await ctx.reply(embed = basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n{embed_field1[6]}\n{embed_field1[7]}\n \n{embed_field1[8]}",self.client.Blue,f"15 secconds to respond"))
        try:
            #Channel
            def check(m):
                return m.channel == ctx.channel and m.author == user and len(m.channel_mentions) != 0
            try:
                response = await self.client.wait_for('message', check=check, timeout=15)
            except asyncio.TimeoutError:
                embed_field1[0] = f"{Emojis['static_cog']} **Counting Setup Canceled**"
                embed_field1[8] = f"{response_timeout}"
                await message.edit(embed = basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n{embed_field1[6]}\n{embed_field1[7]}\n \n{embed_field1[8]}",self.client.Blue,f""))
                return
            await asyncio.sleep(0.25)
            await response.delete()
            channel = response.channel_mentions[0]

            guilds = cluster.find_one({"channel": channel.id})
            if guilds is None: insert = True
            elif channel.id == guilds["channel"]:
                embed_field1[8] = f"{channel.mention} has already been **set**.\nRemove counting from channel? `[Yes/No]`"
                await message.edit(embed = basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n{embed_field1[6]}\n{embed_field1[7]}\n \n{embed_field1[8]}",self.client.Blue,f"15 secconds to respond"))

                def check(m):
                    return m.channel == ctx.channel and m.author == user and m.content.lower() in ("yes","no")
                try:
                    response = await self.client.wait_for('message', check=check, timeout=15)
                except asyncio.TimeoutError:
                    embed_field1[0] = f"{Emojis['static_cog']} **Counting Setup Canceled**"
                    embed_field1[8] = f"{response_timeout}"
                    await message.edit(embed = basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n{embed_field1[6]}\n{embed_field1[7]}\n \n{embed_field1[8]}",self.client.Blue,f""))
                    return
                if response.content.lower() != "yes":
                    await asyncio.sleep(0.25)
                    await response.delete()
                    embed_field1[0] = f"{Emojis['static_cog']} **Counting Setup Canceled**"
                    embed_field1[8] = f"{Emojis['danger']} Removement of counting from {channel.mention} is Canceled."
                    await message.edit(embed = basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n{embed_field1[6]}\n{embed_field1[7]}\n \n{embed_field1[8]}",self.client.Blue,f""))
                cluster.delete_one({"channel": channel.id})
                await asyncio.sleep(0.25)
                await response.delete()
                embed_field1[0] = f"{Emojis['static_cog']}** Counting Setup**"
                embed_field1[8] = f"{Emojis['info']} Counting has been removed from {channel.mention}."
                await message.edit(embed = basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n{embed_field1[6]}\n{embed_field1[7]}\n \n{embed_field1[8]}",self.client.Blue,f""))
                return

            #Starting number
            embed_field1[1] = f"{Emojis['marked_checkbox_2']} **[Channel:]({self.client.youtube})** {channel.mention}"
            embed_field1[8] = f"{Emojis['info']} Please reply with the desired **starting number**."
            await message.edit(embed = basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n{embed_field1[6]}\n{embed_field1[7]}\n \n{embed_field1[8]}",self.client.Blue,f"15 secconds to respond"))

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
                embed_field1[0] = f"{Emojis['static_cog']} **Counting Setup Canceled**"
                embed_field1[8] = f"{response_timeout}"
                await message.edit(embed = basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n{embed_field1[6]}\n{embed_field1[7]}\n \n{embed_field1[8]}",self.client.Blue,f""))
                return
            await asyncio.sleep(0.25)
            await response.delete()
            starting_number = int(response.content)

            #Interval
            embed_field1[2] = f"{Emojis['marked_checkbox_2']} **[Starting number:]({self.client.youtube})** {starting_number}"
            embed_field1[8] = f"{Emojis['info']} Please reply with the desired **Interval**."
            await message.edit(embed = basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n{embed_field1[6]}\n{embed_field1[7]}\n \n{embed_field1[8]}",self.client.Blue,f"15 secconds to respond"))

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
                embed_field1[0] = f"{Emojis['static_cog']} **Counting Setup Canceled**"
                embed_field1[8] = f"{response_timeout}"
                await message.edit(embed = basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n{embed_field1[6]}\n{embed_field1[7]}\n \n{embed_field1[8]}",self.client.Blue,f""))
                return
            await asyncio.sleep(0.25)
            await response.delete()
            interval = int(response.content)

            #Alternate
            embed_field1[3] = f"{Emojis['marked_checkbox_2']} **[Interval:]({self.client.youtube})** {interval}"
            embed_field1[8] = f"{Emojis['info']} Please reply for **Alternate** with `[True/False]`."
            await message.edit(embed = basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n{embed_field1[6]}\n{embed_field1[7]}\n \n{embed_field1[8]}",self.client.Blue,f"15 secconds to respond"))

            def check(m):
                return m.channel == ctx.channel and m.author == user and m.content.lower() in ("true","false")
            try:
                response = await self.client.wait_for('message', check=check, timeout=15)
            except asyncio.TimeoutError:
                embed_field1[0] = f"{Emojis['marked_checkbox_2']} **Counting Setup Canceled**"
                embed_field1[8] = f"{response_timeout}"
                await message.edit(embed = basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n{embed_field1[6]}\n{embed_field1[7]}\n \n{embed_field1[8]}",self.client.Blue,f""))
                return
            await asyncio.sleep(0.25)
            await response.delete()
            alternate = str(response.content).lower()

            #Emoji
            embed_field1[4] = f"{Emojis['marked_checkbox_2']} **[Alternate:]({self.client.youtube})** {alternate.capitalize()}"
            embed_field1[8] = f"{Emojis['info']} Please reply for **Emoji** with `[True/False]`."
            await message.edit(embed = basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n{embed_field1[6]}\n{embed_field1[7]}\n \n{embed_field1[8]}",self.client.Blue,f"15 secconds to respond"))

            def check(m):
                return m.channel == ctx.channel and m.author == user and m.content.lower() in ("true","false")
            try:
                response = await self.client.wait_for('message', check=check, timeout=15)
            except asyncio.TimeoutError:
                embed_field1[0] = f"{Emojis['marked_checkbox_2']} **Counting Setup Canceled**"
                embed_field1[8] = f"{response_timeout}"
                await message.edit(embed = basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n{embed_field1[6]}\n{embed_field1[7]}\n \n{embed_field1[8]}",self.client.Blue,f""))
                return
            await asyncio.sleep(0.25)
            await response.delete()
            emoji = str(response.content).lower()

            #talking 
            embed_field1[5] = f"{Emojis['marked_checkbox_2']} **[Emoji:]({self.client.youtube})** {emoji.capitalize()}"
            embed_field1[8] = f"{Emojis['info']} Please reply for **Talking** with `[True/False]`."
            await message.edit(embed = basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n{embed_field1[6]}\n{embed_field1[7]}\n \n{embed_field1[8]}",self.client.Blue,f"15 secconds to respond"))

            def check(m):
                return m.channel == ctx.channel and m.author == user and m.content.lower() in ("true","false")
            try:
                response = await self.client.wait_for('message', check=check, timeout=15)
            except asyncio.TimeoutError:
                embed_field1[0] = f"{Emojis['marked_checkbox_2']} **Counting Setup Canceled**"
                embed_field1[8] = f"{response_timeout}"
                await message.edit(embed = basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n{embed_field1[6]}\n{embed_field1[7]}\n \n{embed_field1[8]}",self.client.Blue,f""))
                return
            await asyncio.sleep(0.25)
            await response.delete()
            talking = str(response.content).lower()

            #Gamemode
            embed_field1[6] = f"{Emojis['marked_checkbox_2']} **[Talking:]({self.client.youtube})** {talking.capitalize()}"
            embed_field1[8] = f"{Emojis['info']} Please reply for **GameMode** with `[None/TugOfWar]`."
            await message.edit(embed = basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n{embed_field1[6]}\n{embed_field1[7]}\n \n{embed_field1[8]}",self.client.Blue,f"15 secconds to respond"))

            def check(m):
                return m.channel == ctx.channel and m.author == user and m.content.lower() in ("none","tugofwar")
            try:
                response = await self.client.wait_for('message', check=check, timeout=15)
            except asyncio.TimeoutError:
                embed_field1[0] = f"{Emojis['marked_checkbox_2']} **Counting Setup Canceled**"
                embed_field1[8] = f"{response_timeout}"
                await message.edit(embed = basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n{embed_field1[6]}\n{embed_field1[7]}\n \n{embed_field1[8]}",self.client.Blue,f""))
                return
            await asyncio.sleep(0.25)
            await response.delete()
            gamemode = str(response.content).lower()

            #Completed setup
            embed_field1[0] = f"{Emojis['static_cog']} **Counting Setup**"
            embed_field1[7] = f"{Emojis['marked_checkbox_2']} **[GameMode:]({self.client.youtube})** {gamemode.capitalize()}"
            embed_field1[8] = f"{Emojis['green_check1']} Setup Complete."
            await message.edit(embed = basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n{embed_field1[6]}\n{embed_field1[7]}\n \n{embed_field1[8]}",self.client.Blue,f""))

            #Update or insert values to MongoDB
            if insert == True:
                guilds = {"guild": guild.id, "channel": channel.id, 
                          "number": starting_number, 
                          "interval": interval, 
                          "alternate": alternate, 
                          "emoji": emoji,
                          "last_user": user.id,
                          "talking": talking,
                          "gamemode": gamemode}
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
            embed_field1[0] = f"{Emojis['static_cog']} **Counting Setup Canceled**"
            embed_field1[8] = f"{Emojis['danger']} An **ERROR** occurred."
            await message.edit(embed = basic_embed(f"", f"{embed_field1[0]}\n \n{embed_field1[1]}\n{embed_field1[2]}\n{embed_field1[3]}\n{embed_field1[4]}\n{embed_field1[5]}\n{embed_field1[6]}\n{embed_field1[7]}\n \n{embed_field1[8]}",self.client.Blue,f""))

    # on_message counting
    @commands.Cog.listener()
    async def on_message(self, ctx):
        user = ctx.author
        channel = ctx.channel
        cluster = self.client.mongodb["Counting"]["Setup"]
        channels = cluster.find_one({"channel": channel.id})

        # Check if it is the correct channel
        if channels is None: return
        # Check if its a bot
        if user.bot:
            # Filter out webhook from actualy bots, so it doesnt delete its own message.
            if user not in list(filter(lambda m: m.bot, ctx.guild.members)):
                return
        await asyncio.sleep(0.25)
        new_number = channels["number"] + channels["interval"]
        new_number2 = ""
        if channels["gamemode"] == "tugofwar":
            new_number2 = channels["number"] - channels["interval"]
        # Check if its the correct number
        if new_number2 != "": 
            if str(ctx.content).startswith(str(new_number2)): new_number = new_number2
        if str(ctx.content).startswith(str(new_number)):
            if channels["talking"] == "false":
                if ctx.content != str(new_number):
                    await ctx.delete()
                    return
        else: 
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
        
        # Get values for user
        cluster_user = self.client.mongodb["Counting"]["User"]
        users = cluster_user.find_one({"id": user.id})
        if users is None:
            users = {"id": user.id, "count": 1, "fonts": "Default", "font": "Default"}
            cluster_user.insert_one(users)

        # Send webhook
        if len(str(new_number)) == len(ctx.content): content = ""
        else: content = f"**「**{ctx.content[len(str(new_number))::]}**」**"
        if channels["emoji"] == "true":
            await webhook.send(content=f'{convert_num2emoji(self, new_number, users["font"])}{content}', username=f"{ctx.author.name}", avatar_url = user_avatar_url(user))
        else:
            await webhook.send(content=f'{new_number}{content}', username=f"{ctx.author.name}", avatar_url = user_avatar_url(user))

        #update values for main
        cluster.update_one({"channel":channel.id},{"$set":{"number":new_number}})
        cluster.update_one({"channel":channel.id},{"$set":{"last_user":user.id}})
        
        #update values for user
        cluster_user.update_one({"id": user.id},{"$set":{"count":users["count"]+1}})

    # tchannel <channel>
    @commands.command()
    async def channel(self, ctx, channel: Optional[discord.TextChannel]):
        if channel is None:
            await ctx.reply(embed = basic_embed("", f"{self.client.Emojis['danger']} No channel mentioned.",self.client.Red,f""), mention_author=False)
            return
        cluster = self.client.mongodb["Counting"]["Setup"]
        channels = cluster.find_one({"channel": channel.id})
        if channels is None:
            await ctx.reply(embed = basic_embed("", f"{self.client.Emojis['danger']} Not a counting channel.",self.client.Red,f""), mention_author=False)
            return
        Emojis = self.client.Emojis
        e = [f"{Emojis['marked_checkbox_2']} **[Channel:]({self.client.youtube})** {channel.mention}",
            f"{Emojis['marked_checkbox_2']} **[Current number:]({self.client.youtube})** {str(channels['number']).capitalize()}",
            f"{Emojis['marked_checkbox_2']} **[Interval:]({self.client.youtube})** {str(channels['interval']).capitalize()}",
            f"{Emojis['marked_checkbox_2']} **[Alternate:]({self.client.youtube})** {str(channels['alternate']).capitalize()}",
            f"{Emojis['marked_checkbox_2']} **[Emoji:]({self.client.youtube})** {str(channels['emoji']).capitalize()}",
            f"{Emojis['marked_checkbox_2']} **[Talking:]({self.client.youtube})** {str(channels['talking']).capitalize()}",
            f"{Emojis['marked_checkbox_2']} **[GameMode:]({self.client.youtube})** {str(channels['gamemode']).capitalize()}"]
        description = f"{Emojis['static_cog']} **Counting Channel Info**\n \n"
        for x in e: description += f"{x}\n"
        em = discord.Embed(description=description, color=self.client.Blue, timestamp=datetime.utcnow())
        em.set_footer(text="Requested by {}".format(ctx.author.name), icon_url = user_avatar_url(ctx.author))
        await ctx.reply(embed = em)

    # tcount <user>
    @commands.command(aliases=['balance','bal'])
    async def count(self, ctx, target: Optional[Member]):
        def count_embed(self, page, arg):
            user = arg[1] or arg[0].author
            cluster = self.client.mongodb["Counting"]["User"]
            users = cluster.find_one({"id": user.id})
            fonts = f"**[Default]({self.client.youtube})**\n{self.client.Emojis['reply_2']}0 1 2 3 4 5 6 7 8 9\n"
            if users is None: 
                description = f"**Count:** [+0]({self.client.youtube})\n **Fonts:** [1]({self.client.youtube}) \n{fonts}"
            else: 
                count_amt = users["count"]
                data = self.client.CountEmojis
                if users["fonts"] == "Default": fonts = "None"
                else:
                    for name in users["fonts"].split():
                        if name != "Default":
                            fonts += f"**[{name}]({self.client.youtube})**"
                            fonts += f'\n{self.client.Emojis["reply_2"]}{data[name]["Emoji_0"]}{data[name]["Emoji_1"]}{data[name]["Emoji_2"]}{data[name]["Emoji_3"]}{data[name]["Emoji_4"]}{data[name]["Emoji_5"]}{data[name]["Emoji_6"]}{data[name]["Emoji_7"]}{data[name]["Emoji_8"]}{data[name]["Emoji_9"]}\n'
                description = f"**Count**: [+{count_amt}]({self.client.youtube})\n **Fonts**: [{len(users['fonts'].split())}]({self.client.youtube}) \n{fonts}"
            em = discord.Embed(description=description, color = self.client.Blue, timestamp=datetime.utcnow())
            em.set_author(name = f"{user.name}'s count", icon_url = user_avatar_url(user))
            em.set_footer(text = f"page: {page}")
            return em
        #await page_button(self, ctx, 1, 2, count_embed, [ctx, target]) # not enought fonts (not needed)
        await ctx.reply(embed = count_embed(self, 1, [ctx, target]), mention_author=False)

    # tshop
    @commands.command(aliases=['store','font','fonts'])
    async def shop(self, ctx, page: int=1):
        def shop_embed(self, page, arg):
            data = self.client.CountEmojis
            description = ""
            for name in self.client.CountEmojisFont: 
                description += f"**[{name}]({self.client.youtube})** - [+{data[name]['Cost']}]({self.client.youtube})"
                description += f'\n{self.client.Emojis["reply_2"]}{data[name]["Emoji_0"]}{data[name]["Emoji_1"]}{data[name]["Emoji_2"]}{data[name]["Emoji_3"]}{data[name]["Emoji_4"]}{data[name]["Emoji_5"]}{data[name]["Emoji_6"]}{data[name]["Emoji_7"]}{data[name]["Emoji_8"]}{data[name]["Emoji_9"]}\n'
            return basic_embed("Font Shop",description,self.client.Blue,f"Page: {page}")
        try: page = int(abs(page))
        except: page = 1
        max = 2
        if page > max: page = max
        #await page_button(self, ctx, page, max, shop_embed, None) # not enought fonts (not needed)
        await ctx.reply(embed = shop_embed(self, 1, None), mention_author=False)

    # tbuy <font>
    @commands.command(aliases=['purchase'])
    async def buy(self, ctx, font: str="None"):
        command_syntax = f"Syntax: {self.client.serverprefix}buy <font>"
        user = ctx.author
        font = font.replace("_"," ").title().replace(" ","_")
        if font not in self.client.CountEmojisFont:
            await ctx.reply(embed = basic_embed("", f"{self.client.Emojis['danger']} Not an existing font.",self.client.Red,f"{command_syntax}"), mention_author=False)
            return
        cluster = self.client.mongodb["Counting"]["User"]
        users = cluster.find_one({"id": user.id})

        if users is None: 
            await ctx.reply(embed = basic_embed("", f"{self.client.Emojis['danger']} Insufficient balance.",self.client.Red,f"{command_syntax}"), mention_author=False)
            return
        if font in users["fonts"]:
            await ctx.reply(embed = basic_embed("", f"{self.client.Emojis['danger']} You already have this font.",self.client.Red,f"{command_syntax}"), mention_author=False)
            return
        if int(users["count"]) >= int(self.client.CountEmojis[font]['Cost']):
            new_count_amt = int(users["count"]) - int(self.client.CountEmojis[font]['Cost'])
            cluster.update_one({"id": ctx.author.id},{"$set":{"count": new_count_amt}})
            cluster.update_one({"id": ctx.author.id},{"$set":{"fonts": f"{users['fonts']} {font}"}})
            cluster.update_one({"id": ctx.author.id},{"$set":{"font": font}})
            em = discord.Embed(title = "Purchased", 
                               description = f"{ctx.author.mention} bought **{font}**\n**New count:** +{new_count_amt}",
                               color = self.client.Blue,
                               timestamp=datetime.utcnow())
            em.set_footer(text="Requested by {}".format(user.name), icon_url = user_avatar_url(user))
            await ctx.reply(embed = em, mention_author=False)
        else:
            await ctx.reply(embed = basic_embed("", f"{self.client.Emojis['danger']} Insufficient balance.",self.client.Red,f"{command_syntax}"), mention_author=False)

    # tuse <font>
    @commands.command(aliases=['use'])
    async def equip(self, ctx, font: str="None"):
        command_syntax = f"Syntax: {self.client.serverprefix}countuse <font>"
        user = ctx.author
        font = font.replace("_"," ").title().replace(" ","_")
        if font not in str(self.client.CountEmojisFont):
            if font != "Default":
                await ctx.reply(embed = basic_embed("", f"{self.client.Emojis['danger']} Not an existing font.",self.client.Red,f"{command_syntax}"), mention_author=False)
                return
        cluster = self.client.mongodb["Counting"]["User"]
        users = cluster.find_one({"id": ctx.author.id})
        if users is None: 
            await ctx.reply(embed = basic_embed("", f"{self.client.Emojis['danger']} You don't have this font.",self.client.Red,f"{command_syntax}"), mention_author=False)
            return
        if font in str(users["fonts"]).split(" "):
            cluster.update_one({"id": ctx.author.id},{"$set":{"font": font}})
            if font == "Default":
                description = "You're now using the **Default** Font\n0 1 2 3 4 5 6 7 8 9"
            else:
                data = self.client.CountEmojis
                emojis = f'{data[font]["Emoji_0"]}{data[font]["Emoji_1"]}{data[font]["Emoji_2"]}{data[font]["Emoji_3"]}{data[font]["Emoji_4"]}{data[font]["Emoji_5"]}{data[font]["Emoji_6"]}{data[font]["Emoji_7"]}{data[font]["Emoji_8"]}{data[font]["Emoji_9"]}'
                description = f"You're now using the font: **{font}**\n{emojis}"
            em = discord.Embed(title = "Equipped!", description = description, color = self.client.Blue, timestamp=datetime.utcnow())
            em.set_footer(text="Requested by {}".format(user.name), icon_url = user_avatar_url(user))
            await ctx.reply(embed = em, mention_author=False)
        else:
            await ctx.reply(embed = basic_embed("", f"{self.client.Emojis['danger']} You don't have this font.",self.client.Red,f"{command_syntax}"), mention_author=False)

#####################################################################################################################################
def convert_num2emoji(self, number,emoji):
    number = str(number)
    data = self.client.CountEmojis
    output = "+"
    if number.startswith("-"):
        number = number[1::]
        output = "-"
    if emoji == "Default":
        return f"{output}{number}"
    for x in number:
        output += data[emoji][f'Emoji_{x}']
    return output

#####################################################################################################################################
def setup(client):
    client.add_cog(counting(client))

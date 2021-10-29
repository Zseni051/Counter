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

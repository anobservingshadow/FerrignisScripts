# bot.py
import os
import random
import discord
import re
import asyncio
from dotenv import load_dotenv
from shop_generator import weapon_shop

# 1
from discord.ext import commands

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
shopdict = {"weapon":weapon_shop}


# 2
bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name="shop")
async def gen_weaponshop(ctx,shoptype=None,shopsize="average",shopname="Unnamed Shop"):
    if shoptype == "weapon":
        if shopsize == "small":
            shopstring = await shopdict[shoptype](size=7,shopname=shopname)
        elif shopsize == "average":
            shopstring = await shopdict[shoptype](size=12,shopname=shopname)
        elif shopsize == "large":
            shopstring = await shopdict[shoptype](size=20,shopname=shopname)
        else:
            msg = "Apologies, your shop size is invalid. Please use either 'small', 'average', or 'large' to indicate the size of the shop."
            await ctx.channel.send(msg)
        await ctx.channel.send(shopstring)
    elif shoptype == None:
        msg = "Please enter a shop type. Currently supported shoptypes are: {}".format(", ".join(shopdict.keys()))
        await ctx.channel.send(msg)
    else:
        msg = "Apologies, there is no shop type such as {}. This command only supports the 'weapon' shop type currently.".format(str(shoptype))
        await ctx.channel.send(msg)

@bot.command(name="shutdown")
@commands.is_owner()
async def shutdown(ctx):
    await bot.logout()

bot.run(token)
import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
from config import cfg
from utils import Slapper

bot = commands.Bot(command_prefix=cfg["prefix"])
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PHToken = "92a95ab0a3f4d2de"
with open('zene.txt', 'r', encoding="utf8") as file:
    legjob_zene_list = file.read().split("\n\n")
with open('idle_statuses.txt', 'r', encoding="utf8") as file:
    statuses = file.read().split("\n")

print(statuses)

@bot.command(name='hal')
async def slap(ctx, *, reason: Slapper):
    await ctx.send(reason)


@bot.event
async def on_message(message):
    from eventhandlers import handle_on_message
    if message.author == bot.user:
        return
    await handle_on_message(bot, message)


@bot.command(name='captcha', description="random PH captcha")
async def captcha(ctx):
    from utils import get_captcha
    cimg = get_captcha(PHToken)
    await ctx.send(file=discord.File(cimg, 'geci.png'))


@bot.command(name='zene', description="random leg job zene idézet")
async def zene(ctx):
    await ctx.send(random.choice(legjob_zene_list))


@bot.command(name='arena', description="ketrecharc bunyo, hasznalat: {0}arena @user1 @user2 ...".format(cfg["prefix"]))
async def fight(ctx, *args):
    if len(args) == 0:
        return
    await ctx.send("a ketrec harc gyöz tese: {}".format(random.choice(args)))


@bot.command(name='say', description="bemondom ha irsz utana valamit")
async def captcha(ctx, *args):
    await ctx.send(' '.join(args))


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("bohoc kodom"))
    print("ready")


@bot.event
async def on_typing(channel, user, when):
    from eventhandlers import handle_on_typing
    await handle_on_typing(bot,channel,user,when,statuses)


bot.run(TOKEN)

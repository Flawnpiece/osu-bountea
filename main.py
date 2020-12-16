from config import discordToken, osuKey
import discord
from discord.ext import commands
from osuapi import OsuApi, ReqConnector
import requests
import os

connector = connector=ReqConnector()
osuapi = OsuApi(osuKey,connector=ReqConnector())

description = '''ex'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='.', description=description, intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def reload(ctx, name=None):
    if name:
        bot.reload_extension(f'commands.{name}')
    else:
        pass

for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        bot.load_extension(f'commands.{filename[:-3]}')


bot.run(discordToken)

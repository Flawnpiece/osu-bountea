from config import discordToken, osuKey
import discord
from discord.ext import commands
import osuapi

description = '''ex'''

intents = discord.Intents.default()
intents.members = True

# help_command=None
bot = commands.Bot(command_prefix='.', description=description, intents=intents)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)



bot.run(discordToken)

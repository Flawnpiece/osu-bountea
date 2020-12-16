from config import discordToken, osuKey
import discord
from discord.ext import commands
import osuapi

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
    print('------')

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def help(ctx):

    descriptionFormat = """ **Information commands** : ``info`` ``points`` ``map``
                            **Utilities commands** : ``osuset`` ``bounty`` ``score``

                            Do ``.help [command name]`` to get more information!

                        """
    embed = discord.Embed(description = descriptionFormat, color = discord.Color(0xFF748C))
    embed.set_author(name = "osu!bountea commands list!", icon_url = bot.user.avatar_url)
    embed.set_footer(text="Bot made by your local trackpad player")
    await ctx.send(embed=embed)



bot.run(discordToken)

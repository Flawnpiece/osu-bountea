import discord
from discord.ext import commands

def setup(bot):
    bot.add_cog(HelpCommands(bot))

class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self,ctx, arg=None):

        descriptionFormat = """ **Information commands** : ``info`` ``points`` ``map``
                                **Utilities commands** : ``osuset`` ``bounty`` ``score``

                                Do ``.help [command name]`` to get more information!

                            """
        embed = discord.Embed(description = descriptionFormat, color = discord.Color(0xFF748C))
        embed.set_author(name = "osu!bountea commands list!", icon_url = self.bot.user.avatar_url)
        embed.set_footer(text="Bot made by your local trackpad player")
        await ctx.send(embed=embed)

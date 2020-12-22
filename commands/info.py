import discord
from discord.ext import commands
import sqlite3
from main import osuapi
connection = sqlite3.connect('data/scoreInformation.db')
cursor = connection.cursor()

def setup(bot):
    bot.add_cog(information(bot))

class information(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["information"], description="Showcase the generic information about the current bounty", usage=".info")
    async def info(self,ctx):

        cursor.execute("SELECT * FROM genericInformation")
        databaseSection = cursor.fetchone()

        infoDescription = databaseSection[0]
        gamemode = databaseSection[1]
        mapID = databaseSection[2]
        pointBasedOn = databaseSection[3]

        res = osuapi.get_beatmaps(beatmap_id=mapID)


        descriptionFormat = (f"**Our current bounty is on a {gamemode} map where the points system is based on {pointBasedOn}.**\n\n"
                             f"**{infoDescription} Use ``.map`` to get specific information about the map!**\n")

        embed = discord.Embed(description = descriptionFormat, color = discord.Color(0xFF748C))
        embed.set_author(name = "Bounty information!", icon_url = self.bot.user.avatar_url)
        embed.set_image(url = res[0].cover_image)
        embed.set_footer(text="Good luck!")
        await ctx.send(embed=embed)

        connection.close()

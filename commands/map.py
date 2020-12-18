import discord
from discord.ext import commands
from main import osuapi


res = osuapi.get_beatmaps(beatmap_id=1315116)
beatmap = res[0]


def setup(bot):
    bot.add_cog(MapInfo(bot))

class MapInfo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def diffEmote(self,starRating):
        self.sr = starRating
        if self.sr < 2:
            return "Easy"
        elif self.sr < 2.70:
            return "Normal"
        elif self.sr < 4.00:
            return "Hard"
        elif self.sr < 5.30:
            return "Insane"
        elif self.sr < 6.50:
            return "Expert"
        elif self.sr >= 6.5:
            return "Expert+"
        return self.sr

    def lengthFormat(self, length):
        self.length = length
        min = self.length//60
        sec = self.length - min*60

        return "{}:{}".format(min,sec)


    @commands.command(aliases=["Map","maps"], description="Showcase all the information you need to know about the current bounty!", usage=".map")
    async def map(self,ctx):

        descriptionFormat = """ ✦ **{0} - {1}**

                                {11} - {2}
                                ▸ **Difficulty:** {3} ▸ **Length:** {4}
                                ▸ **BPM:** {5} ▸ **Max combo:** {6}

                                ▸ **AR:** {7} **OD:** {8} **HP:** {9} **CS:** {10}
                            """

        formattingElements = (beatmap.artist, beatmap.title, beatmap.version, round(beatmap.difficultyrating,2),
                              self.lengthFormat(beatmap.total_length), beatmap.bpm, beatmap.max_combo, beatmap.diff_approach,
                              beatmap.diff_overall, beatmap.diff_drain, beatmap.diff_size, self.diffEmote(beatmap.difficultyrating))

        embed = discord.Embed(description = descriptionFormat.format(*formattingElements), color = discord.Color(0xFF748C))
        embed.set_thumbnail(url = beatmap.cover_thumbnail)
        embed.set_author(name = "map information!", icon_url = self.bot.user.avatar_url)
        embed.set_footer(text="Bot made by your local trackpad player")
        await ctx.send(embed=embed)

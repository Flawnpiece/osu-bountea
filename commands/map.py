import discord
from discord.ext import commands
from main import osuapi

res = osuapi.get_beatmaps(beatmap_id=2542475)
beatmap = res[0]

'''for x,y in dict(res[0]).items():
    print(x,y)'''

def setup(bot):
    bot.add_cog(MapInfo(bot))

class MapInfo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def diffEmote(self,starRating):
        self.sr = starRating
        if self.sr < 2:
            return "<:easy:790701940022837278>"
        elif self.sr < 2.70:
            return "<:normal:790702199528488960>"
        elif self.sr < 4.00:
            return "<:hard:790702230075605032>"
        elif self.sr < 5.30:
            return "<:insane:790702257083252736>"
        elif self.sr < 6.50:
            return "<:expert:790702286799896586>"
        elif self.sr >= 6.5:
            return "<:expertplus:790702321545904148>"
        return self.sr

    def lengthFormat(self, length):
        self.length = length
        min = self.length//60
        sec = self.length - min*60

        return "{}:{}".format(min,sec)

    def statusOnDate(self,status,date):
        approvedStatus = {4:"Loved", 3:"Qualified", 2:"Approved", 1 : "Ranked", 0 : "Pending", -1 : "WIP", -2 :" Graveyard"}
        status = approvedStatus[status.value]

        return "{} on {}".format(status, date.date())

    @commands.command(aliases=["Map","maps"], description="Showcase all the information you need to know about the current bounty!", usage=".map")
    async def map(self,ctx):

        formattingElements = {"artist":beatmap.artist, "title":beatmap.title, "diffname":beatmap.version, "sr":round(beatmap.difficultyrating,2),
        "length":self.lengthFormat(beatmap.total_length), "bpm":beatmap.bpm, "maxcombo":beatmap.max_combo, "ar":beatmap.diff_approach,
        "od":beatmap.diff_overall, "hp":beatmap.diff_drain, "cs":beatmap.diff_size, "diffemote":self.diffEmote(beatmap.difficultyrating),
        "mapper":beatmap.creator,"mapsetID":beatmap.beatmapset_id,"mapID":beatmap.beatmap_id, "space1":" \u200B", "space2":"\u200B \u200B \u200B \u200B \u200B"}

        descriptionFormat = (f" ✦ [**{formattingElements['artist']} - {formattingElements['title']}**](https://osu.ppy.sh/beatmapsets/{formattingElements['mapsetID']}#osu/{formattingElements['mapID']})\n"
                            f"{formattingElements['space2']} [**| by {formattingElements['mapper']}**](https://osu.ppy.sh/beatmapsets/{formattingElements['mapsetID']}#osu/{formattingElements['mapID']}) \n\n"

                            f"{formattingElements['diffemote']}{formattingElements['space1']} - {formattingElements['diffname']}\n"
                            f"▸ **Difficulty:** {formattingElements['sr']}"
                            f"▸ **Length:** {formattingElements['length']}\n"
                            f"▸ **BPM:** {formattingElements['bpm']}"
                            f"▸ **Max combo:** {formattingElements['maxcombo']}\n\n"

                            f"▸ **AR:** {formattingElements['ar']} **OD:** {formattingElements['od']} **HP:** {formattingElements['hp']} **CS:** {formattingElements['cs']}")

        embed = discord.Embed(description = descriptionFormat, color = discord.Color(0xFF748C))
        embed.set_thumbnail(url = beatmap.cover_thumbnail)
        embed.set_author(name = "Bounty map information!", icon_url = self.bot.user.avatar_url)
        embed.set_footer(text=" {0} | {1} ♡".format(self.statusOnDate(beatmap.approved,beatmap.approved_date),beatmap.favourite_count) )
        await ctx.send(embed=embed)

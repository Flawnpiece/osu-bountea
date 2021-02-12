import discord
from discord.ext import commands
from main import osuapi, connection,cursor
import sqlite3


def setup(bot):
    bot.add_cog(BountyVerification(bot))

class BountyVerification(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def idVerification(self,ctx,playerName):
        returnVar = 0
        if isinstance(playerName,str):
            userID = playerName[3:-1]
            returnVar = 1
        else:
            userID = ctx.author.id
            returnVar = 2

        cursor.execute("SELECT * FROM osuset WHERE discord_id=?", (userID,))
        databaseSection = cursor.fetchone()

        #check if we got something out of the database
        if isinstance(databaseSection,tuple) == True:
            return databaseSection[1]
        else:
            return returnVar

    def recentEmbed(self,res):
        beatmap = osuapi.get_beatmaps(beatmap_id=res[0].beatmap_id)
        osuUser = osuapi.get_user(username=res[0].user_id)

        print(res[0].accuracy("mode"))
        formattingElements = {"artist":beatmap[0].artist, "title":beatmap[0].title, "mapsetID":beatmap[0].beatmapset_id, "mapID":beatmap[0].beatmap_id,"mods":res[0].enabled_mods,
                              "rank":res[0].rank, "pp":"pp soon", "accuracy":res[0].accuracy("OsuMode"),"mapper":beatmap[0].creator,
                              "300":res[0].count300, "100":res[0].count100, "50":res[0].count50, "miss":res[0].countmiss,
                              "playercombo":res[0].maxcombo, "mapcombo":beatmap[0].max_combo ,"spac)e1":" \u200B", "space2":"\u200B \u200B \u200B \u200B \u200B"}

        descriptionFormat = (f" ✦ [**{formattingElements['artist']} - {formattingElements['title']}**](https://osu.ppy.sh/beatmapsets/{formattingElements['mapsetID']}#osu/{formattingElements['mapID']})\n"
                            f"{formattingElements['space2']} [**| by {formattingElements['mapper']}**](https://osu.ppy.sh/beatmapsets/{formattingElements['mapsetID']}#osu/{formattingElements['mapID']}) \n\n"

                            f"|{formattingElements['mods']}\n"
                            f"▸ {formattingElements['rank']} | {formattingElements['pp']}"
                            f"▸ {formattingElements['accuracy']} | [{formattingElements['300']}/{formattingElements['100']}/"
                            f"▸ {formattingElements['50']}/{formattingElements['miss']}]"
                            f"▸ {formattingElements['playercombo']}/{formattingElements['mapcombo']}\n\n")


        embed = discord.Embed(description = descriptionFormat.format(*formattingElements), color = discord.Color(0xFF748C))
        embed.set_thumbnail(url = beatmap[0].cover_thumbnail)
        embed.set_author(name = osuUser[0].username + " recent play!", icon_url = osuUser[0].profile_image)
        embed.set_footer(text="Played " + str(res[0].date)[11:])
        return embed



    @commands.command(aliases=["Bounty","bounties", "bountea"], description="Verify your lastest play as the bounty and check for the points earned", usage=".bounty {username}")
    async def bounty(self, ctx, playerName=None):

        if isinstance(playerName,str) == True:
            try :
                osuUser = int(playerName)
            except:
                osuUser = playerName




        if not playerName or playerName.startswith("<@!"):
            userID = ctx.author.id
            osuUser = self.idVerification(ctx,playerName)
            if osuUser == 1:
                await ctx.send("Player not found!")
                return
            if osuUser == 2:
                await ctx.send("Use the .osuset {username} before using .bounty or do .bounty {username}")
                return

        res = osuapi.get_user_recent(osuUser,limit=1)
        if len(res) == 0:
            await ctx.send("No map found in your recent play")
            return

        embed = self.recentEmbed(res)
        await ctx.send(embed=embed)

        await ctx.send("it's not the bounty map dumdum")

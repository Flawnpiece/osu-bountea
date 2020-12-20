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

    def recentEmbed(self,ctx,res):
        beatmap = osuapi.get_beatmaps(beatmap_id=res[0].beatmap_id)
        osuUser = osuapi.get_user(username=res[0].user_id)

        descriptionFormat = """ ✦ **{0} - {1}** | {2}

                                ▸ {3} | {4} | acc[{5}/{6}/{7}/{8}]
                                ▸ {9}/{10}
                            """
        formattingElements = (beatmap[0].artist, beatmap[0].title, res[0].enabled_mods, res[0].rank,
                             "pp soon", res[0].count300, res[0].count100, res[0].count50,res[0].countmiss,
                             res[0].maxcombo, beatmap[0].max_combo)

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

        embed = self.recentEmbed(ctx,res)
        await ctx.send(embed=embed)

        await ctx.send("it's not the bounty map dumdum")

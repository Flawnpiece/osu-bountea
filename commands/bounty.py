import discord
from discord.ext import commands
from main import osuapi, connection,cursor
import sqlite3



def setup(bot):
    bot.add_cog(BountyVerification(bot))

class BountyVerification(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def idVerification(self,ctx):
        userID = ctx.author.id

        cursor.execute("SELECT * FROM osuset WHERE discord_id=?", (userID,))

        databaseSection = cursor.fetchone()
        connection.close()

        #check if we got something out of the database
        if isinstance(databaseSection,tuple) == True:
            return databaseSection[1]
        else:
            return 0

    @commands.command(aliases=["Bounty","bounties", "bountea"], description="Verify your lastest play as the bounty and check for the points earned", usage=".bounty {username}")
    async def bounty(self, ctx, playerName=None):

        if not playerName:
            osuUserId = self.idVerification(ctx)
            if osuUserId == 0:
                await ctx.send("Use the .osuset command bukako!")
                return

            res = osuapi.get_user_best(osuUserId)

        else:
            res = osuapi.get_user_best(playerName)

        await ctx.send(res[0].user_id)

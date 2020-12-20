import discord
from discord.ext import commands
from main import osuapi, connection,cursor
import sqlite3

def setup(bot):
    bot.add_cog(osuUsernameSet(bot))

class osuUsernameSet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def addIntoDatabase(self,ctx,osuID):
        print("addIntoDatabase")


        cursor.execute("SELECT * FROM osuset WHERE discord_id=?", (ctx.author.id,))
        databaseSection = cursor.fetchone()
        if isinstance(databaseSection,tuple) == True:
            cursor.execute("UPDATE osuset SET osu_id=? WHERE discord_id=?",(osuID,ctx.author.id))
            connection.commit()
            message = 0
        else:
            cursor.execute("INSERT INTO osuset VALUES (?,?)",(ctx.author.id,osuID))
            connection.commit()
            message = 1
        return message

    @commands.command(description="Set your username by default so you don't have to type it when you .bounty!", usage=".osuset {username/id}")
    async def osuset(self,ctx, arg=None):
        if not arg:
            await ctx.send("Please provide a username or an id")
            return

        res = osuapi.get_user(arg)

        message = self.addIntoDatabase(ctx,res[0].user_id)
        if message == 0:
            await ctx.send("Default username updated to " + arg + " !")
        else:
            await ctx.send("Default username set to " + arg + " !")
        

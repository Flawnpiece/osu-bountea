import discord
from discord.ext import commands
import sqlite3
from main import osuapi

#would need some code cleaning but im lazy so ill do it another time

def setup(bot):
    bot.add_cog(pointsInformation(bot))

class pointsInformation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["point","pts"], description="Showcase the points info of the current bounty", usage=".points")
    async def points(self,ctx):

        connection = sqlite3.connect('data/scoreInformation.db')
        cursor = connection.cursor()

        cursor.execute("SELECT pointBasedOn FROM genericInformation")

        pointBasedOn = cursor.fetchone()[0]

        cursor.execute("SELECT cutOff FROM genericInformation")

        cutOff = cursor.fetchone()[0]

        cursor.execute(f"SELECT * FROM {pointBasedOn}")

        pointsSection = cursor.fetchall()

        cursor.execute(f"SELECT * FROM mods")

        modsTuple = cursor.fetchall()

        mods = []
        for v in modsTuple:
            mods.append([v[0],v[1]])

        for v in mods:
            if v[1] > 0:
                v[1] = "+" + str(v[1])

        s = "\u200B "
        s2 = " \u200B "*40
        s3 = " \u200B "*26
        s4 = " \u200B "*32
        descriptionFormat2 = f"**Current pointing system!**\n\n"
        i = 0
        c = 0
        while i < len(pointsSection):
            if i >= cutOff:
                if pointBasedOn == "rank":
                    descriptionFormat2 = descriptionFormat2 + f"{s2}{s4}``{mods[i][0]} = {mods[i][1]} ``\n"
                if pointBasedOn == "combo":
                    descriptionFormat2 = descriptionFormat2 + f"{s2}{s2}``{mods[i][0]} = {mods[i][1]} ``\n"
                if pointBasedOn == "accuracy":
                    descriptionFormat2 = descriptionFormat2 + f"{s2}{s2}{s}{s}``{mods[i][0]} = {mods[i][1]} ``\n"

                i = i + 1

            else:
                if pointBasedOn == "rank":
                    descriptionFormat2 = descriptionFormat2 + f"``{pointsSection[i][0]:2} = {pointsSection[i][1]} points `` {s2} ``{mods[i][0]} = {mods[i][1]:2} ``\n"
                    i = i + 1
                elif pointBasedOn == "accuracy":
                    descriptionFormat2 = descriptionFormat2 + f"``{pointsSection[i][0]:5} = {pointsSection[i][1]:3} points `` {s2} ``{mods[i][0]} = {mods[i][1]:2} ``\n"
                    i = i + 1

                elif pointBasedOn == "combo":
                    descriptionFormat2 = descriptionFormat2 + f"``{pointsSection[i][0]:6} = {pointsSection[i][1]} points `` {s2} ``{mods[i][0]} = {mods[i][1]:2} ``\n"
                    i = i + 1

                elif pointBasedOn == "condition":

                    descriptionFormat2 = descriptionFormat2 + f"``Condition : {pointsSection[i][0]:6} ``{s3} ``{mods[i][0]} = {mods[i][1]:2} ``\n"
                    descriptionFormat2 = descriptionFormat2 + f" {s2}{s2} ``{mods[1][0]} = {mods[1][1]} ``\n"
                    descriptionFormat2 = descriptionFormat2 + f" {s2}{s2} ``{mods[2][0]} = {mods[2][1]} ``\n"
                    descriptionFormat2 = descriptionFormat2 + f" {s2}{s2} ``{mods[3][0]} = {mods[3][1]} ``\n"
                    descriptionFormat2 = descriptionFormat2 + f" {s2}{s2} ``{mods[4][0]} = {mods[4][1]} ``\n"
                    descriptionFormat2 = descriptionFormat2 + f" {s2}{s2} ``{mods[5][0]} = {mods[5][1]} ``\n"


                    i = i + 1


        cursor.execute("SELECT extraMods FROM genericInformation")

        extraMods = cursor.fetchone()[0]


        if extraMods > 0:
            cursor.execute("SELECT * FROM modsCombination")
            modsCombinationTuple = cursor.fetchall()
            print("initial mods",modsCombinationTuple)
            modsCombination = []
            for v in modsCombinationTuple:
                modsCombination.append([v[0],v[1]])

            for v in modsCombination:
                if v[1] > 0:
                    v[1] = "+" + str(v[1])

            modsCombinationFormat =  f"\nSpecific mods combination(s) values: \n``"
            i = 0
            while i < extraMods:
                modsCombinationFormat = modsCombinationFormat + f"{modsCombination[i][0]} = {modsCombination[i][1]:2}"
                i = i + 1
                if i < extraMods:
                    modsCombinationFormat = modsCombinationFormat + "| "
        modsCombinationFormat = modsCombinationFormat + "``"
        descriptionFormat2 = descriptionFormat2 + modsCombinationFormat


        cursor.execute("SELECT bonusPoints FROM genericInformation")

        bonusPoints = cursor.fetchone()[0]


        if bonusPoints > 0:
            cursor.execute("SELECT * FROM bonusPoints")
            bonusPointsTuple = cursor.fetchall()

            bonusPointsList = []
            for v in bonusPointsTuple:
                bonusPointsList.append([v[0],v[1]])

            for v in bonusPointsList:
                if v[1] > 0:
                    v[1] = "+" + str(v[1])
            print(bonusPointsList)
            bonusPointsFormat =  f"\n\nBonus points conditions:\n"
            i = 0
            while i < bonusPoints:
                bonusPointsFormat = bonusPointsFormat + f" ``{bonusPointsList[i][0]:32} = {bonusPointsList[i][1]:2}``\n"
                i = i + 1

        bonusPointsFormat = bonusPointsFormat + ""
        descriptionFormat2 = descriptionFormat2 + bonusPointsFormat


        embed = discord.Embed(description = descriptionFormat2, color = discord.Color(0xFF748C))
        embed.set_author(name = "Bounty information!", icon_url = self.bot.user.avatar_url)
        embed.set_footer(text="Good luck!")
        await ctx.send(embed=embed)

        connection.close()

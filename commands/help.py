import discord
from discord.ext import commands

def setup(bot):
    bot.add_cog(HelpCommands(bot))

class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def subHelpValidity(self,arg):
        commandList = []
        for v in self.bot.commands:
            commandList.append(v)

        validArg = 0

        for v in commandList:
            for a in v.aliases:
                if a == arg:
                    validArg = v
                    break
            if v.name == arg:
                validArg = v
                break

        return validArg

    def aliasesFormatting(self,alias):
        if len(alias) <=1:
            return
        else:
            strAliases = alias[0]
            d = ""
            i = 1
            while i < len(alias):

                strAliases = strAliases + " | " + alias[i]
                i = i + 1
            return strAliases

    @commands.command()
    async def help(self,ctx, arg=None):
        if not arg:
            descriptionFormat = """ **Information commands** : ``info`` ``points`` ``map``
                                    **Utilities commands** : ``osuset`` ``bounty`` ``score``

                                    Do ``.help [command name]`` to get more information!
                                    
                                """
            embed = discord.Embed(description = descriptionFormat, color = discord.Color(0xFF748C))
            embed.set_author(name = "osu!bountea commands list!", icon_url = self.bot.user.avatar_url)
            embed.set_footer(text="Bot made by your local trackpad player")
            await ctx.send(embed=embed)

        else:
            validArg = self.subHelpValidity(arg)

            if validArg == 0:
                await ctx.send("Verify the spelling of the command your entered!")
                return

            descriptionFormat = """ **Command name:** ``{0}``
                                    **Usage:** ``{1}``
                                    **Aliases:** ``{2}``
                                    **Description:**
                                    {3}

                                    Do ``.help`` to get all the comands avaiblie

                                """
            embed = discord.Embed(description = descriptionFormat.format(validArg.name,validArg.usage,self.aliasesFormatting(validArg.aliases),validArg.description), color = discord.Color(0xFF748C))
            embed.set_author(name = "osu!bountea commands list!", icon_url = self.bot.user.avatar_url)
            embed.set_footer(text="Bot made by your local trackpad player")
            await ctx.send(embed=embed)
            print(validArg)

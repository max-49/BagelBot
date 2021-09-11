import os
import json
import asyncio
import discord
from discord.ext import commands


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='resetbot', help='resets all bot data')
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def resetbot(self, ctx):
        await ctx.send("Resetting all saved data")
        await asyncio.sleep(5)
        await ctx.send("Data reset!")
    
    @resetbot.error
    async def resetbot_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cd = round(error.retry_after)
            minutes = str(cd // 60)
            seconds = str(cd % 60)
            em = discord.Embed(title=f"Woah! Stop resetting the bot so fast!",
                               description=f"Try again in {minutes} minutes and {seconds} seconds.", color=0xFF0000)
            await ctx.send(embed=em)

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send(f"`{cog.split('.')[-1]}` cog successfully loaded!")

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send(f"`{cog.split('.')[-1]}` cog successfully unloaded!")

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send(f"`{cog.split('.')[-1]}` cog successfully reloaded!")

    @commands.command(name='fixprofiles', hidden=True)
    @commands.is_owner()
    async def updateprofiles(self, ctx):
        with open('profiles.json') as j:
            profile_data = json.load(j)
        for i in range(len(profile_data)):
            if(profile_data[i]['Balance'] < 0):
                profile_data[i]['Balance'] = 0
        with open('profiles.json', 'w') as j:
            json.dump(profile_data, j)
        await ctx.send("Profiles updated!")

    async def cog_command_error(self, ctx, error):
        await ctx.send(f"**`ERROR in {os.path.basename(__file__)}:`** {type(error).__name__} - {error}")

def setup(bot):
    bot.add_cog(Owner(bot))
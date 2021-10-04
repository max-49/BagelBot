import os
import json
import string
import asyncio
import discord
import subprocess
from datetime import datetime
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
            em = discord.Embed(title=f"Woah! Stop resetting the bot so fast!", description=f"Try again in {minutes} minutes and {seconds} seconds.", color=0xFF0000)
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

    @commands.command(name="addmoney", help="add money to someone's profile!", pass_context=True)
    @commands.is_owner()
    async def addmoney(self, ctx, member: discord.Member, money: int = None):
        def check(msg):
            return msg.author == ctx.author and msg.channel == msg.channel and \
                msg.content.lower()[0] in string.digits
        with open('profiles.json') as f:
            profile_data = json.load(f)
        found = 0
        uid = member.id
        if money is None:
            await ctx.send("How much money would you like to give to this person?")
            money = await self.bot.wait_for("message", check=check)
            money = int(money.content)
        if(money < 0):
            await ctx.send("Infinite robux hack does not work on this bot lol")
            return
        for i in range(len(profile_data)):
            if(profile_data[i]['ID'] == uid):
                found = 1
                embedVar = discord.Embed(
                    title=f"Giving money to {member.display_name}", timestamp=datetime.utcnow(), color=0x00FF00)
                embedVar.add_field(
                    name=f"{member.display_name}", value=f"Old balance: {profile_data[i]['Balance']}\nNew balance: {profile_data[i]['Balance'] + money}", inline=True)
                profile_data[i]['Balance'] = profile_data[i]['Balance'] + money
                await ctx.reply(embed=embedVar)
        if(found == 0):
            await ctx.send("No profile found for this user! Ask them to create one before giving them money!")
        with open('profiles.json', 'w') as json_file:
            json.dump(profile_data, json_file)

    @commands.command(name="takemoney", help="take money from someone's profile!", pass_context=True)
    @commands.is_owner()
    async def takemoney(self, ctx, member: discord.Member, money: int = None):
        def check(msg):
            return msg.author == ctx.author and msg.channel == msg.channel and \
                msg.content.lower()[0] in string.digits
        with open('profiles.json') as f:
            profile_data = json.load(f)
        found = 0
        uid = member.id
        if money is None:
            await ctx.send("How much money would you like to take from this person?")
            money = await self.bot.wait_for("message", check=check)
            money = int(money.content)
        if(money < 0):
            await ctx.send("Infinite robux hack does not work on this bot lol")
            return
        for i in range(len(profile_data)):
            if(profile_data[i]['ID'] == uid):
                found = 1
                embedVar = discord.Embed(
                    title=f"Removing money from {member.display_name}", timestamp=datetime.utcnow(), color=0xFF0000)
                old_money = profile_data[i]['Balance'] - money
                embedVar.add_field(
                    name=f"{member.display_name}", value=f"Old balance: {profile_data[i]['Balance']}\nNew balance: {profile_data[i]['Balance'] - money}", inline=True)
                profile_data[i]['Balance'] = profile_data[i]['Balance'] - money
                await ctx.reply(embed=embedVar)
        if(found == 0):
            await ctx.send("No profile found for this user! Ask them to create one before ruining their life!")
        with open('profiles.json', 'w') as json_file:
            json.dump(profile_data, json_file)

    @commands.command(name="resetprofile", help="resets a profile", hidden=True)
    @commands.is_owner()
    async def resetprofile(self, ctx, user_id):
        with open('profiles.json') as f:
            profile_data = json.load(f)
        if(user_id.isnumeric()):
            uid = int(user_id)
        else:
            uid = user_id
        for i in range(len(profile_data)):
            if(profile_data[i]['ID'] == uid or profile_data[i]['Name'] == uid):
                embedVar = discord.Embed(title=f"{profile_data[i]['Name']}'s balance", timestamp=datetime.utcnow(), color=0x00C3FF)
                profile_data[i]['Balance'] = 0
                profile_data[i]['Profit'] = 0
                profile_data[i]['Win'] = 0
                profile_data[i]['Times'] = 0
                profile_data[i]['Lose'] = 0
                await ctx.reply(embed=embedVar)
                break
        else:
            raise ValueError("No profile found for mentioned user.")
        with open('profiles.json', 'w') as json_file:
            json.dump(profile_data, json_file)

    @commands.command(name='shell', hidden=True)
    @commands.is_owner()
    async def shell(self, ctx):
        await ctx.send('Shell spawned. Type `exit` to exit the shell.')
        def check(msg):
            return msg.author == ctx.author and msg.channel == msg.channel and msg.content.lower()[0] in string.printable

        while True:
            command = await self.bot.wait_for("message", check=check)
            print(f"$ {command.content}")
            if(command.content == 'exit'):
                break
            try:
                proc = subprocess.check_output([command.content], shell=True).decode("utf-8")
            except subprocess.CalledProcessError as e:
                proc = e.stdout
            if(proc == b""):
                await ctx.send("Command errored but idk how to get the error message to show")
            else:
                if(proc != ""):
                    await ctx.send(f"```{proc}```")
                else:
                    await ctx.send("Command executed with no stdout")

        await ctx.send('Shell exited')

    async def cog_command_error(self, ctx, error):
        await ctx.send(f"**`ERROR in {os.path.basename(__file__)}:`** {type(error).__name__} - {error}")

def setup(bot):
    bot.add_cog(Owner(bot))
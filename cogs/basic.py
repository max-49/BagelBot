import os
import json
import discord
import requests
from datetime import datetime
from discord.ext import commands

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pfp', help="Displays a profile picture", pass_context=True)
    async def pfp(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send(f'{ctx.author.avatar_url}')
        else:
            await ctx.send(f'{member.avatar_url}')

    @commands.command(name='info', help="Displays information about this bot")
    async def info(self, ctx):
        embed = discord.Embed(title="Bot Info", timestamp=datetime.utcnow(), color=0x00ff00)
        embed.add_field(name="Creator", value="Made by Max49#9833", inline=False)
        embed.add_field(name="This bot is open source!", value="Check it out on my GitHub!")
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/427832149173862400/7628cad11d9dd038681b4b3e25201e7b.webp?size=1024")
        await ctx.send(embed=embed)
    
    @commands.command(name='help', help='displays this message!')
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def helpcommand(self, ctx, *, select_cog=None):
        help_list = []
        num = 0

        for cog in self.bot.cogs:
            help_dict = {}
            cog_coms = []
            walk_cog = self.bot.get_cog(cog)
            commands = walk_cog.get_commands()
            for command in commands:
                if not command.hidden:
                    cog_coms.append(f'{command.name} - {command.help}')
            help_dict[cog] = cog_coms
            help_list.append(help_dict)
            num += 1

        if select_cog is None:
            number = 0
            embed = discord.Embed(
                title=f"{self.bot.user.name} Help", color=0x00ff00)
            for key, value in help_list[number].items():
                field = ""
                for thing in value:
                    field += f"{thing}\n"
                embed.add_field(name=key, value=field, inline=False)
                embed.set_footer(text=f"{number + 1}/{len(help_list)}")
        else:
            for i in range(len(help_list)):
                for key, value in help_list[i].items():
                    if str(key.lower()) == str(select_cog.lower()):
                        number = i
            embed = discord.Embed(
                title=f"{self.bot.user.name} Help", color=0x00ff00)
            try:
                for key, value in help_list[number].items():
                    field = ""
                    for thing in value:
                        field += f"{thing}\n"
                    embed.add_field(name=key, value=field, inline=False)
                    embed.set_footer(text=f"{number + 1}/{len(help_list)}")
            except UnboundLocalError:
                number = 0
                embed = discord.Embed(
                    title=f"{self.bot.user.name} Help", color=0x00ff00)
                for key, value in help_list[number].items():
                    field = ""
                    for thing in value:
                        field += f"{thing}\n"
                    embed.add_field(name=key, value=field, inline=False)
                    embed.set_footer(text=f"{number + 1}/{len(help_list)}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('⬅️')
        await message.add_reaction('➡️')

        with open('commands.json', 'w') as j:
            json.dump(help_list, j)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        def get_next_embed(embeds, number, react):
            if number == 0 and react == 0 or number == len(embeds) - 1 and react == 1:
                return None
            if react == 0:
                number -= 1
                new_embed_data = embeds[number]
                embed = discord.Embed(
                    title=f"{self.bot.user.name} Help", color=0x00ff00)
                for key, value in new_embed_data.items():
                    field = ""
                    for thing in value:
                        field += f"{thing}\n"
                    embed.add_field(name=key, value=field, inline=False)
                    embed.set_footer(text=f"{number + 1}/{len(embeds)}")
                return embed
            elif react == 1:
                number += 1
                new_embed_data = embeds[number]
                embed = discord.Embed(
                    title=f"{self.bot.user.name} Help", color=0x00ff00)
                for key, value in new_embed_data.items():
                    field = ""
                    for thing in value:
                        field += f"{thing}\n"
                    embed.add_field(name=key, value=field, inline=False)
                    embed.set_footer(text=f"{number + 1}/{len(embeds)}")
                return embed

        with open('commands.json') as j:
            commands = json.load(j)
        if reaction.message.author.id == self.bot.user.id and user != self.bot.user:
            embed = reaction.message.embeds[0]
            for i in range(len(commands)):
                for key in commands[i]:
                    if str(key) == str(embed.fields[0].name):
                        number = i
            if str(reaction.emoji) == "⬅️":
                newEmbed = get_next_embed(commands, number, 0)
                if newEmbed is not None:
                    await reaction.message.edit(embed=newEmbed)
            if str(reaction.emoji) == "➡️":
                newEmbed = get_next_embed(commands, number, 1)
                if newEmbed is not None:
                    await reaction.message.edit(embed=newEmbed)

    @helpcommand.error
    async def help_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cd = round(error.retry_after)
            minutes = str(cd // 60)
            seconds = str(cd % 60)
            em = discord.Embed(title=f"Woah! You don't need so many help embeds! Just use the one you already have!", description=f"Try again in {minutes} minutes and {seconds} seconds.", color=0xFF0000)
            await ctx.send(embed=em)

    @commands.command(name="stats", help="ictf stats lmao", pass_context=True)
    async def stats(self, ctx, member: discord.Member = None):
        try:
            if member is None:
                member = ctx.author
            all_challs = (requests.get(
                'https://imaginaryctf.org/api/challenges/released')).json()
            my_challs = (requests.get(
                f'https://imaginaryctf.org/api/solves/bydiscordid/{member.id}')).json()
            if(my_challs[0]["team"] != None):
                my_challs = (requests.get(
                    f'https://imaginaryctf.org/api/solves/byteamid/{my_challs[0]["team"]["id"]}')).json()
                score = my_challs[0]["team"]["score"]
                name = str(my_challs[0]["team"]["name"]) + " (team)"
            else:
                score = my_challs[0]["user"]["score"]
                name = member.name
            all_solves = []
            all_list = []
            all_list_alt = []
            for i in range(len(my_challs)):
                all_solves.append(my_challs[i]["challenge"]["title"])
            for i in range(len(all_challs)):
                all_list.append(all_challs[i]["title"])
            for thing in all_list:
                all_list_alt.append(thing)
            for thing in all_list_alt:
                if(thing in all_solves):
                    all_list.remove(thing)
            all_solves.reverse()
            all_list.reverse()
            solved = '\n'.join(all_solves)
            unsolved = '\n'.join(all_list)
            embedVar = discord.Embed(title=f"Stats for {name}", color=0x3498DB)
            embedVar.add_field(name="Score", value=score, inline=False)
            if(len(solved) > 3):
                embedVar.add_field(name="Solved Challenges", value=solved, inline=True)
            if(len(unsolved) > 3):
                embedVar.add_field(name="Unsolved Challenges", value=unsolved, inline=True)
            embedVar.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=embedVar)
        except IndexError:
            await ctx.send("User is not on the leaderboard yet! Tell them to check out <https://imaginaryctf.org/>!")

    @commands.command(name='spam', help="spams text")
    async def spam(self, ctx, *, string: str):
        for i in range(5):
            await ctx.send(string, allowed_mentions=discord.AllowedMentions(everyone=False))

    @commands.command(name="ping", help="displays the latency to the bot.")
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency * 1000)}ms')

    async def cog_command_error(self, ctx, error):
        await ctx.send(f"**`ERROR in {os.path.basename(__file__)}:`** {type(error).__name__} - {error}")


def setup(bot):
    bot.add_cog(Basic(bot))
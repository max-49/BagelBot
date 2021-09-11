import os
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound

prefix = 'b.'

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), help_command=None, intents=intents)

TOKEN = os.getenv("BAGEL_TOKEN")

@bot.event
async def on_ready():
    print("Setting NP game", flush=True)
    await bot.change_presence(activity=discord.Game(name='b.help'))
    print(f"Logged in as {bot.user.name}")

@bot.event
async def on_message(ctx):
    if ctx.content.startswith(prefix) and ctx.author.id != bot.user.id:
        print(f"{ctx.author.name}: {ctx.content}")
    await bot.process_commands(ctx)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        command = str(error).split('"')[1]
        await ctx.send(f"Command **`{command}`** not found.", allowed_mentions=discord.AllowedMentions(everyone=False))

if __name__ == '__main__':
    for filename in os.listdir('cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
    bot.run(TOKEN)

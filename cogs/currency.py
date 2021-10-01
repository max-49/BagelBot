import os
import json
import math
import random
import discord
import itertools
from datetime import datetime
from discord.ext import commands

class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="bal", aliases=['balance', 'profile'], help="displays your balance!")
    async def bal(self, ctx, user_id=None):
        with open('profiles.json') as f:
            profile_data = json.load(f)
        if user_id is None:
            uid = ctx.author.id
        else:
            if(user_id.isnumeric()):
                uid = int(user_id)
            else:
                uid = user_id
        for i in range(len(profile_data)):
            if(profile_data[i]['ID'] == uid or profile_data[i]['Name'] == uid):
                embedVar = discord.Embed(title=f"{profile_data[i]['Name']}'s balance", timestamp=datetime.utcnow(), color=0x00C3FF)
                embedVar.add_field(name="Balance", value=f"{profile_data[i]['Balance']} bagels", inline=False)
                embedVar.add_field(name="Net profit from betting", value=f"{profile_data[i]['Profit']} bagels", inline=False)
                try:
                    percent = round((profile_data[i]['Win']/profile_data[i]['Times'])*100, 2)
                except ZeroDivisionError:
                    percent = 0
                embedVar.add_field(name="Percent times won", value=f"{profile_data[i]['Win']}/{profile_data[i]['Times']} times ({percent}%)", inline=False)
                embedVar.set_thumbnail(url=profile_data[i]['Avatar URL'])
                await ctx.reply(embed=embedVar)
                return
        else:
            if(user_id is None):
                profile_data.append({"Name": ctx.author.name, "ID": ctx.author.id, "Avatar URL": str(ctx.author.avatar_url), "Balance": 1000, "Times": 0, "Win": 0, "Lose": 0, "Profit": 0})
                embedVar = discord.Embed(title=f"{ctx.author.name}'s balance", timestamp=datetime.utcnow(), color=0x00C3FF)
                embedVar.add_field(name="Profile initialized!", value="Run `b.balance` again to see your stats", inline=False)
                embedVar.set_thumbnail(url=str(ctx.author.avatar_url))
                await ctx.reply(embed=embedVar)
            else:
                await ctx.send("No profile found for this user! Ask them to create one with `b.balance` :)")
                return
        with open('profiles.json', 'w') as json_file:
            json.dump(profile_data, json_file)
        
    @commands.command(name='table', help='shows the slots payout table!')
    async def table(self, ctx):
        tables = [ { 'emoji': '⚽️', 'count': 2, 'payout': 1 }, { 'emoji': '🔍', 'count': 2, 'payout': 1 }, { 'emoji': '⌛️', 'count': 2, 'payout': 1.75 }, { 'emoji': '🏓', 'count': 2, 'payout': 1.75 }, { 'emoji': '🔴', 'count': 2, 'payout': 2 }, { 'emoji': '🌍', 'count': 2, 'payout': 2 }, { 'emoji': '💵', 'count': 2, 'payout': 2 }, { 'emoji': '📸', 'count': 2, 'payout': 2 }, { 'emoji': '🏓', 'count': 3, 'payout': 5 }, { 'emoji': '⚽️', 'count': 3, 'payout': 10 }, { 'emoji': '🔍', 'count': 3, 'payout': 10 }, { 'emoji': '🔴', 'count': 3, 'payout': 20 }, { 'emoji': '⌛️', 'count': 3, 'payout': 25 }, { 'emoji': '🌍', 'count': 3, 'payout': 50 }, { 'emoji': '📸', 'count': 3, 'payout': 75 }, { 'emoji': '💵', 'count': 3, 'payout': 250 }]
        emojis = ''
        for table in tables:
            emojis += f"{table['emoji'] * table['count']}     - {table['payout']}x\n"
        embed = discord.Embed(title='Slots payout table!', timestamp=datetime.utcnow(), color=0x00C3FF)
        embed.add_field(name='emoji - payout', value=emojis, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='shop', help='buy items at the shop!')
    async def shop(self, ctx):
        embed = discord.Embed(title='BagelBot shop!', timestamp=datetime.utcnow(), color=0x00C3FF)
        embed.add_field(name='Items for sale! (Item code - Price)', value='**1kbagels** - 1,000 bagels\n**fakeflag** - 1,000 bagels\n**flag** - 1,000,000 bagels', inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='buy', help='buy an item from b.shop!')
    async def buy(self, ctx, buy_item: str):
        with open('profiles.json') as f:
            profile_data = json.load(f)
        items = [{'name': '1kbagels', 'price': 1000}, {'name': 'fakeflag', 'price': 1000}, {'name': 'flag', 'price': 1000000}]
        for i in range(len(profile_data)):
            if(profile_data[i]['ID'] == ctx.author.id):        
                for item in items:
                    if(item['name'] == buy_item):
                        if(item['price'] > profile_data[i]['Balance']):
                            await ctx.reply("You don't have enough money to buy this item!")
                            return
                        else:
                            profile_data[i]['Balance'] = profile_data[i]['Balance'] - item['price']
                            if(item['name'] == '1kbagels'):
                                profile_data[i]['Balance'] = profile_data[i]['Balance'] + 1000
                                await ctx.reply('1,000 bagels have been accredited to your account!')
                            elif(item['name'] == 'fakeflag'):
                                await ctx.reply(f"{open('fakeflag.txt', 'r').read()}")
                            elif(item['name'] == 'flag'):
                                await ctx.reply(f"{open('flag.txt', 'r').read()}")
                            else:
                                await ctx.reply("i have no idea how you got here. dm max if you got here.")
                            with open('profiles.json', 'w') as json_file:
                                json.dump(profile_data, json_file)
                            return
                else:
                    await ctx.reply("Item doesn't exist! Make sure to use the item code found in `b.shop`")
        else:
            await ctx.reply("You don't have a profile yet! Create one with `b.balance`!")

    @commands.command(name="bet", help="b.bet <high | slots> <amount>")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def bet(self, ctx, bet: str, amount: int):
        with open('profiles.json') as f:
            profile_data = json.load(f)
        if(amount < 1):
            await ctx.reply('no')
            return
        if(len(bet) > 15):
            await ctx.reply('Invalid option! Please choose either `high` or `slots`.')
            return
        for i in range(len(profile_data)):
            if(profile_data[i]['ID'] == ctx.author.id):
                original_balance = int(profile_data[i]['Balance'])
                bet = bet.replace('../', '')
                if(amount > original_balance):
                    await ctx.reply("You can't bet more than you have!")
                    return
                try:    
                    with open(f'betting/{bet}') as j:
                        welcome_message = j.read()
                except FileNotFoundError:
                    await ctx.reply('Invalid option! Please choose either `high` or `slots`.')
                    return
                if(bet == 'high'):
                    bagel_roll = random.randint(1,6)
                    you_roll = random.randint(1,6)
                    if(you_roll > bagel_roll):
                        percent_won = random.randint(50,100)
                        embed = discord.Embed(title=welcome_message, timestamp=datetime.utcnow(), color=0x00ff00)
                        embed.add_field(name='BagelBot rolls...', value=bagel_roll, inline=True)
                        embed.add_field(name='You roll...', value=you_roll, inline=True)
                        embed.add_field(name=f'Congrats, you win! Your new balance is {math.floor(original_balance + (amount * (percent_won/100)))} bagels!', value=f'Percent won: {percent_won}%', inline=False)
                        profile_data[i]['Times'] = profile_data[i]['Times'] + 1
                        profile_data[i]['Win'] = profile_data[i]['Win'] + 1
                        profile_data[i]['Profit'] = profile_data[i]['Profit'] + math.floor(amount * (percent_won/100))
                        profile_data[i]['Balance'] = int(math.floor(original_balance + (amount * (percent_won/100))))
                        await ctx.reply(embed=embed)
                    elif(you_roll < bagel_roll):
                        embed = discord.Embed(title=welcome_message, timestamp=datetime.utcnow(), color=0xFF0000)
                        embed.add_field(name='BagelBot rolls...', value=bagel_roll, inline=True)
                        embed.add_field(name='You roll...', value=you_roll, inline=True)
                        profile_data[i]['Times'] = profile_data[i]['Times'] + 1
                        profile_data[i]['Lose'] = profile_data[i]['Lose'] + 1
                        profile_data[i]['Profit'] = profile_data[i]['Profit'] - amount
                        embed.add_field(name=f'You lose! Your new balance is {original_balance - amount} bagels!', value=':(', inline=False)
                        profile_data[i]['Balance'] = int(original_balance - amount)
                        await ctx.reply(embed=embed)
                    else:
                        embed = discord.Embed(title=welcome_message, timestamp=datetime.utcnow(), color=0xFFFF00)
                        embed.add_field(name='BagelBot rolls...', value=bagel_roll, inline=True)
                        embed.add_field(name='You roll...', value=you_roll, inline=True)
                        embed.add_field(name=f'Tie! Nobody loses money!', value='Close one', inline=False)
                        profile_data[i]['Times'] = profile_data[i]['Times'] + 1
                        await ctx.reply(embed=embed)
                elif(bet == 'slots'):
                    if(amount > 5000):
                        await ctx.reply("You can't bet more than 5000 bagels in the slot machine!")
                        return
                    emojis = ['⚽️', '🔴', '🔍', '🌍', '📸', '💵', '⌛️', '🏓']
                    slots = ' '.join([random.choice(emojis), random.choice(emojis), random.choice(emojis)])
                    tables = [ { 'emoji': '⚽️', 'count': 2, 'payout': 1 }, { 'emoji': '🔍', 'count': 2, 'payout': 1 }, { 'emoji': '⌛️', 'count': 2, 'payout': 1.75 }, { 'emoji': '🏓', 'count': 2, 'payout': 1.75 }, { 'emoji': '🔴', 'count': 2, 'payout': 2 }, { 'emoji': '🌍', 'count': 2, 'payout': 2 }, { 'emoji': '💵', 'count': 2, 'payout': 2 }, { 'emoji': '📸', 'count': 2, 'payout': 2 }, { 'emoji': '🏓', 'count': 3, 'payout': 5 }, { 'emoji': '⚽️', 'count': 3, 'payout': 10 }, { 'emoji': '🔍', 'count': 3, 'payout': 10 }, { 'emoji': '🔴', 'count': 3, 'payout': 20 }, { 'emoji': '⌛️', 'count': 3, 'payout': 25 }, { 'emoji': '🌍', 'count': 3, 'payout': 50 }, { 'emoji': '📸', 'count': 3, 'payout': 75 }, { 'emoji': '💵', 'count': 3, 'payout': 250 }]
                    payout = 0
                    for emoji in emojis:
                        instances = slots.count(emoji)
                        for table in tables:
                            if(emoji == table['emoji']):
                                if(instances == table['count']):
                                    payout = table['payout']
                    if(payout == 0):
                        embed = discord.Embed(title=welcome_message, timestamp=datetime.utcnow(), color=0xFF0000)
                        embed.add_field(name='Your slot roll:', value=f'**>** {slots} **<**', inline=False)
                        embed.add_field(name=f'You lose! Your new balance is {original_balance - amount} bagels.', value=':(', inline=False)
                        profile_data[i]['Times'] = profile_data[i]['Times'] + 1
                        profile_data[i]['Lose'] = profile_data[i]['Lose'] + 1
                        profile_data[i]['Profit'] = profile_data[i]['Profit'] - amount
                        profile_data[i]['Balance'] = original_balance - amount
                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(title=welcome_message, timestamp=datetime.utcnow(), color=0x00FF00)
                        embed.add_field(name='Your slot roll:', value=f'**>** {slots} **<**', inline=False)
                        embed.add_field(name=f'You win! Your new balance is {math.floor(original_balance + (amount * payout))} bagels! ({payout}x payout)', value=':)', inline=False)
                        profile_data[i]['Times'] = profile_data[i]['Times'] + 1
                        profile_data[i]['Win'] = profile_data[i]['Win'] + 1
                        profile_data[i]['Profit'] = profile_data[i]['Profit'] + math.floor(amount * payout)
                        profile_data[i]['Balance'] = math.floor(original_balance + (amount * payout))
                        await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title=welcome_message, timestamp=datetime.utcnow(), color=0x800080)
                    embed.add_field(name='Achievement Get!', value="How Did We Get Here?\n(if you're seeing this idk what you did lol)", inline=False)
                    await ctx.send(embed=embed)
                with open('profiles.json', 'w') as json_file:
                    json.dump(profile_data, json_file)
                return
        else:
            await ctx.send("You don't have a profile yet! Do `b.balance` to create one!")
            self.bet.reset_cooldown(ctx)
            return

    @bet.error
    async def command_name_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cd = round(error.retry_after)
            minutes = str(cd // 60)
            seconds = str(cd % 60)
            em = discord.Embed(title=f"Woah! Stop betting so fast!", description=f"Try again in {seconds} seconds.", color=0xFF0000)
            await ctx.send(embed=em)

    @commands.command(name='leaderboard', help="b.lb <times | win | lose | profit | bagels | negprofit>", aliases=['lb', 'leader'], pass_context=True)
    async def lb(self, ctx, *, lb: str=None):
        with open('profiles.json') as f:
            profile_data = json.load(f)
        percentages = {}
        if lb is None or lb.lower() not in ['times', 'win', 'lose', 'profit', 'bagels', 'negprofit']:
            lb = 'bagels'
        if(lb.lower() in ['times', 'win', 'lose', 'profit', 'bagels', 'negprofit']):
            if(lb.lower() == 'win' or lb.lower() == 'lose'):
                if(lb.lower() == 'win'):
                    lb_type = 'Win'
                else:
                    lb_type = 'Lose'
                for i in range(len(profile_data)):
                    try:
                        percent_correct = (profile_data[i][lb_type]/profile_data[i]['Times']) * 100
                    except ZeroDivisionError:
                        percent_correct = 0
                    percentages[str(profile_data[i]['Name'])] = percent_correct
                embedVar = discord.Embed(title=f"Highest {lb_type} Percentages", timestamp=datetime.utcnow(), color=0x00ff00)
                sorted_percentages = {k: v for k, v in sorted(percentages.items(), key=lambda item: item[1], reverse=True)}
                msg = ""
                place = 1
                if(len(sorted_percentages) < 10):
                    for key in sorted_percentages:
                        msg += str(place) + ". " + key + " (" + \
                            str(round(sorted_percentages[key], 2)) + f"%)\n"
                        place += 1
                else:
                    for key in itertools.islice(sorted_percentages, 10):
                        msg += str(place) + ". " + key + " (" + \
                            str(round(sorted_percentages[key], 2)) + f"%)\n"
                        place += 1
                embedVar.add_field(name="Placements", value=msg, inline=False)
                await ctx.send(embed=embedVar)
            elif(lb.lower() == 'times' or lb.lower() == 'profit' or lb.lower() == 'bagels'):
                if(lb.lower() == 'times'):
                    lb_type = 'Times'
                    end = 'times'
                    embedVar = discord.Embed(title="People who have gambled the most", timestamp=datetime.utcnow(), color=0x00ff00)
                elif(lb.lower() == 'profit'):
                    lb_type = 'Profit'
                    end = 'bagels'
                    embedVar = discord.Embed(title="Users who have made the most profit", timestamp=datetime.utcnow(), color=0x00ff00)
                else:
                    lb_type = 'Balance'
                    end = 'bagels'
                    embedVar = discord.Embed(title="Richest Users", timestamp=datetime.utcnow(), color=0x00ff00)
                for i in range(len(profile_data)):
                    for i in range(len(profile_data)):
                        number = profile_data[i][lb_type]
                        percentages[str(profile_data[i]['Name'])] = number
                sorted_percentages = {k: v for k, v in sorted(percentages.items(), key=lambda item: item[1], reverse=True)}
                msg = ""
                place = 1
                if(len(sorted_percentages) < 10):
                    for key in sorted_percentages:
                        msg += str(place) + ". " + key + " (" + \
                            str(round(sorted_percentages[key], 2)) + f" {end})\n"
                        place += 1
                else:
                    for key in itertools.islice(sorted_percentages, 10):
                        msg += str(place) + ". " + key + " (" + \
                            str(round(sorted_percentages[key], 2)) + f" {end})\n"
                        place += 1

                embedVar.add_field(name="Placements", value=msg, inline=False)
                await ctx.send(embed=embedVar)
            elif(lb.lower() == 'negprofit'):
                embedVar = discord.Embed(title="Users who have made the least profit", timestamp=datetime.utcnow(), color=0x00ff00)
                for i in range(len(profile_data)):
                    for i in range(len(profile_data)):
                        number = profile_data[i]['Profit']
                        percentages[str(profile_data[i]['Name'])] = number
                sorted_percentages = {k: v for k, v in sorted(percentages.items(), key=lambda item: item[1], reverse=False)}
                msg = ""
                place = 1
                if(len(sorted_percentages) < 10):
                    for key in sorted_percentages:
                        msg += str(place) + ". " + key + " (" + \
                            str(round(sorted_percentages[key], 2)) + f" bagels)\n"
                        place += 1
                else:
                    for key in itertools.islice(sorted_percentages, 10):
                        msg += str(place) + ". " + key + " (" + \
                            str(round(sorted_percentages[key], 2)) + f" bagels)\n"
                        place += 1

                embedVar.add_field(name="Placements", value=msg, inline=False)
                await ctx.send(embed=embedVar)


    @commands.command(name='beg', help="beg for money because you don't have any")
    @commands.cooldown(1, 240, commands.BucketType.user)
    async def beg(self, ctx):
        choice = random.randint(0,1)
        if(choice == 0):
            embed = discord.Embed(title='Begging', timestamp=datetime.utcnow(), color=0xFF0000)
            embed.add_field(name='Your begging did not work', value='No extra money for you', inline=False)
            await ctx.send(embed=embed)
        else:
            with open('profiles.json') as f:
                profile_data = json.load(f)
            for i in range(len(profile_data)):
                if(profile_data[i]['ID'] == ctx.author.id):
                    original_balance = int(profile_data[i]['Balance'])
                    money = random.randint(100, 500)
                    embed = discord.Embed(title='Begging', timestamp=datetime.utcnow(), color=0x00FF00)
                    embed.add_field(name=f"Your begging worked and you've received {money} bagels!", value=f'Your balance is now {original_balance + money}', inline=False)
                    profile_data[i]['Balance'] = profile_data[i]['Balance'] + money
                    await ctx.send(embed=embed)
                    with open('profiles.json', 'w') as json_file:
                        json.dump(profile_data, json_file)
                    return
            else:
                await ctx.send("You don't have a profile yet! Do `b.balance` to create one.")
                self.beg.reset_cooldown(ctx)
            

    @beg.error
    async def command_name_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cd = round(error.retry_after)
            minutes = str(cd // 60)
            seconds = str(cd % 60)
            em = discord.Embed(title=f"You can't just keep begging to get money!", description=f"Try again in {minutes} minutes and {seconds} seconds.", color=0xFF0000)
            await ctx.send(embed=em)
        
    async def cog_command_error(self, ctx, error):
        if not isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"**`ERROR in {os.path.basename(__file__)}:`** {type(error).__name__} - {error}")

    @commands.command(name="sim", help="b.sim <high | slots> <amount> <times>")
    async def sim(self, ctx, bet: str, amount: int, times: int):
        if(amount < 1):
            await ctx.reply('You can\'t simulate that number of attempts!')
            return
        if(bet not in ["high", "slots"]):
            await ctx.reply("You can only simulate 'high' or 'slots'!")
            return
        if(times > 1000):
            await ctx.reply("You can't simulate more than 1000 attempts (for now)!")
            return
        if(amount > 1000000):
            await ctx.reply("You can't simulate bets of more than 1,000,000 bagels (for now)!")
            return
        if(bet == 'high'):
            times_won = 0
            times_tied = 0
            times_lost = 0
            net_profit = 0
            for i in range(times):
                bagel_roll = random.randint(1,6)
                you_roll = random.randint(1,6)
                if(you_roll > bagel_roll):
                    percent_won = random.randint(50,100)
                    times_won += 1
                    net_profit += math.floor(amount * (percent_won/100))
                elif(you_roll < bagel_roll):
                    times_lost += 1
                    net_profit -= amount
                else:
                    times_tied += 1
            embed = discord.Embed(title="BagelBot High Simulation", timestamp=datetime.utcnow(), color=0x00FF00)
            embed.add_field(name='Times won', value=f"{times_won}/{times} ({round((times_won/times)*100, 2)}%)")
            embed.add_field(name='Times tied', value=f"{times_tied}/{times} ({round((times_tied/times)*100, 2)}%)")
            embed.add_field(name='Times lost', value=f"{times_lost}/{times} ({round((times_lost/times)*100, 2)}%)")
            embed.add_field(name='Net profit with consistent bet of {:,} bagels'.format(amount), value="{:,}".format(net_profit), inline=False)
            await ctx.reply(embed=embed)
            return
        elif(bet == 'slots'):
            if(amount > 5000):
                await ctx.reply("You can't bet more than 5000 bagels in the slot machine (not even in simulation)!")
                return
            emojis = ['⚽️', '🔴', '🔍', '🌍', '📸', '💵', '⌛️', '🏓']
            tables = [ { 'emoji': '⚽️', 'count': 2, 'payout': 1 }, { 'emoji': '🔍', 'count': 2, 'payout': 1 }, { 'emoji': '⌛️', 'count': 2, 'payout': 1.75 }, { 'emoji': '🏓', 'count': 2, 'payout': 1.75 }, { 'emoji': '🔴', 'count': 2, 'payout': 2 }, { 'emoji': '🌍', 'count': 2, 'payout': 2 }, { 'emoji': '💵', 'count': 2, 'payout': 2 }, { 'emoji': '📸', 'count': 2, 'payout': 2 }, { 'emoji': '🏓', 'count': 3, 'payout': 5 }, { 'emoji': '⚽️', 'count': 3, 'payout': 10 }, { 'emoji': '🔍', 'count': 3, 'payout': 10 }, { 'emoji': '🔴', 'count': 3, 'payout': 20 }, { 'emoji': '⌛️', 'count': 3, 'payout': 25 }, { 'emoji': '🌍', 'count': 3, 'payout': 50 }, { 'emoji': '📸', 'count': 3, 'payout': 75 }, { 'emoji': '💵', 'count': 3, 'payout': 250 }]
            times_won = 0
            times_lost = 0
            net_profit = 0
            for i in range(times):
                slots = ' '.join([random.choice(emojis), random.choice(emojis), random.choice(emojis)])     
                payout = 0
                for emoji in emojis:
                    instances = slots.count(emoji)
                    for table in tables:
                        if(emoji == table['emoji']):
                            if(instances == table['count']):
                                payout = table['payout']
                if(payout == 0):
                    times_lost += 1
                    net_profit -= amount
                else:
                    times_won += 1
                    net_profit += math.floor(amount * payout)
            embed = discord.Embed(title="BagelBot Slots Simulation", timestamp=datetime.utcnow(), color=0x00FF00)
            embed.add_field(name='Times won', value=f"{times_won}/{times} ({round((times_won/times)*100, 2)}%)")
            embed.add_field(name='Times lost', value=f"{times_lost}/{times} ({round((times_lost/times)*100, 2)}%)")
            embed.add_field(name='Net profit with consistent bet of {:,} bagels'.format(amount), value="{:,}".format(net_profit), inline=False)
            await ctx.reply(embed=embed)
            return


def setup(bot):
    bot.add_cog(Currency(bot))
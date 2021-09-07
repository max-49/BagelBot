# BagelBot

BagelBot is a discord bot that uses the discord.py API wrapper to give you the best gambling experience!

BagelBot is built using a heavily adapted version of ChemBot to allow for the best currency commands of any discord bot!

----------------------------------

If you want to use the already running instance of the bot, dm the bot `b.bal` to create a profile and then gamble using `b.bet <high | slots> <amount>` to gamble!

----------------------------------

If you want to run the bot yourself, here's how to do it!

1. Clone the repository (or download it)
2. pip install discord requests
3. Create a file called `profiles.json` and put the following into it:
```js
[]
```
5. Change `os.getenv("BAGEL_TOKEN")` in `main.py` to a bot token (You can look up how to get one if you don't know how)
6. Run `main.py` (no errors should arise, but you should be able to fix them if they do)
7. Run `b.help` to make and fill `commands.json` and run `b.bal` to make your profile
8. You should now have a running instance of BagelBot!

Important information: This bot is coded using discord.py version 1.7.3. If you have version 2.0 installed and want to run the bot, you might have to change some things (ex. avatar_url --> avatar.url)

-----------------------------------

thanks for reading this

rip discord.py :'(

[1]: https://img.shields.io/discord/881023409872597062?label=Join%20the%20Community%20Server%21&style=plastic
[2]: https://discord.gg/QtWafAvr

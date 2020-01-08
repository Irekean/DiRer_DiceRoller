import sys

import discord
import os.path
from os import path

from log import log
from dice import normal_roll, roll_full_attack
from prefix import PREFIX
from initiative import roll_initiative

# Log file, actually just used for console logging, not yet file logging


# old not used right now
full_attack_roll_OLD = r'\s*(?:(\d*d\d+)|(\d+))(?:([+-])((\d*)))(\/[+-]\d*)*(.*)'
#
# Every group is a single static bonus to add to a single roll.
# Example: 1d20+10/+5; group 1 is +10, group 2 is +5
DIFFERENT_BONUS_MATCHER = r'([\+-\-][0-9]+)'

# Initializing the discord bot:
client = discord.Client()


@client.event
async def on_ready():
    log("The bot is up and running!")
    # game = discord.Game("with the Yellow Sign")
    # await client.change_presence(status=discord.Status.idle, activity=game)


@client.event
async def on_message(message):
    try:
        if message.content.strip().lower().startswith(PREFIX + "usage") or message.content.lower().startswith("/help"):
            await message.channel.send("""Hi there, you can find the working functionality:
            - `""" + PREFIX + """r` : roll some dices using the format: `1d20+10`
            - `""" + PREFIX + """rf` : roll a D&D/Pathfinder full attack! Use the format: `1d20+15/+10/+5` WORK IN PROGRESS
            - `""" + PREFIX + """git` : get the GitHub project link
    
        If something does not work please open an issue on GitHub: https://github.com/Irekean/Discord-Dice-Roller/issues
            """)
        elif message.content.strip().lower().startswith(PREFIX + 'initiative'):
            await message.channel.send(roll_initiative(message))
        elif message.content.strip().lower().startswith(PREFIX + 'rf '):
            await message.channel.send(roll_full_attack(message))
        elif message.content.strip().lower().startswith(PREFIX + 'r ') or message.content.strip().lower().startswith(
                PREFIX + 'roll '):
            await message.channel.send(normal_roll(message))
        elif (message.content.lower().strip() + " ").startswith(PREFIX + "git "):
            await message.channel.send("The bot code is on GitHub: https://github.com/Irekean/Discord-Dice-Roller")
        elif message.author.id == 322449846336356363 and (
                message.content.strip().lower().startswith(PREFIX + 'kill') or message.content.strip().lower().startswith(
            PREFIX + 'stop')):
            await client.logout()
        elif message.content.strip().startswith(PREFIX):  # Always keep as last
            await message.channel.send("Need help? Try with `" + PREFIX + "help` or `" + PREFIX + "usage`")
    except:
        log.log("Unexpected error:" + sys.exc_info()[0])
        raise


# You need to put your token in a file named token.txt
if path.exists("token.txt"):
    bot_token = open("token.txt", "r")
    client.run(bot_token.read())
else:
    raise FileNotFoundError("File token.txt not found. You need to create it and paste in it your bot token.")

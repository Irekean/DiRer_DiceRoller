import sys

import discord
import os
from os import path
from pathlib import Path

from log import log
from dice import normal_roll, roll_full_attack
from prefix import PREFIX
from tinydb import TinyDB, Query

# Log file, actually just used for console logging, not yet file logging


# old not used right now
full_attack_roll_OLD = r'\s*(?:(\d*d\d+)|(\d+))(?:([+-])((\d*)))(\/[+-]\d*)*(.*)'
#
# Every group is a single static bonus to add to a single roll.
# Example: 1d20+10/+5; group 1 is +10, group 2 is +5
DIFFERENT_BONUS_MATCHER = r'([\+-\-][0-9]+)'

# Initializing the discord bot:
client = discord.Client()

#initializing the db
dbfile = Path("db.json")
dbfile.touch(exist_ok=True)
db = TinyDB('db.json')


@client.event
async def on_ready():
    log("The bot is up and running!")
    # game = discord.Game("with the Yellow Sign")
    # await client.change_presence(status=discord.Status.idle, activity=game)


@client.event
async def on_message(message):
    try:
        msg = message.content.strip().lower()
        if msg.startswith(PREFIX + "usage") or message.content.lower().startswith("/help"):
            await message.channel.send("""Hi there, you can find the working functionality:
            - `""" + PREFIX + """r` : roll some dices using the format: `1d20+10`
            - `""" + PREFIX + """gr` : roll some dices directly in the gm private chat, requires first the use of the command """ + PREFIX + """set gm
            - `""" + PREFIX + """set gm` : become the gm of the channel, you will receive privately all the gr commands sent in the actual channel
            - `""" + PREFIX + """git` : get the GitHub project link
    
        If something does not work please open an issue on GitHub: https://github.com/Irekean/DiRer_DiceRoller/issues
            """)
        elif msg.startswith(PREFIX + 'rf '):
            await message.channel.send(roll_full_attack(message))
        elif msg.startswith(PREFIX + 'r ') or msg.startswith(PREFIX + 'roll '):
            await message.channel.send(normal_roll(message))
        elif msg.startswith(PREFIX + 'set gm'):
            gms = Query()
            db.remove(gms.channel == message.channel.id)
            db.insert({'channel': message.channel.id, 'gm': message.author.id})
            await message.channel.send(message.author.display_name + " is the new GM of the channel")
        elif msg.startswith(PREFIX + 'gmroll ') or msg.startswith(PREFIX + 'gr '):
            gms = Query()
            gm = db.search(gms.channel == message.channel.id)
            if (len(gm) > 0):
                #user = await client.fetch_user(322449846336356363)
                user = await client.fetch_user(int(gm[0]['gm']))
                await user.send(normal_roll(message))
                await message.channel.send("Message sent to the GM")
            else:
                await message.channel.send("There is not GM setted in this channel. The GM should use the command " + PREFIX + "set gm")
        elif (message.content.lower().strip() + " ").startswith(PREFIX + "git "):
            await message.channel.send("The bot code is on GitHub: https://github.com/Irekean/DiRer_DiceRoller")
        elif message.author.id == 322449846336356363 and (
                msg.startswith(PREFIX + 'kill') or msg.startswith(PREFIX + 'stop')):
            await client.logout()
        elif msg.startswith(PREFIX):  # Always keep as last
            await message.channel.send("Need help? Try with `" + PREFIX + "help` or `" + PREFIX + "usage`")
    except:
        log("Unexpected error:" + sys.exc_info()[0])
        raise


# You need to put your token in a file named token.txt
if path.exists("token.txt"):
    bot_token = open("token.txt", "r")
    client.run(bot_token.read())
else:
    raise FileNotFoundError("File token.txt not found. You need to create it and paste in it your bot token.")

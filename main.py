import sys
import logging
import discord

from bot import Bot, get_response
from settings import get_value
from admin import is_this_admin

# Initializing the discord bot:
client = discord.Client()

# Starting the bot requires its token
try:
    client.run(get_value("CustomBotSettings", "BotToken"))
except:
    logging.error("Token not valid or not found in your conf.ini")
    sys.exit(1)


@client.event
async def on_ready():
    logging.info("The bot is up and running!")


@client.event
async def on_message(message):
    try:
        bot = Bot(client, message)
        msg = bot.get_response()
        if msg is not None:
            message.channel.send(msg)
    except:
        logging.error("Unexpected error: ", sys.exc_info()[0])

import discord
import logging
import sys

from bot import Bot
from settings import get_value

# Initializing the discord bot:
client = discord.Client()


@client.event
async def on_ready():
    logging.info("The bot is up and running!")


@client.event
async def on_message(message):
    #try:
    bot = Bot(client, message)
    msg = bot.get_response()
    if msg is not None:
        await message.channel.send(msg)
    #except Exception as err:
     #   logging.error("Unexpected error: " + str(err))


# Starting the bot requires its token
try:
    client.run(get_value("CustomBotSettings", "BotToken"))
except KeyError as err:
    logging.error(str(err))
    sys.exit(1)

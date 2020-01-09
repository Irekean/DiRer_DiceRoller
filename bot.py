import sys

import discord

from dice import roll_full_attack, Dice
from prefix import PREFIX
from settings import get_value
from admin import is_this_admin


class Bot:
    def __init__(self, client, message):
        self.client = client
        self.message = message
        self.content = message.content.strip()
        self.admin = is_this_admin(message.author.id)

    def get_response(self):
        if self.admin:
            if self.__is_message_command("kill") or self.__is_message_command("stop"):
                await self.client.logout()
                return None
            elif self.__is_message_command("update"):
                return "You got me! But I am still developing this part."

    def __is_message_command(self, command):
        return self.message.lower().startswith(command)


def get_response(message, admin_right):
    if message.content.strip().lower().startswith(PREFIX + "usage") or message.content.lower().startswith("/help"):
        await message.channel.send("""Hi there, you can find the working functionality:
        - `""" + PREFIX + """r` : roll some dices using the format: `1d20+10`
        - `""" + PREFIX + """rf` : roll a D&D/Pathfinder full attack! Use the format: `1d20+15/+10/+5` WORK IN PROGRESS
        - `""" + PREFIX + """git` : get the GitHub project link

    If something does not work please open an issue on GitHub: """ + get_value("CustomBotUpdates",
                                                                               "UpdateRepository") + """/issues""")
    elif message.content.strip().lower().startswith(PREFIX + 'rf '):
        await message.channel.send(roll_full_attack(message))
    elif message.content.strip().lower().startswith(PREFIX + 'r ') or message.content.strip().lower().startswith(
            PREFIX + 'roll '):
        result = Dice(message).roll()
        await message.channel.send(result)
    elif (message.content.lower().strip() + " ").startswith(PREFIX + "git "):
        await message.channel.send(
            "The bot code is on GitHub: " + get_value("CustomBotUpdates", "UpdateRepository"))
    elif is_this_admin(message.author.id) and (
            message.content.strip().lower().startswith(
                PREFIX + 'kill') or message.content.strip().lower().startswith(
        PREFIX + 'stop')):
        await client.logout()
    elif message.content.strip().startswith(PREFIX):  # Always keep as last
        await message.channel.send("Need help? Try with `" + PREFIX + "help` or `" + PREFIX + "usage`")

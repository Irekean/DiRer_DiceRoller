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
            if self.__is_command__("kill") or self.__is_command__("stop"):
                await self.client.logout()
                return None
            elif self.__is_command__("update"):
                return "You got me! But I am still developing this part."

        if self.__is_command__("usage") or self.__is_command__("help"):
            return """Hi there, you can find the working functionality:
        - `""" + PREFIX + """r` : roll some dices using the format: `1d20+10`
        - `""" + PREFIX + """rf` : roll a D&D/Pathfinder full attack! Use the format: `1d20+15/+10/+5` WORK IN PROGRESS
        - `""" + PREFIX + """git` : get the GitHub project link

    If something does not work please open an issue on GitHub: """ + get_value("CustomBotUpdates",
                                                                               "UpdateRepository") + """/issues"""
        elif self.__is_command__("rf "):
            return roll_full_attack(self.message)
        elif self.__is_command__("r ") or self.__is_command__("roll "):
            return Dice(self.message).roll()
        elif self.__is_command__("git"):
            return "The bot code is on GitHub: " + get_value("CustomBotUpdates", "UpdateRepository")
        elif self.__is_command__(""):
            return "Need help? Try with `" + PREFIX + "help` or `" + PREFIX + "usage`"

    def __is_command__(self, command):
        return self.message.lower().startswith(PREFIX + command)

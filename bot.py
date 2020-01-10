import platform
import os
import sys
import subprocess
from subprocess import CalledProcessError
import logging

from dice import roll_full_attack, Dice
from prefix import PREFIX
from settings import get_value
from admin import is_this_admin


def __run_command__(command):
    value = os.system(command)
    if value is not 0:
        raise RuntimeError("Error code " + str(value))
    else:
        return True


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
                return self.__update__()

        if self.__is_command__("usage") or self.__is_command__("help"):
            return """Hi there, you can find the working functionality:
        - `""" + PREFIX + """r` : roll some dices using the format: `1d20+10`
        - `""" + PREFIX + """rf` : roll a D&D/Pathfinder full attack! Use the format: `1d20+15/+10/+5` WORK IN PROGRESS
        - `""" + PREFIX + """git` : get the GitHub project link

    If something does not work please open an issue on GitHub: """ + get_value("CustomBotUpdates",
                                                                               "CodeRepository") + """/issues"""
        elif self.__is_command__("rf "):
            return roll_full_attack(self.message)
        elif self.__is_command__("r ") or self.__is_command__("roll "):
            return Dice(self.message).roll()
        elif self.__is_command__("git"):
            return "The bot code is on GitHub: " + get_value("CustomBotUpdates", "CodeRepository")
        elif self.__is_command__(""):
            # Keep as last
            return "Need help? Try with `" + PREFIX + "help` or `" + PREFIX + "usage`"

    def __is_command__(self, command):
        return self.message.lower().startswith(PREFIX + command)

    def __update__(self):
        if len(self.content.split(" ")) == 1:
            branch = get_value("CustomBotUpdates", "UpdateBranch")
        else:
            branch = self.content[self.content.find(" ") + 1:]

        last_command_error = ""
        try:
            last_command_error = "Could not fetch, the bot code is not connected to a git repository."
            __run_command__("git fetch --all")
            last_command_error = "Could not find the branch " + branch + "."
            __run_command__("git checkout " + branch)
            last_command_error = "Could not update."
            __run_command__("git update")
        except Exception as e:
            error = last_command_error + " " + str(e)
            logging.error(error)
            return error

        self.client.logout()
        output_process = None
        try:
            system = platform.system()
            if system is "Windows":
                output_process = subprocess.check_output("pip install -r requirements.txt && python main.py")
                if output_process is 0:
                    sys.exit(0);
            elif system is "Linux" or system is "Darwin":
                output_process = subprocess.check_output("pip3 install -r requirements.txt && python3 main.py")
        except CalledProcessError as err:
            logging.error(str(err) + " Output code: " + output_process)
            self.client.run()
            return "Error while trying to restart, go check the log."

import logging
import os
import platform
import subprocess
from subprocess import CalledProcessError
import sys

from dice import roll_full_attack, Dice
from prefix import PREFIX
from settings import get_value
from admin import is_this_admin


def __run_command__(command):
    value = os.system(command)
    if value != 0:
        raise RuntimeError("Error code " + str(value))
    else:
        return True


class Bot:
    def __init__(self, client, message):
        self.client = client
        self.message = message
        self.content = message.content.strip()
        self.admin = is_this_admin(message.author.id)

    async def get_response(self):
        if self.admin:
            if self.__is_command__("kill") or self.__is_command__("stop"):
                self.client.logout()
                return None
            elif self.__is_command__("update"):
                await self.__update__()
                return None

        if self.__is_command__("usage") or self.__is_command__("help"):
            return """Hi there, you can find the working functionality:
        - `""" + PREFIX + """r` : roll some dices using the format: `1d20+10`
        - `""" + PREFIX + """rf` : roll a D&D/Pathfinder full attack! Use the format: `1d20+15/+10/+5` WORK IN PROGRESS
        - `""" + PREFIX + """git` : get the GitHub project link

    If something does not work please open an issue on GitHub: """ + get_value("CustomBotUpdates",
                                                                               "CodeRepository") + """/issues"""
        elif self.__is_command__("rf "):
            return Dice(self.message, "rf").roll()
        elif self.__is_command__("r "):
            return Dice(self.message, "r").roll()
        elif self.__is_command__("roll "):
            return Dice(self.message, "roll").roll()
        elif self.__is_command__("git"):
            return "The bot code is on GitHub: " + get_value("CustomBotUpdates", "CodeRepository")
        elif self.__is_command__(""):
            # Keep it at last
            return "Need help? Try with `" + PREFIX + "help` or `" + PREFIX + "usage`"

    def __is_command__(self, command):
        return self.content.lower().startswith(PREFIX + command)

    async def __update__(self):
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
            __run_command__("git pull")
        except Exception as e:
            error = last_command_error + " " + str(e)
            logging.error(error)
            return error

        return_code = None
        try:
            system = platform.system()
            if system == "Windows":
                child = subprocess.Popen("pip install -r requirements.txt", stdout=subprocess.PIPE)
                streamdata = child.communicate()[0]
                return_code = child.returncode
                if return_code == 0:
                    child = subprocess.Popen("python main.py", stdout=subprocess.PIPE)
                    streamdata = child.communicate()[0]
                    return_code = child.returncode
                    if return_code == 0:
                        await self.client.logout()
                        sys.exit(0)
            elif system == "Linux" or system == "Darwin":
                return_code = subprocess.check_output("pip3 install -r requirements.txt && python3 main.py")
        except CalledProcessError as err:
            logging.error(str(err) + " Output code: " + return_code)
            return "Error while trying to restart, go check the log."
        return return_code

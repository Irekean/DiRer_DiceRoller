from prefix import PREFIX
from settings import get_value


class Messages:

    def __init__(self):
        pass

    def get_help(self):
        return """Hi there, you can find the working functionality:
        - `""" + PREFIX + """r` : roll some dices using the format: `1d20+10`
        - `""" + PREFIX + """rf` : roll a D&D/Pathfinder full attack! Use the format: `1d20+15/+10/+5` WORK IN PROGRESS
        - `""" + PREFIX + """git` : get the GitHub project link

    If something does not work please open an issue on GitHub: """ + get_value("CustomBotUpdates",
                                                                               "CodeRepository") + "/issues"

    def get_code(self):
        return "The bot code is on GitHub: " + get_value("CustomBotUpdates", "CodeRepository")

    def get_wrong_command(self):
        return "Need help? Try with `" + PREFIX + "help` or `" + PREFIX + "usage`"

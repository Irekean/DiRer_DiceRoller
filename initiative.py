from json_handler import get_initiative
from dice import roll_dices


def roll_initiative(message):
    if " " in message.content.strip().lower():
        return "Working on it"  # Handle the possibility to have different list
    init_list = get_initiative(message.author.id)
    if init_list is None:
        return "You haven't saved any initiative yet!"
    ret = ""
    for single_init in init_list['init']:
        ret += single_init['name'] + ": "
        value = roll_dices("1d20")
        value = value.replace("(", "").replace(")", "").replace("+", "")
        value = int(value) + int(single_init['value']) if single_init['value'] >= 0 else -int(single_init['value'])
        value = str(value).replace("(", "").replace(")", "").replace("+", "")
        value = value + "." + str(single_init['value'])
        ret += value + "\n"
    return ret

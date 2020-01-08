import random
import re

from prefix import PREFIX

#
# Used to check if the input string is valid for a full attack:
FULL_ATTACK_WITH_TEXT = r'[0-9]{1,2}d[0-9]{1,2}([+,-][0-9]{1,2})(/[+,-][0-9]{1,2})+[a-z]+'
FULL_ATTACK_WITHOUT_TEXT = r'[0-9]{1,2}d[0-9]{1,2}([+,-][0-9]{1,2})(/[+,-][0-9]{1,2})+'
#
# Normal roll matcher:
NORMAL_ROLL = r'([+-]\d{1,3}d\d{1,3}|[+-]\d{1,3})'
#
# Check if someone is trying to roll more than 2 digit number
VALIDATE_ROLL_TOO_MANY_DICE = r'([0-9]{3,3}d)'
VALIDATE_ROLL_DICE_TOO_BIG = r'(d[0-9]{4,4})'


def roll_dices(dice):  # Accepts a *d* value where an * is a number
    results = []
    sign = check_sign(dice[0])
    rolls = dice.replace("-", "").replace("+", "").split('d')
    # print(rolls)
    for number_of_roll in range(0, int(rolls[0])):
        random.seed()
        results.append(random.randint(1, int(rolls[1])))
    # print(results)
    ret = ""
    for i in results:
        ret = "{}+{}".format(ret, i)
    ret = ret[1:]
    ret = "{}({})".format(sign, ret)
    return ret


def check_sign(sign):  # check if I get a valid sign, if not it's a +
    if sign != "-":
        sign = "+"
    return sign


def roll_full_attack(message):
    message = message.content.strip()
    roll = message.lower().replace(PREFIX + "rf", "").replace(" ", "")
    if re.compile(FULL_ATTACK_WITH_TEXT).match(roll) or re.compile(FULL_ATTACK_WITHOUT_TEXT).match(roll):
        return "Still working on it"
    else:
        return "Incorrect input, if you need help try with: `" + PREFIX + "help` or `" + PREFIX + "usage`"


def normal_roll(message):
    #
    # Checking if there are too many dice or dices are too big
    #
    text_included = ""
    text_included = message.content.replace("/r ", "").replace("/roll ", "")
    message_content = message.content.replace(PREFIX + "r ", "/r +").replace(PREFIX + "roll ", "/roll +").replace("+d", "+1d").replace("-d", "-1d").strip()
    pattern = re.compile(VALIDATE_ROLL_TOO_MANY_DICE)
    pattern.match(message_content)
    if pattern.search(message_content) is not None:
        return "You can't roll more than 99 dice"
    pattern = re.compile(VALIDATE_ROLL_DICE_TOO_BIG)
    pattern.match(message_content)
    a = pattern.search(message_content)
    if pattern.search(message_content) is not None:
        return "You can't roll dice with more than 999 faces"
    #
    # Actual Rolling:
    #
    to_be_splitted = message_content.lower().split(" ")
    roll = to_be_splitted[1]
    mtch_iterator = re.finditer(NORMAL_ROLL, roll)
    # print(mtch_iterator)
    final_return = ""
    int_return = 0
    for matchNum, match in enumerate(mtch_iterator, start=1):
        # print(match)
        if "d" in match.group():
            results = roll_dices(match.group().strip())
            final_return += results
            int_return = int_return + eval(results)
        else:
            int_return = int_return + eval(match.group().strip())
            final_return += match.group().strip()
    if final_return == "":
        return message_content.replace(PREFIX + "r", "").replace(" ", "").strip()

    final_return = "{} = **{}**".format(final_return, int_return)
    if final_return[0] == "+":
        return message.author.mention + " rolled: " + text_included + "\n" + final_return[1:]
    return final_return

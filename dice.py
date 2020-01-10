import random
import re

from prefix import PREFIX

VALIDATE_ROLL_TOO_MANY_DICE = r'([0-9]{5,5}d)'
VALIDATE_ROLL_DICE_TOO_BIG = r'(d[0-9]{5,5})'
NORMAL_ROLL = r'([+-]\d{1,5}d\d{1,5}|[+-]\d+)'


class Dice:
    def __init__(self, message, mode):
        self.message = message
        self.mode = mode
        clean_text = self.message.content.replace(PREFIX + mode + " ", "+")
        self.clean_text = clean_text.replace("+d", "+1d").replace("-d", "-1d").strip()
        self.message_text = self.clean_text[self.clean_text.find(" ") + 1:].strip()
        self.tag_user = self.message.author.mention
        self.final_return = ""
        self.final_result = 0

    def roll(self):
        are_too_big = self.__are_dices_too_big__()
        if are_too_big:
            return are_too_big

        if self.mode == "r" or self.mode == "roll":
            return self.__normal_roll__()
        elif self.mode == "rf":
            return self.__full_attack__()

    def __normal_roll__(self):
        match_iterator = re.finditer(NORMAL_ROLL, self.clean_text)
        self.final_return = ""
        self.final_result = 0
        for matchNum, match in enumerate(match_iterator, start=1):
            self.__evaluate_roll__(match)

        if self.final_return == "":
            return "Wat"

        ret_message = "{} = **{}**".format(self.final_return, self.final_result)
        if ret_message[0] == "+":
            return self.tag_user + " rolled: " + self.message_text + "\n" + ret_message[1:]
        else:
            return self.tag_user + " rolled: " + self.message_text + "\n" + ret_message

    def __evaluate_roll__(self, match):
        if "d" in match.group():
            results = roll_dices(match.group().strip())
            self.final_return += results
            self.final_result = self.final_result + eval(results)
        else:
            self.final_result = self.final_result + eval(match.group().strip())
            self.final_return += match.group().strip()

    def __full_attack__(self):
        roll_full_attack(self.clean_text)

    def __are_dices_too_big__(self):
        pattern = re.compile(VALIDATE_ROLL_TOO_MANY_DICE)
        pattern.match(self.clean_text)
        if pattern.search(self.clean_text) is not None:
            return "You can't roll more than 9999 dice"
        pattern = re.compile(VALIDATE_ROLL_DICE_TOO_BIG)
        pattern.match(self.clean_text)
        if pattern.search(self.clean_text) is not None:
            return "You can't roll dice with more than 9999 faces"


# Used to check if the input string is valid for a full attack:
FULL_ATTACK_WITH_TEXT = r'[0-9]{1,2}d[0-9]{1,2}([+,-][0-9]{1,2})(/[+,-][0-9]{1,2})+[a-z]+'
FULL_ATTACK_WITHOUT_TEXT = r'[0-9]{1,2}d[0-9]{1,2}([+,-][0-9]{1,2})(/[+,-][0-9]{1,2})+'


def roll_dices(dice):  # Accepts a *d* value where an * is a number
    results = []
    sign = check_sign(dice[0])
    rolls = dice.replace("-", "").replace("+", "").split('d')
    for number_of_roll in range(0, int(rolls[0])):
        random.seed()
        results.append(random.randint(1, int(rolls[1])))
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

import time
import datetime


def get_actual_time():
    ts = time.time()  # Just a seconds timestamp
    st = datetime.datetime.fromtimestamp(ts).strftime(
        '%Y-%m-%d %H:%M:%S')  # Converting it to human time
    return st


def log(value):
    ts = time.time()  # Just a seconds timestamp
    st = datetime.datetime.fromtimestamp(ts).strftime(
        '%Y-%m-%d %H:%M:%S')  # Converting it to human time
    print("[ {} ] : {}".format(st, value))


def print_actual_time():
    ts = time.time()  # Just a seconds timestamp
    st = datetime.datetime.fromtimestamp(ts).strftime(
        '%Y-%m-%d %H:%M:%S')  # Converting it to human time
    print("[ {} ] : ".format(st), end='')

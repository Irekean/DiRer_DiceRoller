import configparser
import os

setup_done = False
config = configparser.ConfigParser()


def __setup():
    global setup_done
    if not setup_done:
        global config
        config.read(os.getcwd() + '\conf.ini')
        setup_done = True


def get_value(section, key):
    __setup()
    global config
    return config[section][key]

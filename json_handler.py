import json


def get_initiative(user_id):
    try:
        with open("data/initiative.json", "r") as read_file:
            init_data = json.load(read_file)
    except FileNotFoundError:
        return "Couldn't find the JSON file. You need to create data/initiative.json in the root of your project"
    init_list = None
    for user_init in init_data['users_initiative']:
        if user_init['user'] == user_id:
            init_list = user_init
            break
    if init_list is not None:
        return init_list
    else:
        return None



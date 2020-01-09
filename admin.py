from settings import get_value

setup_done = False
admin_list = None


# Returns the list of the ids of the admin
def get_admin_list():
    global admin_list
    __setup()
    return admin_list


# Check if the variable is in the list of the admin
def is_this_admin(possible_admin):
    global admin_list
    __setup()
    return possible_admin in admin_list


def __setup():
    global setup_done
    if not setup_done:
        global admin_list
        admin_list = __populate_list()
        setup_done = True


def __populate_list():
    admin_raw = get_value("DEFAULT", "Admins")
    return admin_raw.replace(" ", "").split(",")

class Admin:
    def __init__(self, client, message):
        pass
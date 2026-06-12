CURRENT_ROLE = "admin"


def get_current_role():

    return CURRENT_ROLE


def set_current_role(
    role
):

    global CURRENT_ROLE

    CURRENT_ROLE = role
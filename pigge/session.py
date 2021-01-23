"""Handling user sessions"""

USER = None


def parent_user(u):
    global USER
    USER = u


def get_name():
    return USER.parent_name


def get_acc_status():
    return USER.acc_status


def get_ID():
    return USER.parent_id


def limit_transaction(val):
    try:
        USER.restrict_bal = val
        return True
    except NameError:
        return False

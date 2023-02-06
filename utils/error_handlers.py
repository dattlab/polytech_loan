import re

from ui.dialogs_ui import invalidEmailError


def isNotEmpty(*args):
    for i in args:
        if i == "":
            return False
    return True


def isInDB():
    # TODO: Check DB function
    return False


def gwaAccepted(gwa):
    if gwa in {1.0, 1.25, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 4.0, 5.0}:
        if 1.75 >= gwa >= 1.0:
            return True
    return False


def isFloat(userInput):
    try:
        float(userInput)
    except ValueError:
        return False
    return True


def isValidEmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, email):
        return True
    return False

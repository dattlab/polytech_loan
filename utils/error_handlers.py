import json
import os.path
import re

from utils.constants import DATA_FILE
from ui.dialogs_ui import invalidEmailError, invalidCredentials


def isNotEmpty(*args):
    for i in args:
        if i == "":
            return False
    return True


def isInDB(studentNumber):
    with open(DATA_FILE, "r") as f:
        accounts = json.load(f)
    if studentNumber in accounts:
        return True
    return False


def noLoan(studentNumber):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        if data[studentNumber]["loanAmount"] is None:
            return True
        return False
    return True


def validCredentials(studentNumber, *args):
    with open(DATA_FILE, "r") as f:
        accounts = json.load(f)
    for a in args:
        if accounts[studentNumber][a[0]] != a[1]:
            invalidCred = invalidCredentials()
            invalidCred.exec()
            return False
    return True


def gwaAccepted(gwa):
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
    invalidEmailError().raiseError()
    return False

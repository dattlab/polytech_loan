def isNotEmpty(*args):
    for i in args:
        if i == "":
            return False
    return True


def isInDB():
    # TODO: Check DB function
    return False


def gwaAccepted(gwa):
    # TODO: Check GWA function
    return True


def isFloat(userInput):
    try:
        float(userInput)
    except ValueError:
        return False
    return True

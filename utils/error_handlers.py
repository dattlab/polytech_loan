import re

from ui.dialogs_ui import invalidEmailError, invalidCredentials, invalidStudentNumError
from utils.helpers import DB_CONNECT, DB_CURSOR


def isNotEmpty(*args):
    for i in args:
        if i == "":
            return False
    return True


def isInDB(studentNumber):
    DB_CURSOR.execute(
        f"""SELECT COUNT(1) FROM student
            WHERE student_number = '{studentNumber}'
        """
    )

    res = DB_CURSOR.fetchall()[0][0]

    return True if res == 1 else False


def noLoan(studentNumber):
    DB_CURSOR.execute(
        f"""SELECT COUNT(1) FROM loan
            WHERE student_number = '{studentNumber}'
        """
    )

    res = DB_CURSOR.fetchall()[0][0]

    DB_CONNECT.commit()

    return True if not res else False


def validCredentials(studentNumber, *args):
    DB_CURSOR.execute(
        f"""SELECT COUNT(1) FROM student
            WHERE student_number = '{studentNumber}'
            AND name = '{args[0]}'
            AND email = '{args[1]}'
            AND passwd = '{args[2]}'
            AND college = '{args[3]}'
            AND course = '{args[4]}'
        """
    )

    res = DB_CURSOR.fetchall()[0][0]

    DB_CONNECT.commit()

    if res:
        return True
    invalidCredentials().exec()
    return False


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
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if re.fullmatch(regex, email):
        return True
    invalidEmailError().exec()
    return False


def isValidStudentNum(studentNumber):
    regex = r"20\d{2}-\d{5}-MN-0"
    if re.fullmatch(regex, studentNumber):
        return True
    invalidStudentNumError().exec()
    return False

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

from utils.constants import *


class errorInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(ERROR_INPUT_DIALOG_UI, self)
        self.pushButton.clicked.connect(self.close)


class invalidCredentials(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(INVALID_CRED_DIALOG_UI, self)
        self.pushButton.clicked.connect(self.close)


class wrongPasswd(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(WRONG_PASSWD_DIALOG_UI, self)
        self.pushButton.clicked.connect(self.close)


class applySuccessDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(APPLY_SUCCESS_DIALOG_UI, self)
        self.pushButton.clicked.connect(self.close)


class applyRejectedDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(APPLY_REJECTED_DIALOG_UI, self)
        self.pushButton.clicked.connect(self.close)


class exceedMaxError(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(EXCEED_MAX_AMOUNT_DIALOG_UI, self)
        self.pushButton.clicked.connect(self.close)


class invalidEmailError(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(INVALID_EMAIL_DIALOG_UI, self)
        self.pushButton.clicked.connect(self.close)

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

from utils.constants import (
    ERROR_INPUT_DIALOG_UI,
    APPLY_SUCCESS_DIALOG_UI,
    APPLY_REJECTED_DIALOG_UI,
    EXCEED_MAX_AMOUNT_DIALOG_UI,
    INVALID_EMAIL_DIALOG_UI
)


class errorInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(ERROR_INPUT_DIALOG_UI, self)
        self.pushButton.clicked.connect(self.close)

    def raiseError(self):
        self.exec()


class applySuccessDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(APPLY_SUCCESS_DIALOG_UI, self)
        self.pushButton.clicked.connect(self.close)

    def raiseDialog(self):
        self.exec()


class applyRejectedDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(APPLY_REJECTED_DIALOG_UI, self)
        self.pushButton.clicked.connect(self.close)

    def raiseError(self):
        self.exec()


class exceedMaxError(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(EXCEED_MAX_AMOUNT_DIALOG_UI, self)
        self.pushButton.clicked.connect(self.close)

    def raiseError(self):
        self.exec()


class invalidEmailError(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi(INVALID_EMAIL_DIALOG_UI, self)
        self.pushButton.clicked.connect(self.close)

    def raiseError(self):
        self.exec()

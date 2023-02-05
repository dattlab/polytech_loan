import sys

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow
)
from PyQt5.uic import loadUi

from ui.main_window_ui import Ui_MainWindow
from utils.error_handlers import *
from utils.helpers import *


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def raiseInputError(self):
        dialog = errorInputDialog(self)
        dialog.exec()

    def raiseApplySuccess(self):
        dialog = applySuccessDialog(self)
        dialog.exec()

    def gotoDashboardPage1(self):
        pass

    def gotoDashboardPage2(self):
        pass

    def gotoApplyPage1(self):
        pass

    def gotoApplyPage2(self):
        pass

    def gotoSummaryPage(self):
        pass

    def gotoLoginPage(self):
        pass


class errorInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ui/error_input.ui", self)


class applySuccessDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ui/apply_success_dialog.ui", self)


def main() -> None:
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

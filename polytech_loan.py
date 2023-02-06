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
        self.loginBtn.clicked.connect(self.gotoMainPage)
        self.pushButton.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.loginPage))
        self.applyBtn.clicked.connect(self.gotoApplyPage1)
        self.applyBtn_2.clicked.connect(self.gotoApplyPage2)
        self.applyConfirmBtn.clicked.connect(self.gotoSummaryPage)
        self.applyCancelBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.loginPage))
        self.applyConfirmBtn_3.clicked.connect(self.raiseApplySuccess)

    def raiseInputError(self):
        dialog = errorInputDialog(self)
        dialog.exec()

    def raiseApplySuccess(self):
        dialog = applySuccessDialog(self)
        dialog.exec()
        self.stackedWidget.setCurrentWidget(self.loginPage)

    def gotoMainPage(self):
        if isInDB():
            self.stackedWidget.setCurrentWidget(self.withLoanPage)
        else:
            self.stackedWidget.setCurrentWidget(self.noLoanPage)

    def gotoApplyPage1(self):
        self.stackedWidget.setCurrentWidget(self.applyPage)

    def gotoApplyPage2(self):
        self.stackedWidget.setCurrentWidget(self.applyPage2)

    def gotoSummaryPage(self):
        self.stackedWidget.setCurrentWidget(self.summaryPage)


class errorInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ui/error_input.ui", self)
        self.pushButton.clicked.connect(self.close)


class applySuccessDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ui/apply_success_dialog.ui", self)
        self.pushButton.clicked.connect(self.close)


def main() -> None:
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

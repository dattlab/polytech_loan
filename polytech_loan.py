import sys

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog
)

from ui.main_window_ui import Ui_MainWindow
from ui.dialogs_ui import *
from utils.error_handlers import *
from utils.helpers import *


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.loginBtn.clicked.connect(self.gotoMainPage)
        self.logOutBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.loginPage))
        self.logOutBtn_2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.loginPage))
        self.applyBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.applyPage))
        self.applyCancelBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.noLoanPage))
        self.applyBtn_2.clicked.connect(self.gotoApplyPage2)
        self.applyCancelBtn_2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.applyPage))
        self.applyConfirmBtn.clicked.connect(self.gotoSummaryPage)
        self.applyCancelBtn_3.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.applyPage2))
        self.applyConfirmBtn_3.clicked.connect(self.raiseApplySuccess)
        self.applySaveCopyBtn.clicked.connect(self.saveToPdf)

    def raiseInputError(self):
        dialog = errorInputDialog(self)
        dialog.exec()

    def raiseApplySuccess(self):
        dialog = applySuccessDialog(self)
        dialog.exec()
        self.stackedWidget.setCurrentWidget(self.loginPage)

    def gotoMainPage(self):
        name = self.nameLineEdit.text()
        studentNum = self.studentNumLineEdit.text()
        course = self.courseComboBox.currentText()
        if isNotEmpty(name, studentNum, course):
            self.nameLabel.setText(name)
            self.studentNumLabel.setText(studentNum)
            self.courseLabel.setText(course)
            if isInDB():
                self.stackedWidget.setCurrentWidget(self.withLoanPage)
            else:
                self.stackedWidget.setCurrentWidget(self.noLoanPage)
        else:
            self.raiseInputError()

    def gotoApplyPage2(self):
        gwa = self.gwaApplyInput.text()
        loanPurpose = self.loanPurposeInput.text()
        if isNotEmpty(gwa, loanPurpose):
            if isFloat(gwa) and gwaAccepted(float(gwa)):
                self.stackedWidget.setCurrentWidget(self.applyPage2)
            else:
                rejectDialog = applyRejectedDialog()
                rejectDialog.exec()
        else:
            self.raiseInputError()

    def gotoSummaryPage(self):
        desiredAmount = self.loanAmountInput.text()
        maxLoanAmount = self.maxAmountDisplay.text()
        if isNotEmpty(desiredAmount):
            if isFloat(desiredAmount) and desiredAmount <= maxLoanAmount:
                self.renderSummary()
                self.stackedWidget.setCurrentWidget(self.summaryPage)
            else:
                exceedMaxDialog = exceedMaxError()
                exceedMaxDialog.exec()
        else:
            self.raiseInputError()

    def renderSummary(self):
        ...

    def saveToPdf(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Copy", "loan_summary.pdf", "PDF (*.pdf)", options=options)
        filePath = filePath.replace("/", "\\\\")
        createPdf(filePath)


def main() -> None:
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

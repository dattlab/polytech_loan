import sys

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QWidget
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
        self.logOutBtn.clicked.connect(self.gotoLoginPage)
        self.logOutBtn_2.clicked.connect(self.gotoLoginPage)
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
        self.gotoLoginPage()

    def gotoMainPage(self):
        name = self.nameLineEdit.text()
        email = self.emailLineEdit.text()
        studentNum = self.studentNumLineEdit.text()
        course = self.courseComboBox.currentText()
        if isNotEmpty(name, email, studentNum):
            self.nameLabel.setText(name)
            self.studentNumLabel.setText(studentNum)
            self.courseLabel.setText(course)
            if isInDB():
                self.gotoDashboard()
            else:
                self.gotoEmptyDashboard()
        else:
            self.raiseInputError()

    def gotoEmptyDashboard(self):
        self.stackedWidget.setCurrentWidget(self.noLoanPage)

    def gotoDashboard(self):
        self.stackedWidget.setCurrentWidget(self.withLoanPage)

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

    def gotoLoginPage(self):
        self.clearLoginInput()
        self.stackedWidget.setCurrentWidget(self.loginPage)

    def clearLoginInput(self):
        self.nameLineEdit.setText("")
        self.emailLineEdit.setText("")
        self.studentNumLineEdit.setText("")

    def renderSummary(self):
        ...

    def saveToPdf(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filePath, _ = QFileDialog.getSaveFileName(None, "Save Copy", "loan_summary.pdf", "PDF (*.pdf)", options=options)
        filePath = filePath.replace("/", "\\\\")
        createPdf(filePath)
        self.gotoLoginPage()


def main() -> None:
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

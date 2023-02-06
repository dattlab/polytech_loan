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
        self.logOutBtn.clicked.connect(self.gotoLoginPage)
        self.logOutBtn_2.clicked.connect(self.gotoLoginPage)
        self.applyBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.applyPage))
        self.applyCancelBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.noLoanPage))
        self.applyBtn_2.clicked.connect(self.gotoApplyPage2)
        self.applyCancelBtn_2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.applyPage))
        self.applyConfirmBtn.clicked.connect(self.gotoSummaryPage)
        self.applyCancelBtn_3.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.applyPage2))
        self.applyConfirmBtn_3.clicked.connect(lambda: self.raisApplySuccess())
        self.applySaveCopyBtn.clicked.connect(self.saveToPdf)

        self.paymentDurationInput.currentTextChanged.connect(self.updateApplyPage2)
        self.paymentMethodInput.currentTextChanged.connect(self.updateApplyPage2)

    def gotoMainPage(self):
        name = self.nameLineEdit.text()
        email = self.emailLineEdit.text()
        studentNum = self.studentNumLineEdit.text()
        college = self.collegeComboBox.currentText()
        course = self.courseComboBox.currentText()
        if isNotEmpty(name, email, studentNum):
            if isValidEmail(email):
                self.nameLabel.setText(name)
                self.studentNumLabel.setText(studentNum)
                self.courseLabel.setText(course)
                if isInDB():
                    self.displayLoanStatus()
                    self.gotoDashboard()
                else:
                    storeInDB(name, email, studentNum, college, course)
                    self.gotoEmptyDashboard()
            else:
                invalidEmailError().raiseError()
                return
        else:
            errorInputDialog().raiseError()

    def gotoEmptyDashboard(self):
        self.stackedWidget.setCurrentWidget(self.noLoanPage)

    def displayLoanStatus(self):
        ...

    def gotoDashboard(self):
        self.stackedWidget.setCurrentWidget(self.withLoanPage)

    def gotoApplyPage2(self):
        gwa = self.gwaApplyInput.text()
        loanPurpose = self.loanPurposeInput.text()
        if isNotEmpty(gwa, loanPurpose):
            if isFloat(gwa) and gwaAccepted(float(gwa)):
                gwa = float(gwa)
                updateDB(
                    self.studentNumLabel.text(),
                    ("gwa", gwa),
                    ("loanPurpose", loanPurpose),
                    ("honor", determineHonor(gwa))
                )
                self.updateApplyPage2()
                self.stackedWidget.setCurrentWidget(self.applyPage2)
            else:
                applyRejectedDialog().raiseError()
        else:
            errorInputDialog().raiseError()

    def updateApplyPage2(self):
        paymentDuration = self.paymentDurationInput.currentText()

        if self.typeLabel.text()[-1] == "A":
            self.maxAmountDisplay.setText("15000")
        else:
            self.maxAmountDisplay.setText("10000")

        if paymentDuration == "3":
            if self.typeLabel.text()[-1] == "A":
                self.interestRateDisplay.setText("5%")
            else:
                self.interestRateDisplay.setText("7%")
        if paymentDuration == "6":
            if self.typeLabel.text()[-1] == "A":
                self.interestRateDisplay.setText("8%")
            else:
                self.interestRateDisplay.setText("10%")
        if paymentDuration == "12":
            if self.typeLabel.text()[-1] == "A":
                self.interestRateDisplay.setText("10%")
            else:
                self.interestRateDisplay.setText("15%")

    def gotoSummaryPage(self):
        desiredAmount = self.loanAmountInput.text()
        maxLoanAmount = self.maxAmountDisplay.text()
        if isNotEmpty(desiredAmount):
            if isFloat(desiredAmount) and desiredAmount <= maxLoanAmount:
                self.renderSummary()
                self.stackedWidget.setCurrentWidget(self.summaryPage)
            else:
                exceedMaxError().raiseError()
        else:
            errorInputDialog().raiseError()

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

    def raisApplySuccess(self):
        applySuccessDialog().raiseDialog()
        self.gotoLoginPage()


def main() -> None:
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

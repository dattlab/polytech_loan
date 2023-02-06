import sys
import json

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
        if isNotEmpty(name, email, studentNum):
            if isValidEmail(email):
                self.checkCredentials(name, email, studentNum)
            else:
                invalidEmailError().raiseError()
                return
        else:
            errorInputDialog().raiseError()

    def checkCredentials(self, name, email, studentNum):
        college = self.collegeComboBox.currentText()
        course = self.courseComboBox.currentText()
        if os.path.exists(DATA_FILE) and isInDB(studentNum):
            if validCredentials(studentNum, ("name", name), ("email", email), ("college", college), ("course", course)):
                if noLoan(studentNum):
                    self.renderInfoHeader()
                    self.gotoEmptyDashboard()
                else:
                    self.nameLabel_2.setText(name)
                    self.studentNumLabel_2.setText(studentNum)
                    self.courseLabel_2.setText(course)
                    self.renderDashboardStat()
                    self.gotoDashboard()
            else:
                invalidCred = invalidCredentials()
                invalidCred.exec()
        else:
            self.renderInfoHeader()
            storeInDB(name, email, studentNum, college, course)
            self.gotoEmptyDashboard()

    def gotoEmptyDashboard(self):
        self.stackedWidget.setCurrentWidget(self.noLoanPage)

    def renderInfoHeader(self):
        self.nameLabel.setText(self.nameLineEdit.text())
        self.studentNumLabel.setText(self.studentNumLineEdit.text())
        self.courseLabel.setText(self.courseComboBox.currentText())

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
                self.updateType()
                self.updateApplyPage2()
                self.stackedWidget.setCurrentWidget(self.applyPage2)
            else:
                applyRejectedDialog().raiseError()
        else:
            errorInputDialog().raiseError()

    def updateType(self):
        if 1.50 < float(self.gwaApplyInput.text()) <= 1.75:
            self.typeLabel.setText("TYPE B")

    def updateApplyPage2(self):
        paymentDuration = self.paymentDurationInput.currentText()

        if self.typeLabel.text()[-1] == "A":
            self.maxAmountDisplay.setText("Php 15000")
        else:
            self.maxAmountDisplay.setText("Php 10000")

        if paymentDuration == "3":
            if self.paymentMethodInput.currentText()[8] == "d":
                self.interestRateDisplay.setText("5%")
            else:
                self.interestRateDisplay.setText("7%")
        if paymentDuration == "6":
            if self.paymentMethodInput.currentText()[8] == "d":
                self.interestRateDisplay.setText("8%")
            else:
                self.interestRateDisplay.setText("10%")
        if paymentDuration == "12":
            if self.paymentMethodInput.currentText()[8] == "d":
                self.interestRateDisplay.setText("10%")
            else:
                self.interestRateDisplay.setText("15%")

    def gotoSummaryPage(self):
        desiredAmount = self.loanAmountInput.text()
        maxLoanAmount = float(self.maxAmountDisplay.text()[4:])
        interestRate = float(self.interestRateDisplay.text()[:-1]) / 100
        paymentDuration = int(self.paymentDurationInput.currentText())
        if isNotEmpty(desiredAmount):
            if isFloat(desiredAmount) and float(desiredAmount) <= maxLoanAmount:
                desiredAmount = float(desiredAmount)
                interestAmount = desiredAmount * interestRate
                totalDebt = desiredAmount + interestAmount
                monthlyPayment = round(totalDebt / paymentDuration, 2)
                updateDB(
                    self.studentNumLabel.text(),
                    ("loanAmount", desiredAmount),
                    ("interestAmount", interestAmount),
                    ("paymentDuration", f"{paymentDuration} months"),
                    ("totalDebt", totalDebt),
                    ("monthlyPayment", monthlyPayment),
                    ("paymentMode", self.paymentMethodInput.currentText())
                )
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

    def renderDashboardStat(self):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        data = data[self.studentNumLabel.text()]
        self.gwaDisplay.setText(str(data["gwa"]))
        self.honorDisplay.setText(data["honor"])
        self.loanAmountDisplay.setText(str(data["loanAmount"]))
        self.interestAmountDisplay.setText(str(data["interestAmount"]))
        self.paymentDurationDisplay.setText(str(data["paymentDuration"]))
        self.totalDebtDisplay.setText(str(data["totalDebt"]))
        self.monthPaymentDisplay.setText(str(data["monthlyPayment"]))
        self.modePaymentDisplay.setText(data["paymentMode"])
        self.purposeDisplay.setText(data["loanPurpose"])

    def renderSummary(self):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        data = data[self.studentNumLabel.text()]
        self.nameSummDisplay.setText(data["name"])
        self.emailSummDisplay.setText(data["email"])
        self.studentNumSummDisplay.setText(self.studentNumLabel.text())
        self.collegeSummDisplay.setText(data["college"])
        self.courseSummDisplay.setText(data["course"])
        self.gwaSummDisplay.setText(str(data["gwa"]))
        self.honorSummDisplay.setText(data["honor"])
        self.loanAmountSummDisplay.setText(str(data["loanAmount"]))
        self.interestAmountSummDisplay.setText(str(data["interestAmount"]))
        self.paymentDurationSummDisplay.setText(str(data["paymentDuration"]))
        self.totalDebtSummDisplay.setText(str(data["totalDebt"]))
        self.monthPaymentSummDisplay.setText(str(data["monthlyPayment"]))
        self.modePaymentSummDisplay.setText(data["paymentMode"])
        self.purposeSummDisplay.setText(data["loanPurpose"])

    def saveToPdf(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filePath, _ = QFileDialog.getSaveFileName(None, "Save Copy", "loan_summary.pdf", "PDF (*.pdf)", options=options)
        filePath = filePath.replace("/", "\\\\")
        createPdf(filePath, self.studentNumLabel.text())
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

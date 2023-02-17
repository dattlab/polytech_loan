from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QLineEdit
)

from ui.dialogs_ui import *
from ui.main_window_ui import Ui_MainWindow
from utils.error_handlers import *
from utils.helpers import *


class Window(QMainWindow, Ui_MainWindow):
    """
    Controller of Main Window UI
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Polytech-Loan")

        self.passwdLineEdit.setEchoMode(QLineEdit.Password)

        self.loginBtn.clicked.connect(self.gotoMainPage)
        self.logOutBtn.clicked.connect(self.gotoLoginPage)
        self.logOutBtn_2.clicked.connect(self.gotoLoginPage)
        self.applyBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.applyPage))
        self.applyCancelBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.noLoanPage))
        self.applyBtn_2.clicked.connect(self.gotoApplyPage2)
        self.applyCancelBtn_2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.applyPage))
        self.applyConfirmBtn.clicked.connect(self.gotoSummaryPage)
        self.applyCancelBtn_3.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.applyPage2))
        self.applyConfirmBtn_3.clicked.connect(lambda: self.raiseApplySuccess())
        self.applySaveCopyBtn.clicked.connect(self.saveToPdf)

        self.paymentDurationInput.currentTextChanged.connect(self.updateApplyPage2)
        self.paymentMethodInput.currentTextChanged.connect(self.updateApplyPage2)

    def gotoMainPage(self) -> None:
        name = self.nameLineEdit.text()
        email = self.emailLineEdit.text()
        passwd = self.passwdLineEdit.text()
        studentNumber = self.studentNumLineEdit.text()
        college = self.collegeComboBox.currentText()
        course = self.courseComboBox.currentText()
        if isNotEmpty(name, email, studentNumber) and isValidEmail(email) and \
                isValidStudentNum(studentNumber):
            if os.path.exists(DATA_FILE) and isInDB(studentNumber):
                if validCredentials(studentNumber, name, email, passwd,
                                    college, course):
                    if noLoan(studentNumber):
                        self.renderInfoHeader()
                        self.gotoEmptyDashboard()
                    else:
                        self.nameLabel_2.setText(name)
                        self.studentNumLabel_2.setText(studentNumber)
                        self.courseLabel_2.setText(course)

                        DB_CURSOR.execute(f"""SELECT * FROM students
                                                WHERE student_number = '{studentNumber}'
                                            """)
                        data = DB_CURSOR.fetchall()[0]
                        DB_CONNECT.commit()

                        self.renderDashboardStat(data)
                        self.gotoDashboard()
            else:
                self.renderInfoHeader()
                storeInDB(name, email, studentNumber, passwd, college, course)
                self.gotoEmptyDashboard()

    def gotoEmptyDashboard(self) -> None:
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
                self.updateType()
                self.updateApplyPage2()
                self.stackedWidget.setCurrentWidget(self.applyPage2)
            else:
                applyRejectedDialog().exec()
        else:
            errorInputDialog().exec()

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

    def gotoSummaryPage(self) -> None:
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
                gwa = float(self.gwaApplyInput.text())
                updateLoanDetails(
                    self.studentNumLabel.text(),
                    gwa, determineHonor(gwa),
                    desiredAmount,
                    interestAmount,
                    paymentDuration,
                    totalDebt,
                    monthlyPayment,
                    self.paymentMethodInput.currentText(),
                    self.loanPurposeInput.text(),
                    'Pending'
                )
                self.renderSummary()
                self.stackedWidget.setCurrentWidget(self.summaryPage)
            else:
                exceedMaxError().exec()
        else:
            errorInputDialog().exec()

    def gotoLoginPage(self) -> None:
        self.clearLoginInput()
        self.stackedWidget.setCurrentWidget(self.loginPage)

    def clearLoginInput(self) -> None:
        self.nameLineEdit.setText("")
        self.emailLineEdit.setText("")
        self.studentNumLineEdit.setText("")
        self.passwdLineEdit.setText("")

    def renderDashboardStat(self, data) -> None:
        self.statusLabel.setText(data[15])
        self.gwaDisplay.setText(str(data[6]))
        self.honorDisplay.setText(data[7])
        self.loanAmountDisplay.setText(str(data[8]))
        self.interestAmountDisplay.setText(str(data[9]))
        self.paymentDurationDisplay_2.setText(str(data[10]))
        self.totalDebtDisplay.setText(str(data[11]))
        self.monthPaymentDisplay.setText(str(data[12]))
        self.modePaymentDisplay.setText(data[13])
        self.purposeDisplay.setText(data[14])

    def renderSummary(self) -> None:
        studentNumber = self.studentNumLabel.text()
        DB_CURSOR.execute(f"""SELECT * FROM students
                WHERE student_number = '{studentNumber}'
            """)

        data = DB_CURSOR.fetchall()[0]

        DB_CONNECT.commit()

        self.nameSummDisplay.setText(data[0])
        self.emailSummDisplay.setText(data[1])
        self.studentNumSummDisplay.setText(data[2])
        self.collegeSummDisplay.setText(data[4])
        self.courseSummDisplay.setText(data[5])
        self.gwaSummDisplay.setText(str(data[6]))
        self.honorSummDisplay.setText(data[7])
        self.loanAmountSummDisplay.setText(str(data[8]))
        self.interestAmountSummDisplay.setText(str(data[9]))
        self.paymentDurationSummDisplay.setText(str(data[10]))
        self.totalDebtSummDisplay.setText(str(data[11]))
        self.monthPaymentSummDisplay.setText(str(data[12]))
        self.modePaymentSummDisplay.setText(data[13])
        self.purposeSummDisplay.setText(data[14])

    def saveToPdf(self) -> None:
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filePath, _ = QFileDialog.getSaveFileName(None, "Save Copy", "loan_summary.pdf", "PDF (*.pdf)", options=options)
        createPdf(filePath, self.studentNumLabel.text())
        self.gotoLoginPage()

    def raiseApplySuccess(self) -> None:
        applySuccessDialog().exec()
        self.gotoLoginPage()


def main() -> None:
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    appStart = app.exec()
    DB_CONNECT.close()
    sys.exit(appStart)


if __name__ == '__main__':
    main()

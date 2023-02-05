import sys

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow
)
from PyQt5.uic import loadUi

from ui.main_window_ui import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    def raiseInputError(self):
        dialog = errorInputDialog(self)
        dialog.exec()


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

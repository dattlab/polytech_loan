import getpass
import os
import sys

# DATA FILE PATH
USER_NAME = getpass.getuser()
if os.name == "nt":
    DATA_FILE_PATH = f"C:\\Users\\{USER_NAME}\\AppData\\Local\\Polytech-Loan"
    DATA_FILE = f"{DATA_FILE_PATH}\\polytech-loan.db"
else:
    DATA_FILE_PATH = f"/home/{USER_NAME}/.local/share/Polytech-Loan"
    DATA_FILE = f"/home/{USER_NAME}/.local/share/Polytech-Loan/polytech-loan.db"

if not os.path.exists(DATA_FILE_PATH):
    os.makedirs(DATA_FILE_PATH)

# DIALOG UI FILES PATH
bundle_dir = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))

ERROR_INPUT_DIALOG_UI = os.path.abspath(os.path.join(bundle_dir, "../ui/error_input.ui"))
APPLY_SUCCESS_DIALOG_UI = os.path.abspath(os.path.join(bundle_dir, "../ui/apply_success_dialog.ui"))
APPLY_REJECTED_DIALOG_UI = os.path.abspath(os.path.join(bundle_dir, "../ui/apply_rejected_dialog.ui"))
EXCEED_MAX_AMOUNT_DIALOG_UI = os.path.abspath(os.path.join(bundle_dir, "../ui/exceed_max_amount_dialog.ui"))
INVALID_EMAIL_DIALOG_UI = os.path.abspath(os.path.join(bundle_dir, "../ui/invalid_email_dialog.ui"))
INVALID_STUDENTNUM_DIALOG_UI = os.path.abspath(os.path.join(bundle_dir, "../ui/invalid_studentnum_dialog.ui"))
INVALID_CRED_DIALOG_UI = os.path.abspath(os.path.join(bundle_dir, "../ui/invalid_cred_dialog.ui"))
WRONG_PASSWD_DIALOG_UI = os.path.abspath(os.path.join(bundle_dir, "../ui/wrong_passwd_dialog.ui"))

INTERFACE_FONT = "Helvetica"
BG_MAROON_0 = "rgb(91, 6, 22)"
BG_MAROON_1 = " rgb(136, 0, 0)"

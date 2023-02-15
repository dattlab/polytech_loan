import getpass
import sys
import os

# DATA FILE PATH
USER_NAME = getpass.getuser()
if os.name == "nt":
    DATA_FILE_PATH = f"C:\\Users\\{USER_NAME}\\AppData\\Local\\Polytech-Loan"
    DATA_FILE = f"{DATA_FILE_PATH}\\data.json"
else:
    DATA_FILE_PATH = f"/home/{USER_NAME}/.local/share/Polytech-Loan"
    DATA_FILE = f"/home/{USER_NAME}/.local/share/Polytech-Loan/data.json"

if not os.path.exists(DATA_FILE_PATH):
    os.makedirs(DATA_FILE_PATH)

# DIALOG UI FILES PATH
bundle_dir = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))

ERROR_INPUT_DIALOG_UI = os.path.abspath(os.path.join(bundle_dir, "error_input.ui"))
APPLY_SUCCESS_DIALOG_UI = os.path.abspath(os.path.join(bundle_dir, "apply_success_dialog.ui"))
APPLY_REJECTED_DIALOG_UI = os.path.abspath(os.path.join(bundle_dir, "apply_rejected_dialog.ui"))
EXCEED_MAX_AMOUNT_DIALOG_UI = os.path.abspath(os.path.join(bundle_dir, "exceed_max_amount_dialog.ui"))
INVALID_EMAIL_DIALOG_UI = os.path.abspath(os.path.join(bundle_dir, "invalid_email_dialog.ui"))
INVALID_CRED_DIALOG_UI = os.path.abspath(os.path.join(bundle_dir, "invalid_cred_dialog.ui"))

INTERFACE_FONT = "Helvetica"
BG_MAROON_0 = "rgb(91, 6, 22)"
BG_MAROON_1 = " rgb(136, 0, 0)"

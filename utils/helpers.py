import json
import os

from fpdf import FPDF

from utils.constants import INTERFACE_FONT


def exceedsMaxAmount():
    # TODO: Check loan amount input function
    pass


def determineHonor(gwa):
    if gwa >= 1.5:
        return "President's Lister"
    return "Dean's Lister"


def createPdf(filePath):
    pdf = FPDF()
    pdf.set_font(INTERFACE_FONT, size=15)
    pdf.add_page()
    pdf.multi_cell(
        200, 10,
        "**Polytech-Loan**\n" +
        "**Loan Summary Details**\n\n" +
        "                                                   **Iskolar Details**\n" +
        f"**Name:** \n" +
        f"**Email:** \n" +
        f"**Student Number:** \n" +
        f"**College:** =\n" +
        f"**Course:** \n" +
        f"**GWA:** \n" +
        f"**Honor:** \n\n" +
        "                                                   **Loan Details**\n" +
        f"**Loan amount:** \n" +
        f"**Interest amount:** \n" +
        f"**Payment duration:** \n" +
        f"**Total debt:** \n" +
        f"**Monthly payment:** \n" +
        f"**Mode of payment:** \n" +
        f"**Purpose:** \n\n",
        align='L',
        markdown=True
    )
    print(filePath)
    pdf.output(filePath)


def write_json(data: dict) -> None:
    """Writes the data in user database"""
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4, separators=(",", ": "), sort_keys=True)


def storeInDB(*args):
    if os.path.exists("data.json"):
        with open("data.json", "r") as data:
            existing_data = json.load(data)
    else:
        newAccount = {
            args[2]: {
                "name": args[0],
                "email": args[1],
                "college": args[3],
                "course": args[4],
                "gwa": None,
                "honor": None,
                "loanAmount": None,
                "interestAmount": None,
                "paymentDuration": None,
                "totalDebt": None,
                "monthlyPayment": None,
                "paymentMode": None,
                "loanPurpose": None
            }
        }
        write_json(newAccount)


def updateDB(studentNumber, *args):
    with open("data.json", "r") as f:
        data = json.load(f)

    for i in args:
        keyToBeUpdated = i[0]
        valueUpdate = i[1]
        data[studentNumber][keyToBeUpdated] = valueUpdate
    write_json(data)

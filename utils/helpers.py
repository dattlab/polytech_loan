import bcrypt
import json
import os

from fpdf import FPDF

from utils.constants import INTERFACE_FONT, DATA_FILE


def determineHonor(gwa):
    if gwa >= 1.5:
        return "President's Lister"
    return "Dean's Lister"


def createPdf(filePath, studentNumber):
    pdf = FPDF()
    pdf.set_font(INTERFACE_FONT, size=15)
    pdf.add_page()

    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    data = data[studentNumber]
    pdf.multi_cell(
        200, 10,
        "**Polytech-Loan**\n" +
        "**Loan Summary Details**\n\n" +
        "                                                   **Iskolar Details**\n" +
        f"**Name:** {data['name']}\n" +
        f"**Email:** {data['email']}\n" +
        f"**Student Number:** {studentNumber}\n" +
        f"**College:** {data['college']}\n" +
        f"**Course:** {data['course']}\n" +
        f"**GWA:** {data['gwa']}\n" +
        f"**Honor:** {data['honor']}\n\n" +
        "                                                   **Loan Details**\n" +
        f"**Loan amount:** {data['loanAmount']}\n" +
        f"**Interest amount:** {data['interestAmount']}\n" +
        f"**Payment duration:** {data['paymentDuration']}\n" +
        f"**Total debt:** {data['totalDebt']}\n" +
        f"**Monthly payment:** {data['monthlyPayment']}\n" +
        f"**Mode of payment:** {data['paymentMode']}\n" +
        f"**Purpose:** {data['loanPurpose']}\n\n",
        align='L',
        markdown=True
    )
    pdf.output(filePath)


def write_json(newData):
    with open(DATA_FILE, "w") as f:
        json.dump(newData, f, indent=4, separators=(",", ": "), sort_keys=True)


def hash_str(s):
    return bcrypt.hashpw(s, bcrypt.gensalt()).decode("utf-8").replace("'", '"')


def storeInDB(*args):
    passwd = hash_str(args[2].encode("utf-8"))
    newAccount = {
        args[3]: {
            "name": args[0],
            "email": args[1],
            "passwd": passwd,
            "college": args[4],
            "course": args[5],
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
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            existing_data = json.load(f)
        existing_data[args[2]] = newAccount[args[2]]
        write_json(existing_data)
    else:
        write_json(newAccount)


def updateDB(studentNumber, *args):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    for i in args:
        keyToBeUpdated = i[0]
        valueUpdate = i[1]
        data[studentNumber][keyToBeUpdated] = valueUpdate
    write_json(data)

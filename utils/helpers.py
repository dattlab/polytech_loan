import sqlite3

from fpdf import FPDF

from utils.constants import INTERFACE_FONT, DATA_FILE

DB_CONNECT = sqlite3.connect(DATA_FILE)
DB_CURSOR = DB_CONNECT.cursor()

DB_CURSOR.execute("""CREATE TABLE IF NOT EXISTS students (
    name text,
    email text,
    student_number text,
    passwd text,
    college text,
    course text,
    gwa real,
    honor text,
    loan_amount real,
    interest_amount real,
    payment_duration integer,
    total_debt real,
    monthly_payment real,
    payment_mode text,
    loan_purpose text,
    loan_status text
)
""")

DB_CONNECT.commit()


def determineHonor(gwa):
    if 1 <= gwa <= 1.5:
        return "President's Lister"
    return "Dean's Lister"


def createPdf(filePath, studentNumber):
    pdf = FPDF()
    pdf.set_font(INTERFACE_FONT, size=15)
    pdf.add_page()

    DB_CURSOR.execute(f"""SELECT * FROM students
        WHERE student_number = '{studentNumber}'
    """)

    data = DB_CURSOR.fetchall()[0]

    pdf.multi_cell(
        200, 10,
        "**Polytech-Loan**\n" +
        "**Loan Summary Details**\n\n" +
        "                                                   **Iskolar Details**\n" +
        f"**Name:** {data[0]}\n" +
        f"**Email:** {data[1]}\n" +
        f"**Student Number:** {data[2]}\n" +
        f"**College:** {data[4]}\n" +
        f"**Course:** {data[5]}\n" +
        f"**GWA:** {data[6]}\n" +
        f"**Honor:** {data[7]}\n\n" +
        "                                                   **Loan Details**\n" +
        f"**Status:** {data[15].upper()}\n" +
        f"**Loan amount:** {data[8]}\n" +
        f"**Interest amount:** {data[9]}\n" +
        f"**Payment duration:** {data[10]}\n" +
        f"**Total debt:** {data[11]}\n" +
        f"**Monthly payment:** {data[12]}\n" +
        f"**Mode of payment:** {data[13]}\n" +
        f"**Purpose:** {data[14]}\n\n",
        align='L',
        markdown=True
    )
    pdf.output(filePath)


def storeInDB(*args):
    DB_CURSOR.execute(f"""INSERT INTO students
    		VALUES (
    			'{args[0]}','{args[1]}','{args[2]}','{args[3]}','{args[4]}',
    			'{args[5]}',0,'',0,0,0,0,0,'','',''
    		)
    	""")

    DB_CONNECT.commit()


def updateLoanDetails(studentNumber, *args):
    DB_CURSOR.execute(f"""UPDATE students
    		SET (
    		    gwa, honor, loan_amount, interest_amount, payment_duration,
    			total_debt, monthly_payment, payment_mode, loan_purpose, loan_status
    		) = (?,?,?,?,?,?,?,?,?,?)
    		WHERE student_number = '{studentNumber}'
    	""", args)

    DB_CONNECT.commit()

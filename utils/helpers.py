import pyodbc

from fpdf import FPDF

from utils.constants import INTERFACE_FONT


DB_CONNECT = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                            'Server=DATWIN\SQLEXPRESS;'
                            'Database=PolytechLoan;'
                            'Trusted_Connection=yes;')
DB_CURSOR = DB_CONNECT.cursor()

DB_CURSOR.execute(
    """
    IF NOT EXISTS (SELECT * FROM sys.objects
                   WHERE object_id = OBJECT_ID(N'dbo.student')
                   AND type in (N'U'))
        CREATE TABLE student (
            student_number NVARCHAR(15) NOT NULL,
            name NVARCHAR(50) NOT NULL,
            email NVARCHAR(50) NOT NULL,
            passwd NVARCHAR(50) NOT NULL,
            college NVARCHAR(50) NOT NULL,
            course NVARCHAR(50) NOT NULL,
            gwa NUMERIC(3,2),
            honor NVARCHAR(50),
            
            CONSTRAINT PK_student_number PRIMARY KEY (student_number)
        )
    IF NOT EXISTS (SELECT * FROM sys.objects
                   WHERE object_id = OBJECT_ID(N'dbo.loan')
                   AND type in (N'U'))
        CREATE TABLE loan (
            student_number NVARCHAR(15) NOT NULL,
            loan_amount REAL,
            interest_amount REAL,
            payment_duration SMALLINT,
            total_debt REAL,
            monthly_payment REAL,
            payment_mode NVARCHAR(20),
            loan_purpose TEXT,
            loan_status TEXT
            
            CONSTRAINT PK_loan_student_number PRIMARY KEY (student_number),
            CONSTRAINT FK_loan_student_number FOREIGN KEY (student_number)
                REFERENCES student (student_number)
                ON DELETE CASCADE
        )
    """
)
DB_CONNECT.commit()


def determineHonor(gwa):
    if 1 <= gwa <= 1.5:
        return "President's Lister"
    return "Dean's Lister"


def createPdf(filePath, studentNumber):
    pdf = FPDF()
    pdf.set_font(INTERFACE_FONT, size=15)
    pdf.add_page()

    # TODO: migrate to MSSQL
    DB_CURSOR.execute(
        f"""SELECT * FROM students
        WHERE student_number = '{studentNumber}'
    """
    )
    data_user = DB_CURSOR.fetchall()[0]

    DB_CURSOR.execute(
        f"""SELECT * FROM loan
        WHERE student_number = '{studentNumber}'
        """
    )
    data_loan = DB_CURSOR.fetchall()[0]

    pdf.multi_cell(
        200,
        10,
        "**Polytech-Loan**\n"
        + "**Loan Summary Details**\n\n"
        + "                                                   **Iskolar Details**\n"
        + f"**Name:** {data_user[1]}\n"
        + f"**Email:** {data_user[2]}\n"
        + f"**Student Number:** {data_user[0]}\n"
        + f"**College:** {data_user[4]}\n"
        + f"**Course:** {data_user[5]}\n"
        + f"**GWA:** {data_user[6]}\n"
        + f"**Honor:** {data_user[7]}\n\n"
        + "                                                   **Loan Details**\n"
        + f"**Status:** {data_loan[8].upper()}\n"
        + f"**Loan amount:** {data_loan[1]}\n"
        + f"**Interest amount:** {data_loan[2]}\n"
        + f"**Payment duration:** {data_loan[3]}\n"
        + f"**Total debt:** {data_loan[4]}\n"
        + f"**Monthly payment:** {data_loan[5]}\n"
        + f"**Mode of payment:** {data_loan[6]}\n"
        + f"**Purpose:** {data_loan[7]}\n\n",
        align="L",
        markdown=True,
    )
    pdf.output(filePath)


def storeInDB(*args):
    DB_CURSOR.execute(
        f"""
        INSERT INTO student (student_number, name, email, passwd, college, course)
        VALUES ('{args[2]}', '{args[0]}', '{args[1]}', '{args[3]}', '{args[4]}', '{args[5]}')
        """
    )

    DB_CONNECT.commit()


def updateLoanDetails(studentNumber, *args):
    DB_CURSOR.execute(
        f"""
        UPDATE student
        SET gwa = {args[0]}, honor = '{args[1]}'
        WHERE student_number = '{studentNumber}'
        """
    )
    DB_CONNECT.commit()

    DB_CURSOR.execute(
        f"""
        IF EXISTS (SELECT * FROM loan WHERE student_number = '{studentNumber}')
        BEGIN
            UPDATE loan
            SET loan_amount = {args[2]},
                interest_amount = {args[3]},
                payment_duration = {args[4]},
                total_debt = {args[5]},
                monthly_payment = {args[6]},
                payment_mode = '{args[7]}',
                loan_purpose = '{args[8]}',
                loan_status = '{args[9]}'
            WHERE student_number = '{studentNumber}';
        END
        ELSE
        BEGIN
            INSERT INTO loan (
                student_number, loan_amount, interest_amount, payment_duration,
                total_debt, monthly_payment, payment_mode, loan_purpose, loan_status
            )
            VALUES (
                '{studentNumber}', {args[2]}, {args[3]}, {args[4]},
                {args[5]}, {args[6]}, '{args[7]}', '{args[8]}', '{args[9]}'
            );
        END
        """
    )
    DB_CONNECT.commit()

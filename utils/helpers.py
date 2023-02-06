from fpdf import FPDF

from utils.constants import INTERFACE_FONT


def exceedsMaxAmount():
    # TODO: Check loan amount input function
    pass


def createPdf(filePath):
    pdf = FPDF()
    pdf.set_font(INTERFACE_FONT, size=15)
    pdf.multi_cell(
        200, 10,
        "**Polytech-Loan**\n"
        "**Loan Summary Details**\n\n" +
        "                                                   **Iskolar Details**\n"
        f"**Name:** {}\n" +
        f"**Email:** {}\n" +
        f"**Student Number:** {}\n" +
        f"**College:** {}\n" +
        f"**Course:** {}\n" +
        f"**GWA:** {}\n" +
        f"**Honor:** {}\n\n" +
        "                                                   **Loan Details**\n"
        f"**Loan amount:** {}\n" +
        f"**Interest amount:** {}\n" +
        f"**Payment duration:** {}\n" +
        f"**Total debt:** {}\n" +
        f"**Monthly payment:** {}\n" +
        f"**Mode of payment:** {}\n" +
        f"**Purpose:** {}\n\n",
        align='L',
        markdown=True
    )
    pdf.output(filePath)


def storeInDB():
    # TODO: Function for storing data in DB
    pass

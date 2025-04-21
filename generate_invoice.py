from fpdf import FPDF
from datetime import datetime
from fpdf.enums import XPos, YPos

# === Helper: Auto-Increment Invoice Number ===
def get_next_invoice_number(counter_file="invoice_counter.txt"):
    try:
        with open(counter_file, "r") as file:
            number = int(file.read().strip())
    except (FileNotFoundError, ValueError):
        number = 1

    with open(counter_file, "w") as file:
        file.write(str(number + 1))

    return str(number).zfill(4)  # Example: 0001

# === CONFIGURATION ===
YOUR_NAME = "Your Name or Business"
YOUR_ADDRESS = "123 Your St, City, State ZIP"
YOUR_EMAIL = "youremail@example.com"
LOGO_PATH = "assets/logo.png"  # Optional: path to your logo file

class InvoicePDF(FPDF):
    def header(self):
        if LOGO_PATH:
            try:
                self.image(LOGO_PATH, 10, 8, 33)
            except:
                pass
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "INVOICE", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="R")

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_invoice(data):
    pdf = InvoicePDF()
    pdf.add_page()

    # Your info
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 10, YOUR_NAME, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 10, YOUR_EMAIL, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(10)

    # Client info
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Bill To:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 10, data["client_name"], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 10, data["client_email"], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)

    # Invoice meta
    pdf.cell(0, 10, f"Invoice #: {data['invoice_number']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 10, f"Date: {data['invoice_date']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(10)

    # Table header
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(80, 10, "Description", border=1)
    pdf.cell(30, 10, "Qty", border=1)
    pdf.cell(40, 10, "Rate", border=1)
    pdf.cell(40, 10, "Total", border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Line items
    pdf.set_font("Helvetica", "", 12)
    grand_total = 0
    for item in data["items"]:
        total = item["qty"] * item["rate"]
        grand_total += total
        pdf.cell(80, 10, item["desc"], border=1)
        pdf.cell(30, 10, str(item["qty"]), border=1)
        pdf.cell(40, 10, f"${item['rate']:.2f}", border=1)
        pdf.cell(40, 10, f"${total:.2f}", border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Optional tax
    # if data.get("tax_rate"):
    #     tax_amount = grand_total * (data["tax_rate"] / 100)
    #     pdf.cell(150, 10, "Tax", border=1)
    #     pdf.cell(40, 10, f"${tax_amount:.2f}", border=1, ln=True)
    #     grand_total += tax_amount

    # Grand Total
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(150, 10, "Total Due", border=1)
    pdf.cell(40, 10, f"${grand_total:.2f}", border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Save PDF
    filename = f"Invoice_{data['invoice_number']}.pdf"
    pdf.output(filename)
    print(f"Invoice saved as {filename}")

# === Example Manual Input ===
invoice_data = {
    "client_name": "John Client",
    "client_email": "john@example.com",
    "invoice_number": get_next_invoice_number(),
    "invoice_date": datetime.now().strftime("%Y-%m-%d"),
    "tax_rate": 0,  # Set to 0 if tax not needed
    "items": [
        {"desc": "Web development - 10 hours", "qty": 10, "rate": 50.00},
        {"desc": "Design review", "qty": 1, "rate": 75.00},
    ]
}

generate_invoice(invoice_data)






from datetime import datetime
from generate_invoice import generate_invoice, get_next_invoice_number

def get_invoice_data():
    print("\n--- Invoice Generator (CLI) ---\n")

    client_name = input("Client name: ")
    client_email = input("Client email: ")

    items = []
    while True:
        desc = input("\nItem description: ")
        qty = int(input("Quantity: "))
        rate = float(input("Rate per unit: "))
        items.append({"desc": desc, "qty": qty, "rate": rate})

        more = input("Add another item? (y/n): ").lower()
        if more != 'y':
            break

    tax_input = input("Enter tax rate (leave blank if none): ")
    tax_rate = float(tax_input) if tax_input else 0.0

    invoice_data = {
        "client_name": client_name,
        "client_email": client_email,
        "invoice_number": get_next_invoice_number(),
        "invoice_date": datetime.now().strftime("%Y-%m-%d"),
        "tax_rate": tax_rate,
        "items": items
    }

    return invoice_data

if __name__ == "__main__":
    data = get_invoice_data()
    generate_invoice(data)
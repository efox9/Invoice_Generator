import json
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QSpinBox, QDoubleSpinBox, QMessageBox, QComboBox
)
from datetime import datetime
from generate_invoice import generate_invoice, get_next_invoice_number
import os


class InvoiceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Invoice Generator")

        # Layouts
        layout = QVBoxLayout()

        # Load client data
        self.clients_file = "clients.json"
        self.clients = self.load_clients()
        # Client info
        self.client_name = QLineEdit()
        self.client_email = QLineEdit()

        # Dropdown to select existing clients
        self.client_selector = QComboBox()
        self.client_selector.addItem("-- Select Client --")
        self.client_selector.addItems(self.clients.keys())
        self.client_selector.currentIndexChanged.connect(self.fill_client_info)
        layout.addLayout(self._form_row("Saved Clients:", self.client_selector))
  

        layout.addLayout(self._form_row("Client Name:", self.client_name))
        layout.addLayout(self._form_row("Client Email:", self.client_email))
        save_btn = QPushButton("Save Client")
        save_btn.clicked.connect(self.save_clients)
        layout.addLayout(self._form_row("", save_btn))  

        # Line Items Table
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Service", "Hours", "Rate/hr", "Details"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        # Buttons
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Add Item")
        add_btn.clicked.connect(self.add_item_row)
        gen_btn = QPushButton("Generate Invoice")
        gen_btn.clicked.connect(self.generate_invoice)
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(gen_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def _form_row(self, label, widget):
        row = QHBoxLayout()
        row.addWidget(QLabel(label))
        row.addWidget(widget)
        return row

    def add_item_row(self):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(""))
        hours = QSpinBox()
        hours.setRange(0, 1000)
        self.table.setCellWidget(row, 1, hours)
        rate = QDoubleSpinBox()
        rate.setPrefix("$")
        rate.setDecimals(2)
        rate.setRange(0, 100000)
        self.table.setCellWidget(row, 2, rate)
        self.table.setItem(row, 3, QTableWidgetItem(""))

    def load_clients(self):
        if os.path.exists(self.clients_file):
            with open(self.clients_file, "r") as file:
                return json.load(file)    
        return {}

    def save_clients(self):
        name = self.clients_name.text().strip()
        email = self.clients_email.text().strip()

        if not name or not email:
            QMessageBox.warning(self, "Missing Info", "Client name and email required.")   
            return
        
        new_client = {"name": name, "email": email}

        try:
            with open(self.clients_file, "r") as file:
                clients = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            clients = []

        # Avoid duplicates
        if any(c["name"] == name and c["email"] == email for c in clients):
            QMessageBox.information(self, "Duplicate", "Client already exists.")
            return
        clients.append(new_client)

        # Save to file
        with open(self.clients_file, "w") as file:
            json.dump(clients, file, indent=2)
        
        self.clients_dropdown.addItem(f"{name} <{email}>")
        QMessageBox.information(self, "Saved", "Client saved Successfully!")

    def fill_client_info(self):
        name = self.client_selector.currentText()
        if name in self.clients:
            self.client_name.setText(name)
            self.client_email.setText(self.clients[name])

    def generate_invoice(self):
        name = self.client_name.text()
        email = self.client_email.text()

        if not name or not email:
            QMessageBox.warning(self, "Missing Info", "Client name and email are required.")
            return

        items = []
        for row in range(self.table.rowCount()):
            service_item = self.table.item(row, 0)
            hours_widget = self.table.cellWidget(row, 1)
            rate_widget = self.table.cellWidget(row, 2)
            details_item = self.table.item(row, 3)
            
            if service_item is None or not service_item.text():
                continue

            desc = service_item.text()
            if details_item and details_item.text():
                desc += f" - {details_item.text()}"

            items.append({
                "desc": desc,
                "qty": hours_widget.value(),
                "rate": rate_widget.value()  
            })

        if not items:
            QMessageBox.warning(self, "No Items", "Please add at least one item.")
            return

        data = {
            "client_name": name,
            "client_email": email,
            "invoice_number": get_next_invoice_number(),
            "invoice_date": datetime.now().strftime("%Y-%m-%d"),
            "items": items
        }

        generate_invoice(data)
        QMessageBox.information(self, "Success", "Invoice generated successfully!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InvoiceApp()
    window.show()
    sys.exit(app.exec_())
# invoice-generator
Mini-project for Tech4Girls Cohort 4

## Project Overview
The Invoice Generator is a command-line Python application that allows small businesses to generate professional invoices directly from the terminal. The program collects business details, client information, invoice items, performs automatic calculations, and generates a formatted invoice. Each invoice is saved as a file and recorded in an invoice history log.

## Features

### Feature 1 — Business Profile
On the first run, the program collects business information including the business name, address, phone number, and email.  
This information is saved in business_profile.txt and automatically loaded whenever the program starts.

### Feature 2 — Create Invoice
The user enters:
- Client name
- Client email
- Number of days until the invoice is due

The program automatically:
- Generates an invoice number (INV-001, INV-002, etc.)
- Captures the invoice date
- Calculates the due date

Users can enter multiple line items (description, quantity, unit price).

### Feature 3 — Calculations
The system calculates:
- Subtotal
- Optional tax (15%)
- Grand total

### Feature 4 — Format and Display Invoice
The program formats the invoice clearly in the terminal, displaying:
- Business details
- Client details
- Invoice date and due date
- Item table (Item, Quantity, Price, Total)
- Subtotal, tax, and total due

### Feature 5 — Save Invoice
Each invoice is saved as a text file using the format:

INV-001_ClientName.txt

All invoices are also recorded in invoice_log.txt, which stores:
- Invoice number
- Client name
- Total amount
- Invoice date

### Feature 6 — View Invoice History
The program reads invoice_log.txt and displays all past invoices in a formatted table.

### Menu System
The application includes a simple menu interface:

1. Create Invoice  
2. View Invoice History  
3. Exit

## Technologies Used
- Python
- File Handling
- Dictionaries
- Loops and Conditional Statements
- Datetime Module

## Project Structure
invoice-generator/
│
├── invoice.py  
├── business_profile.txt  
├── invoice_log.txt  
├── README.md  
└── Generated invoices (INV-XXX_ClientName.txt)

## How to Run the Project

Clone the repository:

git clone https://github.com/queentaamy/invoice-generator.git

Navigate into the project folder:

cd invoice-generator

Run the program:

python3 invoice.py

## Authors
Asantewa Tutua Appiah  
Rashida Ahmed

## Program
Tech4Girls Backend Development Training

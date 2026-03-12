# Import modules used for working with dates
from datetime import datetime, timedelta

# Program welcome message
welcome_msg = "Welcome to invoice generator!\nProgram started successfully!"
print(welcome_msg)


# -------------------------------
# Feature 1 — Business Profile Setup
# -------------------------------
# This function collects the business details from the user
def business_setup():
    business_name = input("Please enter your business name: ")
    business_email = input("Please enter your business email: ")
    business_address = input("Please enter your business address: ")
    business_phone_number = input("Please enter your business phone number: ")

    # Store business information inside a dictionary
    business_profile = {
        "name": business_name,
        "email": business_email,
        "address": business_address,
        "phone_number": business_phone_number
    }

    # Display confirmation of captured data
    print("\nYour business information has been created!")
    print("Name:", business_profile["name"])
    print("Email:", business_profile["email"])
    print("Address:", business_profile["address"])
    print("Phone number:", business_profile["phone_number"])

    return business_profile


# This function saves the business profile into a text file
def save_business_profile(profile):
    with open("business_profile.txt", "w") as file:
        file.write("Name: " + profile["name"] + "\n")
        file.write("Email: " + profile["email"] + "\n")
        file.write("Address: " + profile["address"] + "\n")
        file.write("Phone number: " + profile["phone_number"] + "\n")

    print("Profile saved successfully!")


# This function loads the business profile from the file if it already exists
def load_business_profile():
    try:
        with open("business_profile.txt", "r") as file:
            lines = file.readlines()

            # Reconstruct the dictionary from file data
            business_profile = {
                "name": lines[0].strip().split(": ")[1],
                "email": lines[1].strip().split(": ")[1],
                "address": lines[2].strip().split(": ")[1],
                "phone_number": lines[3].strip().split(": ")[1]
            }

            print("\nBusiness profile loaded successfully!")
            print("Name:", business_profile["name"])
            print("Email:", business_profile["email"])
            print("Address:", business_profile["address"])
            print("Phone number:", business_profile["phone_number"])

            return business_profile

    # If the file does not exist, ask user to set up the business profile
    except FileNotFoundError:
        print("No business profile found. Please set up your business profile first.")
        return None


# -------------------------------
# Invoice Number Generation
# -------------------------------
# This function generates the next invoice number using invoice_log.txt
def generate_invoice_number():
    try:
        with open("invoice_log.txt", "r") as file:
            lines = file.readlines()
            next_number = len(lines) + 1
    except FileNotFoundError:
        next_number = 1

    # Format invoice number like INV-001
    invoice_number = f"INV-{next_number:03}"
    print("Generated Invoice Number:", invoice_number)
    return invoice_number


# -------------------------------
# Saving the Invoice File
# -------------------------------
# This function saves the formatted invoice to a text file
def save_invoice(invoice_string, invoice_number, client_name):
    # Replace spaces with underscores to make filename safe
    safe_client_name = client_name.replace(" ", "_")

    # Example filename: INV-001_MTN_Ghana.txt
    file_name = f"{invoice_number}_{safe_client_name}.txt"

    with open(file_name, "w") as file:
        file.write(invoice_string)

    print("Invoice saved successfully as", file_name)


# -------------------------------
# Updating Invoice Log
# -------------------------------
# This function records invoice history inside invoice_log.txt
def update_invoice_log(invoice_number, client_name, grand_total, invoice_date):
    with open("invoice_log.txt", "a") as file:
        file.write(f"{invoice_number}, {client_name}, {grand_total}, {invoice_date}\n")

    print("Invoice log updated successfully!")


# -------------------------------
# Feature 2 — Creating Invoice
# -------------------------------

# Collect client information
def get_client_details():
    client_name = input("Enter client name: ")
    client_email = input("Enter client email: ")

    client = {
        "name": client_name,
        "email": client_email
    }

    print("\nClient details collected successfully!")
    print("Client Name:", client["name"])
    print("Client Email:", client["email"])

    return client


# Generate invoice and due dates
def get_invoice_dates():
    invoice_date = datetime.today().date()

    # Ask user how many days until payment is due
    days_until_due = int(input("Enter number of days until due: "))

    # Calculate due date
    due_date = invoice_date + timedelta(days=days_until_due)

    print("\nInvoice dates generated successfully!")
    print("Invoice Date:", invoice_date)
    print("Due Date:", due_date)

    return {
        "invoice_date": invoice_date,
        "due_date": due_date
    }


# Collect invoice line items
def collect_line_items():
    items = []

    while True:
        description = input("Enter item description (or type 'done' to finish): ")

        if description.lower() == "done":
            break

        quantity = int(input("Enter quantity: "))
        unit_price = float(input("Enter unit price: "))

        item = {
            "description": description,
            "quantity": quantity,
            "unit_price": unit_price
        }

        items.append(item)

    print("\nLine items collected successfully!")

    # Display collected items
    for item in items:
        print(
            item["description"],
            "| Qty:", item["quantity"],
            "| Unit Price:", item["unit_price"]
        )

    return items


# Calculate subtotal, tax, and grand total
def calculate_totals(items):
    subtotal = 0

    for item in items:
        item_total = item["quantity"] * item["unit_price"]
        subtotal += item_total

    tax_choice = input("Apply 15% tax? (yes/no): ").lower()

    if tax_choice == "yes":
        tax = subtotal * 0.15
    else:
        tax = 0

    grand_total = subtotal + tax

    print("\nTotals calculated successfully!")
    print("Subtotal:", subtotal)
    print("Tax:", tax)
    print("Grand Total:", grand_total)

    return {
        "subtotal": subtotal,
        "tax": tax,
        "grand_total": grand_total
    }


# Format and display the final invoice
def format_invoice(profile, client, invoice_number, invoice_dates, items, totals):

    invoice_text = ""
    invoice_text += "=" * 40 + "\n"
    invoice_text += f"INVOICE - {invoice_number}\n"
    invoice_text += "=" * 40 + "\n"

    # Business details
    invoice_text += f"FROM: {profile['name']}\n"
    invoice_text += f"{profile['address']}\n"
    invoice_text += f"{profile['email']}\n"
    invoice_text += f"{profile['phone_number']}\n\n"

    # Client details
    invoice_text += f"TO: {client['name']}\n"
    invoice_text += f"{client['email']}\n\n"

    # Invoice dates
    invoice_text += f"Date: {invoice_dates['invoice_date']}\n"
    invoice_text += f"Due Date: {invoice_dates['due_date']}\n\n"

    # Invoice table header
    invoice_text += "-" * 40 + "\n"
    invoice_text += "ITEM\tQTY\tPRICE\tTOTAL\n"
    invoice_text += "-" * 40 + "\n"

    # List all line items
    for item in items:
        line_total = item["quantity"] * item["unit_price"]
        invoice_text += (
            f"{item['description']}\t{item['quantity']}\t"
            f"{item['unit_price']}\t{line_total}\n"
        )

    # Totals section
    invoice_text += "-" * 40 + "\n"
    invoice_text += f"Subtotal: {totals['subtotal']}\n"
    invoice_text += f"Tax: {totals['tax']}\n"
    invoice_text += f"Total Due: {totals['grand_total']}\n"
    invoice_text += "=" * 40 + "\n"

    # Print invoice to terminal
    print("\n" + invoice_text)

    # Return invoice text so it can be saved to a file
    return invoice_text


# -------------------------------
# Main Program Flow
# -------------------------------
def main():

    # Load existing business profile or create a new one
    profile = load_business_profile()

    if profile is None:
        profile = business_setup()
        save_business_profile(profile)

    # Collect invoice information
    client = get_client_details()
    invoice_dates = get_invoice_dates()
    items = collect_line_items()

    # Calculate totals
    totals = calculate_totals(items)

    # Generate invoice number
    invoice_number = generate_invoice_number()

    # Format invoice
    invoice_string = format_invoice(
        profile,
        client,
        invoice_number,
        invoice_dates,
        items,
        totals
    )

    # Save invoice file
    save_invoice(invoice_string, invoice_number, client["name"])

    # Update invoice log
    update_invoice_log(
        invoice_number,
        client["name"],
        totals["grand_total"],
        invoice_dates["invoice_date"]
    )


# Start the program
main()
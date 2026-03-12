# Import modules used for working with dates
from datetime import datetime, timedelta

# Import QR code generator from separate file
from invoice_qr import generate_invoice_qr

# Program welcome message
welcome_msg = "Welcome to invoice generator!\nProgram started successfully!"
print(welcome_msg)


# -------------------------------------------------
# Feature 1 — Business Profile Setup
# -------------------------------------------------

# Collect business details from the user
def business_setup():
    business_name = input("Please enter your business name: ")
    business_email = input("Please enter your business email: ")
    business_address = input("Please enter your business address: ")
    business_phone_number = input("Please enter your business phone number: ")

    # Store business information in a dictionary
    business_profile = {
        "name": business_name,
        "email": business_email,
        "address": business_address,
        "phone_number": business_phone_number
    }

    print("\nYour business information has been created!")
    print("Name:", business_profile["name"])
    print("Email:", business_profile["email"])
    print("Address:", business_profile["address"])
    print("Phone number:", business_profile["phone_number"])

    return business_profile


# Save business profile to a file
def save_business_profile(profile):
    with open("business_profile.txt", "w") as file:
        file.write("Name: " + profile["name"] + "\n")
        file.write("Email: " + profile["email"] + "\n")
        file.write("Address: " + profile["address"] + "\n")
        file.write("Phone number: " + profile["phone_number"] + "\n")

    print("Profile saved successfully!")


# Load business profile from file if it exists
def load_business_profile():
    try:
        with open("business_profile.txt", "r") as file:
            lines = file.readlines()

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

    except FileNotFoundError:
        print("No business profile found. Please set up your business profile first.")
        return None


# -------------------------------------------------
# Feature 2 — Create Invoice (Client + Dates + Items)
# -------------------------------------------------

# Collect client details
def get_client_details():
    client_name = input("Enter client name: ")
    client_email = input("Enter client email: ")

    # Store client details in a dictionary
    client = {
        "name": client_name,
        "email": client_email
    }

    return client


# Generate invoice date and due date
def get_invoice_dates():
    # Set invoice date to today
    invoice_date = datetime.today().date()

    # Ask user how many days until payment is due
    days_until_due = int(input("Enter number of days until due: "))

    # Calculate due date
    due_date = invoice_date + timedelta(days=days_until_due)

    return {
        "invoice_date": invoice_date,
        "due_date": due_date
    }


# Collect invoice line items
def collect_line_items():
    items = []

    while True:
        description = input("Enter item description (or type 'done'): ")

        # Stop collecting items when user types done
        if description.lower() == "done":
            break

        quantity = int(input("Enter quantity: "))
        unit_price = float(input("Enter unit price: "))

        # Add each item as a dictionary to the list
        items.append({
            "description": description,
            "quantity": quantity,
            "unit_price": unit_price
        })

    return items


# -------------------------------------------------
# Feature 3 — Calculations
# -------------------------------------------------

# Calculate subtotal, tax and grand total
def calculate_totals(items):
    subtotal = 0

    # Add up all line totals
    for item in items:
        subtotal += item["quantity"] * item["unit_price"]

    # Ask whether tax should be applied
    tax_choice = input("Apply 15% tax? (yes/no): ").lower()

    if tax_choice == "yes":
        tax = subtotal * 0.15
    else:
        tax = 0

    grand_total = subtotal + tax

    return {
        "subtotal": subtotal,
        "tax": tax,
        "grand_total": grand_total
    }


# -------------------------------------------------
# Feature 4 — Format and Display Invoice
# -------------------------------------------------

# Format the invoice and display it in the terminal
def format_invoice(profile, client, invoice_number, invoice_dates, items, totals):
    invoice_text = ""

    invoice_text += "=" * 60 + "\n"
    invoice_text += f"INVOICE - {invoice_number}\n"
    invoice_text += "=" * 60 + "\n"

    # Business details
    invoice_text += f"FROM: {profile['name']}\n"
    invoice_text += f"      {profile['address']} | {profile['email']}\n"

    # Client details
    invoice_text += f"TO:   {client['name']} | {client['email']}\n"

    # Date details
    invoice_text += f"Date: {invoice_dates['invoice_date']} | Due: {invoice_dates['due_date']}\n\n"

    # Invoice item table header
    invoice_text += "-" * 60 + "\n"
    invoice_text += f"{'ITEM':<20}{'QTY':<10}{'PRICE':<10}{'TOTAL':<10}\n"
    invoice_text += "-" * 60 + "\n"

    # Display each line item
    for item in items:
        line_total = item["quantity"] * item["unit_price"]

        invoice_text += (
            f"{item['description']:<20}"
            f"{item['quantity']:<10}"
            f"{item['unit_price']:<10.2f}"
            f"{line_total:<10.2f}\n"
        )

    invoice_text += "-" * 60 + "\n"

    # Totals section
    invoice_text += f"{'Subtotal:':<30}{totals['subtotal']:.2f}\n"
    invoice_text += f"{'Tax (15%):':<30}{totals['tax']:.2f}\n"
    invoice_text += f"{'TOTAL DUE:':<30}{totals['grand_total']:.2f}\n"
    invoice_text += "=" * 60 + "\n"

    # Display invoice in terminal
    print("\n" + invoice_text)

    return invoice_text


# -------------------------------------------------
# Feature 5 — Save Invoice + Update Log + Generate QR
# -------------------------------------------------

# Generate invoice number automatically
# This improved version reads the last invoice number
# instead of just counting file lines
def generate_invoice_number():
    try:
        with open("invoice_log.txt", "r") as file:
            lines = file.readlines()

        # If the file is empty, start from INV-001
        if not lines:
            return "INV-001"

        # Get the invoice number from the last line
        last_line = lines[-1]
        last_invoice_number = last_line.split(",")[0].strip()

        # Extract numeric part from something like INV-007
        last_number = int(last_invoice_number.split("-")[1])

        # Increment the number by 1
        next_number = last_number + 1

        return f"INV-{next_number:03}"

    except FileNotFoundError:
        return "INV-001"


# Save invoice to a text file
def save_invoice(invoice_string, invoice_number, client_name):
    # Replace spaces with underscores for a safe filename
    safe_client_name = client_name.replace(" ", "_")
    file_name = f"{invoice_number}_{safe_client_name}.txt"

    with open(file_name, "w") as file:
        file.write(invoice_string)

    print("Invoice saved successfully as", file_name)

    return file_name


# Update invoice history log
def update_invoice_log(invoice_number, client_name, grand_total, invoice_date):
    with open("invoice_log.txt", "a") as file:
        file.write(f"{invoice_number}, {client_name}, {grand_total:.2f}, {invoice_date}\n")

    print("Invoice log updated successfully!")


# -------------------------------------------------
# Feature 6 — View Invoice History
# -------------------------------------------------

# Display all previous invoices in a table format
def view_invoice_history():
    try:
        with open("invoice_log.txt", "r") as file:
            lines = file.readlines()

        # Check whether the file is empty
        if not lines:
            print("No invoice history found.")
            return

        print("\n" + "=" * 60)
        print("INVOICE HISTORY")
        print("=" * 60)

        # Print table headings
        print(f"{'Invoice No.':<15}{'Client':<20}{'Total':<12}{'Date':<15}")
        print("-" * 60)

        # Print each row of invoice history
        for line in lines:
            invoice_number, client, total, date = line.strip().split(",")

            print(
                f"{invoice_number.strip():<15}"
                f"{client.strip():<20}"
                f"{total.strip():<12}"
                f"{date.strip():<15}"
            )

        print("=" * 60)

    except FileNotFoundError:
        print("No invoice history file found.")


# -------------------------------------------------
# Main Program Flow with Menu
# -------------------------------------------------

def main():
    # Load existing business profile or create a new one
    profile = load_business_profile()

    if profile is None:
        profile = business_setup()
        save_business_profile(profile)

    # Keep showing the menu until user chooses Exit
    while True:
        print("\n----- INVOICE GENERATOR MENU -----")
        print("1. Create Invoice")
        print("2. View Invoice History")
        print("3. Exit")

        choice = input("Choose an option: ")

        # Option 1 — Create a new invoice
        if choice == "1":
            client = get_client_details()
            invoice_dates = get_invoice_dates()
            items = collect_line_items()
            totals = calculate_totals(items)
            invoice_number = generate_invoice_number()

            # Format the invoice using your existing structure
            invoice_string = format_invoice(
                profile,
                client,
                invoice_number,
                invoice_dates,
                items,
                totals
            )

            # Save invoice as text file
            save_invoice(invoice_string, invoice_number, client["name"])

            # Generate QR code using the exact same invoice string
            generate_invoice_qr(invoice_string, invoice_number)

            # Update invoice log
            update_invoice_log(
                invoice_number,
                client["name"],
                totals["grand_total"],
                invoice_dates["invoice_date"]
            )

        # Option 2 — View invoice history separately
        elif choice == "2":
            print("\nDisplaying invoice history:")
            view_invoice_history()
            print("Invoice history displayed successfully!")
            print("Returning to main menu...")

        # Option 3 — Exit the program
        elif choice == "3":
            print("Exiting program...")
            break

        # Handle invalid menu input
        else:
            print("Invalid option. Please choose 1, 2, or 3.")



# Run the program
main()
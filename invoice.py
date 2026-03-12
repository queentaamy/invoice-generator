# Import modules for working with dates
from datetime import datetime, timedelta

# Welcome message
welcome_msg = "Welcome to invoice generator!\nProgram started successfully!"
print(welcome_msg)


# -------------------------------
# Feature 1 — Business Profile Setup
# -------------------------------
def business_setup():
    # Collect business details from user
    business_name = input("Please enter your business name: ")
    business_email = input("Please enter your business email: ")
    business_address = input("Please enter your business address: ")
    business_phone_number = input("Please enter your business phone number: ")

    # Store the data in a dictionary
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


# Save business profile to file
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


# -------------------------------
# Invoice Number Generation
# -------------------------------
def generate_invoice_number():
    try:
        with open("invoice_log.txt", "r") as file:
            lines = file.readlines()
            next_number = len(lines) + 1
    except FileNotFoundError:
        next_number = 1

    invoice_number = f"INV-{next_number:03}"
    print("Generated Invoice Number:", invoice_number)
    return invoice_number


# -------------------------------
# Save Invoice to File
# -------------------------------
def save_invoice(invoice_string, invoice_number, client_name):
    safe_client_name = client_name.replace(" ", "_")
    file_name = f"{invoice_number}_{safe_client_name}.txt"

    with open(file_name, "w") as file:
        file.write(invoice_string)

    print("Invoice saved successfully as", file_name)


# -------------------------------
# Update Invoice Log
# -------------------------------
def update_invoice_log(invoice_number, client_name, grand_total, invoice_date):
    with open("invoice_log.txt", "a") as file:
        file.write(f"{invoice_number}, {client_name}, {grand_total}, {invoice_date}\n")

    print("Invoice log updated successfully!")


# -------------------------------
# Feature 2 — Creating Invoice
# -------------------------------

# Get client details
def get_client_details():
    client_name = input("Enter client name: ")
    client_email = input("Enter client email: ")

    client = {
        "name": client_name,
        "email": client_email
    }

    return client


# Generate invoice date and due date
def get_invoice_dates():
    invoice_date = datetime.today().date()
    days_until_due = int(input("Enter number of days until due: "))
    due_date = invoice_date + timedelta(days=days_until_due)

    return {
        "invoice_date": invoice_date,
        "due_date": due_date
    }


# Collect invoice items
def collect_line_items():
    items = []

    while True:
        description = input("Enter item description (or type 'done'): ")

        if description.lower() == "done":
            break

        quantity = int(input("Enter quantity: "))
        unit_price = float(input("Enter unit price: "))

        items.append({
            "description": description,
            "quantity": quantity,
            "unit_price": unit_price
        })

    return items


# Calculate totals
def calculate_totals(items):
    subtotal = 0

    for item in items:
        subtotal += item["quantity"] * item["unit_price"]

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


# -------------------------------
# Format and Display Invoice
# -------------------------------
def format_invoice(profile, client, invoice_number, invoice_dates, items, totals):

    invoice_text = ""
    invoice_text += "=" * 60 + "\n"
    invoice_text += f"INVOICE - {invoice_number}\n"
    invoice_text += "=" * 60 + "\n"

    # Business information
    invoice_text += f"FROM: {profile['name']}\n"
    invoice_text += f"      {profile['address']} | {profile['email']}\n"

    # Client information
    invoice_text += f"TO:   {client['name']} | {client['email']}\n"

    # Dates
    invoice_text += f"Date: {invoice_dates['invoice_date']} | Due: {invoice_dates['due_date']}\n\n"

    invoice_text += "-" * 60 + "\n"
    invoice_text += f"{'ITEM':<20}{'QTY':<10}{'PRICE':<10}{'TOTAL':<10}\n"
    invoice_text += "-" * 60 + "\n"

    for item in items:
        line_total = item["quantity"] * item["unit_price"]

        invoice_text += (
            f"{item['description']:<30}"
            f"{item['quantity']:<10}"
            f"{item['unit_price']:<10.2f}"
            f"{line_total:<10.2f}\n"
        )

    invoice_text += "-" * 60 + "\n"

    # Totals section with spacing
    invoice_text += f"{'Subtotal:':<30}{totals['subtotal']:.2f}\n"
    invoice_text += f"{'Tax (15%):':<30}{totals['tax']:.2f}\n"
    invoice_text += f"{'TOTAL DUE:':<30}{totals['grand_total']:.2f}\n"

    invoice_text += "=" * 60 + "\n"

    print("\n" + invoice_text)

    return invoice_text


# -------------------------------
# Main Program Flow
# -------------------------------
def main():

    # Load business profile or create one
    profile = load_business_profile()

    if profile is None:
        profile = business_setup()
        save_business_profile(profile)

    # Collect invoice information
    client = get_client_details()
    invoice_dates = get_invoice_dates()
    items = collect_line_items()

    totals = calculate_totals(items)

    invoice_number = generate_invoice_number()

    invoice_string = format_invoice(
        profile,
        client,
        invoice_number,
        invoice_dates,
        items,
        totals
    )

    save_invoice(invoice_string, invoice_number, client["name"])

    update_invoice_log(
        invoice_number,
        client["name"],
        totals["grand_total"],
        invoice_dates["invoice_date"]
    )


# Run program
main()
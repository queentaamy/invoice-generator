# Import modules used for working with dates
# datetime helps us get today's date
# timedelta helps us calculate the due date by adding days
from datetime import datetime, timedelta


# Welcome message displayed when the program starts
welcome_msg = "Welcome to invoice generator!\nProgram started successfully!"
print(welcome_msg)


# This helper function ensures the user does not leave input empty
# It keeps asking until a value is entered
def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()

        if value == "":
            print("Input cannot be empty. Please try again.")
        else:
            return value


# This helper function ensures the user enters a valid integer
# It prevents the program from crashing if the user enters text
def get_valid_int(prompt):
    while True:
        value = input(prompt).strip()

        try:
            number = int(value)

            if number <= 0:
                print("Please enter a number greater than 0.")
            else:
                return number

        except ValueError:
            print("Invalid input. Please enter a valid whole number.")


# This helper function ensures the user enters a valid decimal number
# It is used for prices where decimals may be needed
def get_valid_float(prompt):
    while True:
        value = input(prompt).strip()

        try:
            number = float(value)

            if number <= 0:
                print("Please enter a number greater than 0.")
            else:
                return number

        except ValueError:
            print("Invalid input. Please enter a valid number.")


# This helper function validates yes/no responses
def get_yes_no_input(prompt):
    while True:
        value = input(prompt).strip().lower()

        if value in ["yes", "no"]:
            return value
        else:
            print("Invalid input. Please type 'yes' or 'no'.")


# Feature 1 — Business Profile

# This function collects business information from the user
# The details are stored in a dictionary so they can be reused later
def business_setup():
    business_name = get_non_empty_input("Enter your business name: ")
    business_email = get_non_empty_input("Enter your business email: ")
    business_address = get_non_empty_input("Enter your business address: ")
    business_phone_number = get_non_empty_input("Enter your business phone number: ")

    business_profile = {
        "name": business_name,
        "email": business_email,
        "address": business_address,
        "phone_number": business_phone_number
    }

    return business_profile


# This function saves the business profile to a file
# Saving the data allows the program to load it automatically next time
def save_business_profile(profile):
    with open("business_profile.txt", "w") as file:
        file.write("Name: " + profile["name"] + "\n")
        file.write("Email: " + profile["email"] + "\n")
        file.write("Address: " + profile["address"] + "\n")
        file.write("Phone: " + profile["phone_number"] + "\n")

    print("Business profile saved successfully!")


# This function loads the business profile from the file
# If the file does not exist, the user will create a new profile
def load_business_profile():
    try:
        with open("business_profile.txt", "r") as file:
            lines = file.readlines()

            profile = {
                "name": lines[0].strip().split(": ")[1],
                "email": lines[1].strip().split(": ")[1],
                "address": lines[2].strip().split(": ")[1],
                "phone_number": lines[3].strip().split(": ")[1]
            }

            print("Business profile loaded successfully!")
            return profile

    except FileNotFoundError:
        print("No business profile found.")
        return None


# Feature 2 — Create Invoice

# This function collects client details
# The information is stored in a dictionary
def get_client_details():
    client_name = get_non_empty_input("Enter client name: ")
    client_email = get_non_empty_input("Enter client email: ")

    client = {
        "name": client_name,
        "email": client_email
    }

    return client


# This function generates invoice date and due date
# datetime.today() gets the current date
# timedelta adds the number of days until payment is due
def get_invoice_dates():
    invoice_date = datetime.today().date()

    days_until_due = get_valid_int("Enter number of days until due: ")

    due_date = invoice_date + timedelta(days=days_until_due)

    return {
        "invoice_date": invoice_date,
        "due_date": due_date
    }


# This function collects invoice items from the user
# Each item contains item name, quantity, and unit price
def collect_line_items():
    items = []

    while True:
        item_name = input("Enter item (or type 'done'): ")

        if item_name.lower() == "done":
            if not items:
                print("You must enter at least one item.")
                continue
            break

        quantity = get_valid_int("Enter quantity: ")
        unit_price = get_valid_float("Enter unit price: ")

        items.append({
            "item": item_name,
            "quantity": quantity,
            "unit_price": unit_price
        })

    return items


# Feature 3 — Calculations

# This function calculates subtotal, tax, and grand total
# It multiplies quantity and price for each item
# All item totals are added together to get the subtotal
# If the user selects tax, 15% is applied
def calculate_totals(items):
    subtotal = 0

    for item in items:
        line_total = item["quantity"] * item["unit_price"]
        subtotal += line_total

    tax_choice = get_yes_no_input("Apply 15% tax? (yes/no): ")

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


# Feature 4 — Format and Display Invoice

# This function formats the invoice to display clearly in the terminal
# It prints business details, client details, items table, and totals
def format_invoice(profile, client, invoice_number, invoice_dates, items, totals):

    print("\n===================================================")
    print("INVOICE:", invoice_number)
    print("===================================================")

    print("FROM:", profile["name"])
    print(profile["address"], "|", profile["email"])

    print("\nTO:", client["name"], "|", client["email"])

    print("\nDate:", invoice_dates["invoice_date"], "| Due:", invoice_dates["due_date"])

    print("\n---------------------------------------------------")
    print(f"{'ITEMS':<20}{'QTY':<10}{'PRICE':<10}{'TOTAL':<10}")
    print("---------------------------------------------------")

    for item in items:
        total = item["quantity"] * item["unit_price"]

        print(
            f"{item['item']:<20}"
            f"{item['quantity']:<10}"
            f"{item['unit_price']:<10}"
            f"{total:<10}"
        )

    print("---------------------------------------------------")

    print(f"{'Subtotal:':<20}{totals['subtotal']}")
    print(f"{'Tax (15%):':<20}{totals['tax']}")
    print(f"{'TOTAL DUE:':<20}{totals['grand_total']}")

    print("===================================================")


# Feature 5 — Save Invoice

# This function generates a unique invoice number
# It reads the last invoice number from invoice_log.txt
def generate_invoice_number():
    try:
        with open("invoice_log.txt", "r") as file:
            lines = file.readlines()

        if not lines:
            return "INV-001"

        last_line = lines[-1]
        last_invoice_number = last_line.split(",")[0]

        last_number = int(last_invoice_number.split("-")[1])

        next_number = last_number + 1

        return f"INV-{next_number:03}"

    except FileNotFoundError:
        return "INV-001"


# This function saves the invoice as a text file
def save_invoice(invoice_number, client_name, totals):

    safe_client_name = client_name.replace(" ", "_")

    file_name = f"{invoice_number}_{safe_client_name}.txt"

    with open(file_name, "w") as file:
        file.write(f"Invoice Number: {invoice_number}\n")
        file.write(f"Client: {client_name}\n")
        file.write(f"Total Due: {totals['grand_total']}\n")

    print("Invoice saved as", file_name)


# This function updates invoice history
def update_invoice_log(invoice_number, client_name, total, date):

    with open("invoice_log.txt", "a") as file:
        file.write(f"{invoice_number}, {client_name}, {total}, {date}\n")


# Feature 6 — View Invoice History

# This function reads the invoice log file
# It displays all previous invoices in a table
def view_invoice_history():
    try:
        with open("invoice_log.txt", "r") as file:
            lines = file.readlines()

        print("\n================ INVOICE HISTORY =================")

        print(f"{'Invoice No':<15}{'Client':<20}{'Total':<10}{'Date':<15}")

        print("--------------------------------------------------")

        for line in lines:
            invoice_number, client, total, date = line.strip().split(",")

            print(
                f"{invoice_number:<15}"
                f"{client:<20}"
                f"{total:<10}"
                f"{date:<15}"
            )

    except FileNotFoundError:
        print("No invoice history found.")


# Main function controls the program flow
def main():

    profile = load_business_profile()

    if profile is None:
        profile = business_setup()
        save_business_profile(profile)

    while True:

        print("\n===== INVOICE GENERATOR MENU =====")
        print("1. Create Invoice")
        print("2. View Invoice History")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":

            client = get_client_details()

            invoice_dates = get_invoice_dates()

            items = collect_line_items()

            totals = calculate_totals(items)

            invoice_number = generate_invoice_number()

            format_invoice(profile, client, invoice_number, invoice_dates, items, totals)

            save_invoice(invoice_number, client["name"], totals)

            update_invoice_log(
                invoice_number,
                client["name"],
                totals["grand_total"],
                invoice_dates["invoice_date"]
            )

        elif choice == "2":

            view_invoice_history()

        elif choice == "3":

            print("Exiting program...")
            break

        else:

            print("Invalid option. Please choose 1, 2 or 3.")


# This line runs the program
main()
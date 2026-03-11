from datetime import datetime, timedelta

welcome_msg = "Welcome to invoice generator!\nProgram started successfully!"
print(welcome_msg)


# Feature 1 — Business Profile Setup
def business_setup():
    business_name = input("Please enter your business name: ")
    business_email = input("Please enter your business email: ")
    business_address = input("Please enter your business address: ")
    business_phone_number = input("Please enter your business phone number: ")


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


# Saving the Data to 'business_profile.txt' File
def save_business_profile(profile):
    with open("business_profile.txt", "w") as file:
        file.write("Name: " + profile["name"] + "\n")
        file.write("Email: " + profile["email"] + "\n")
        file.write("Address: " + profile["address"] + "\n")
        file.write("Phone number: " + profile["phone_number"] + "\n")

    print("Profile saved successfully!")

#Load Data From 'business_profile.txt' File
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

            print ("\nBusiness profile loaded successfully!")
            print("Name:", business_profile["name"])
            print("Email:", business_profile["email"])
            print("Address:", business_profile["address"])
            print("Phone number:", business_profile["phone_number"])
            
            return business_profile
        
    except FileNotFoundError:
        print("No business profile found. Please set up your business profile first.")
        return None
    
# Feature 2 Creating Invoice
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

def get_invoice_dates():
    invoice_date = datetime.today().date()
    days_until_due = int(input("Enter number of days until due: "))
    due_date = invoice_date + timedelta(days=days_until_due)

    print("\nInvoice dates generated successfully!")
    print("Invoice Date:", invoice_date)
    print("Due Date:", due_date)

    return {
        "invoice_date": invoice_date,
        "due_date": due_date
    }

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

    for item in items:
        print(
            item["description"],
            "| Qty:", item["quantity"],
            "| Unit Price:", item["unit_price"]
        )

    return items

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

def main():
    profile = load_business_profile()

    if profile is None:
        profile = business_setup()
        save_business_profile(profile)
    client = get_client_details()
    invoice_dates = get_invoice_dates()
    items = collect_line_items()
    totals = calculate_totals(items)
main()
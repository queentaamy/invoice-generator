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

def main():
    profile = load_business_profile()

    if profile is None:
        profile = business_setup()
        save_business_profile(profile)
        
    generate_invoice_number()


main()
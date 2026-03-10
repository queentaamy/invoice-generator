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


def main():
    profile = business_setup()
    save_business_profile(profile)


main()
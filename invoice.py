welcome_msg = "Welcome to invoice generator!\nProgram started successfully!"
print(welcome_msg)

# Feature 1
def bussiness_setup ():
    client_name = input ("Please enter your name: ")
    client_email = input ("Please enter your email: ")
    client_address = input ("Please enter your address: ")
    client_phone_number = input ("Please enter your phone number: ")

    bussiness_profile = {
    "name": client_name,
    "email": client_email,
    "address": client_address,
    "phone_number": client_phone_number
}

    print ("Your bussiness information has been saved successfully!")
    print ("Name: ", bussiness_profile["name"])
    print ("Email: ", bussiness_profile["email"])
    print ("Address: ", bussiness_profile["address"])
    print ("Phone number: ", bussiness_profile["phone_number"])
    
    return bussiness_profile
def main():
    bussiness_setup()


main()
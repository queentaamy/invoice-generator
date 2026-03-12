# -------------------------------------------------
# invoice_qr.py
# Handles QR code generation for invoices
# -------------------------------------------------

# Import required modules
import os
import qrcode


# -------------------------------------------------
# Function: generate_invoice_qr
# Generates both:
# 1. A QR code image
# 2. A QR code preview in the terminal
# -------------------------------------------------

def generate_invoice_qr(invoice_text, invoice_number):

    # Ensure QR code folder exists
    os.makedirs("qr_codes", exist_ok=True)

    # Create QR code object
    qr = qrcode.QRCode(
        version=None,
        box_size=10,
        border=4
    )

    # Add invoice data
    qr.add_data(invoice_text)

    # Build QR structure
    qr.make(fit=True)

    # Create QR image
    img = qr.make_image(fill_color="black", back_color="white")

    # File path for saving
    file_path = f"qr_codes/{invoice_number}_qr.png"

    # Save image
    img.save(file_path)

    print(f"\nQR code generated successfully: {file_path}")

    # -------------------------------------------------
    # Print QR code in terminal
    # -------------------------------------------------

    print("\nScan this QR code to view the invoice:\n")

    qr_terminal = qrcode.QRCode()

    qr_terminal.add_data(invoice_text)
    qr_terminal.make()

    # This prints the QR code directly in the terminal
    qr_terminal.print_ascii(invert=True)

    return file_path
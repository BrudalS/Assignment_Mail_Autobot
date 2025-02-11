import smtplib

EMAIL = "subhash7483558714@gmail.com"  # Your Gmail
PASSWORD = "nqxo igkt tewp utvv"  # Use the App Password here

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

try:
    server.login(EMAIL, PASSWORD)
    print("Login successful!")
except smtplib.SMTPAuthenticationError as e:
    print("SMTP Authentication Error:", e)
finally:
    server.quit()

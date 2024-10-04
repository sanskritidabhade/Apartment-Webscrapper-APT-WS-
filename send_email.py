import os # Used for accessing environment variables set using setx commands in Windows.
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .webscrap_apts import webscrap_apts

user_budget = int(input("Enter your budget: "))

def send_email():
    # SMTP server configuration with login and password
    smtp_server = "smtp.gmail.com"
    port = 587
    # Sender email and password are stored as environment variables on my operating system.
    sender_email = os.getenv('EMAIL_ADDRESS') 
    password = os.getenv('EMAIL_PASSWORD')

    receiver_email = input("Enter your email address: ")
    message = MIMEMultipart("alternative")
    message["Subject"] = "Apartment Listings | APT WS"  # The subject line of the email
    message["From"] = sender_email  # The sender's email (displayed in the "From" field)
    message["To"] = receiver_email  # The recipient's email (displayed in the "To" field)

    # Create the text part of the email
    listings = webscrap_apts(user_budget)
    text = "\n".join([f"Title: {apt[0]}, Area: {apt[1]}, Price: {apt[2]}, Link: {apt[3]}" for apt in listings])

    part = MIMEText(text, "plain")  # Specify that this part of the email is plain text
    message.attach(part)  # Attach the plain text part to the MIMEMultipart object

    # Secure SMTP connection between client and server
    try: 

        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")

    # Exception handling while sending email
    except Exception as e:
        print(f"Error: {e}")

    # Close SMTP connection once email is sent
    finally:
        server.quit()
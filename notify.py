# This code will be used to send email to users
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, sender_password, recipient_email, subject, message):
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Add body to the email
    body = message
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Create a secure connection with the SMTP server
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()

        # Login to the sender's email account
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Email sent successfully!")

    except Exception as e:
        print(f"An error occurred while sending the email: {str(e)}")

    finally:
        # Close the SMTP server connection
        server.quit()


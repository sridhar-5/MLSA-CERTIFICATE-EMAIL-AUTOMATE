import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv()
import os

def push_emails_to_participants(list_of_participants):

    for participant in list_of_participants:

        name = participant['Name Surname']
        email_id = participant['E Mail ']
        send_email(email_id, name)


def send_email(receiver_mail, name):
    subject = "Microsoft learn student ambassadors event certificate"
    body = "Thank you for attending the workshop. Please find the attachment of your certificate below. \nThanks."
    sender_email = "kv.sridharsai@gmail.com"  # enter your mail-id (ambassadors email id)
    receiver_email = receiver_mail
    password = os.environ.get("password")

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = "Output/PDF/" + name + ".pdf"  # In same directory as script
    print(filename)
    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
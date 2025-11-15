# email_invoice.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

def send_invoice(email, invoice_path):
    msg = MIMEMultipart()
    msg['Subject'] = "Your Invoice"
    msg['From'] = "yourstore@gmail.com"
    msg['To'] = email

    msg.attach(MIMEText("Thank you for your purchase!"))

    with open(invoice_path, "rb") as f:
        attachment = MIMEApplication(f.read(), _subtype="pdf")
        attachment.add_header('Content-Disposition', 'attachment', filename=invoice_path)
        msg.attach(attachment)

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login("yourstore@gmail.com", "your-app-password")
    server.send_message(msg)
    server.quit()

    return "Email sent!"

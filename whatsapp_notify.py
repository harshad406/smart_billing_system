# whatsapp_notify.py
from twilio.rest import Client

def send_whatsapp(phone, text):
    SID = "your_twilio_sid"
    TOKEN = "your_twilio_token"
    client = Client(SID, TOKEN)

    message = client.messages.create(
        body=text,
        from_="whatsapp:+917096922727",
        to=f"whatsapp:+91{phone}"
    )
    return message.sid

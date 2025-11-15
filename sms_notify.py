# sms_notify.py
import requests

API_KEY = "YOUR_FAST2SMS_API_KEY"

def send_sms(phone, message):
    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = {
        "sender_id": "TXTIND",
        "message": message,
        "route": "v3",
        "numbers": phone
    }
    headers = {
        "authorization": API_KEY
    }

    response = requests.post(url, data=payload, headers=headers)
    return response.json()

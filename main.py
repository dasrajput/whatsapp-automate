from twilio.rest import Client
from datetime import datetime, timedelta
import time

account_sid = "xxxxxxxxxxxxxxxxxx"
auth_token = "xxxxxxxxxxxxx"

client = Client(account_sid, auth_token)

def send_whatsapp_message(recipient_number, message_body):
    try:
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=message_body,
            to=f'whatsapp:{recipient_number}'
        )
        print(f"Message sent Successfully to {recipient_number} ! Message SID: {message.sid}")
    except Exception as e:
        print(f"Error sending message to {recipient_number}: {str(e)}")

name = input("Enter the recipient name: ")
recipient_number = input("Enter the recipient whatsapp number with country code: ")
message_body = input(f'Enter the message for {name}: ')

date_str = input("Enter the date in YYYY-MM-DD format: ")
time_str = input("Enter the time in HH:MM:SS format: ")

schedule_datetime = datetime.strptime(date_str + " " + time_str, "%Y-%m-%d %H:%M:%S")
current_datetime = datetime.now()
time_difference = schedule_datetime - current_datetime
delay_seconds = time_difference.total_seconds()

if delay_seconds <= 0:
    print("The scheduled time has already passed.")
else:
    print(f'Message scheduled to be sent to {name} at {schedule_datetime}.')


    time.sleep(delay_seconds)

    send_whatsapp_message(recipient_number, message_body)
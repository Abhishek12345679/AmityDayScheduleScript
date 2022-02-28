import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


def sendMessage(message):
    account_sid = "AC7882dd01bc9eb3b7e0c0affcb17e2578"
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]

    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            to="whatsapp:+917908174073",
            from_="whatsapp:+14155238886",
            body=message
        )
        print(message.sid)
    except TwilioRestException as err:
        print(err)

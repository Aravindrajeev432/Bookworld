from django.conf import settings
import os
from twilio.rest import Client


account_sid = ''
auth_token =  ''


class MessageHandler:

    phone_number = None
    otp = None

    def __init__(self, phone_number, otp) :
        self.phone_number = phone_number
        self.otp = otp 

    def send_otp_on_phone(self):
        client = Client(account_sid, auth_token)
        message = client.messages.create(
                                body=f'Welcome to BookWorld, your OTP to login is {self.otp} ',
                                from_='+12057842829',
                                to= self.phone_number,
                            )

        print(message.sid)
from twilio.rest import Client
from dotenv import load_dotenv
import os
# Create your views here.
load_dotenv()


def generateOTP():
    import random
    return random.randrange(10000, 99999)


def post():
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_ACCOUNT_TOKEN')
    phone_number = os.getenv('TWILIO_PHONE_NUMBER')

    client = Client(account_sid, auth_token)
    send_to = '+251935024844'
    print("sender - ", phone_number)
    print("recipient - ", send_to)

    otp = generateOTP()
    print("otp ", otp)

    body = f"Your Smile Verification code is {str(otp)}"
    message = client.messages.create(
        from_=phone_number,
        body=body,
        to=send_to
    )

    if message.sid:
        print(message.sid)
    else:
        print("error")


# post()


def call():
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_ACCOUNT_TOKEN')
    phone_number = os.getenv('TWILIO_PHONE_NUMBER')

    client = Client(account_sid, auth_token)
    send_to = '+251935024844'
    print("sender - ", phone_number)
    print("recipient - ", send_to)

    otp = generateOTP()
    print("otp ", otp)
    call = client.calls.create(
                        url='http://demo.twilio.com/docs/voice.xml',
                        to='+15558675310',
                        from_='+15017122661'
                    )
    print(call.sid)


call()

# import package
import os
from dotenv import load_dotenv
import africastalking

# Load environment variables
load_dotenv()

# Initialize SDK
api_key= os.getenv('AT_API_KEY')    
username = os.getenv('AT_USER_NAME')     
africastalking.initialize(username, api_key)


# Initialize a service e.g. SMS
sms = africastalking.SMS


def send_sms(message:str, recipients:str):
    if len(recipients) ==10:
        recipients = '+255' + recipients[1:]
    recipients_list = [recipients,"+255755327135"]
    response = sms.send(message, recipients_list)
    print(response)
    return response

def call_agent(recipient_number:str):
    voice = africastalking.Voice
    if len(recipient_number) ==10:
        recipient_number = '+255' + recipient_number[1:]
    response = voice.call("+255699997913", [recipient_number])
    print(response)
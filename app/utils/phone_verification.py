import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

import logging
logging.basicConfig(level=logging.INFO)


# Constants
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")  # Replace with your actual token or environment variable
PHONE_NUMBER_ID = os.getenv("RECIPIENT_WAID")  # Replace with your Phone Number ID
VERSION = "v1"  # Replace with the actual Graph API version you're using

def register_whatsapp_account(cc, phone_number, cert, method="sms", pin=None):
    """
    Register a WhatsApp account using the Graph API.
    
    :param cc: Country code (e.g., "255").
    :param phone_number: Phone number without country code or '+' sign.
    :param cert: Base64-encoded certificate string.
    :param method: Method to receive the registration code ('sms' or 'voice').
    :param pin: Optional 6-digit PIN for two-step verification.
    """
    url = f"https://graph.facebook.com/{VERSION}/account"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "cc": cc,
        "phone_number": phone_number,
        "method": method,
        "cert": cert
    }
    if pin:
        data["pin"] = pin

    response = requests.post(url, headers=headers, json=data)
    if response.status_code in [201, 202]:
        logging.info(f"Registration successful. Response: {response.json()}")
    else:
        logging.error(f"Failed to register account: {response.status_code} - {response.text}")


# Example usage
if __name__ == "__main__":
    COUNTRY_CODE = "+255"  # Example: Tanzania
    PHONE_NUMBER = "755327135"  # Without country code
    CERT = "CmwKKAj36LS7y969AhIGZW50OndhIg9VU0NGIENDVFRha3dpbXVQgof9uQYaQJgGSgo47UYIPeSQTfsYcaj/3bFARzgJ4+IhAvgU+mBoTDMziuLjgSGRauvCYXwOtku2NxMyKAGeChr+SXhSRAcSLm1ZEcX+r8Ba4ESMt52raCyWWOPkX8DYn8ExOE6tPI6x93IwA0GwlvNux+zWOe4="  # Replace with your cert
    METHOD = "sms"  # 'sms' or 'voice'
    PIN = 539712  # Optional PIN if two-step verification is enabled
    
    register_whatsapp_account(
        cc=COUNTRY_CODE,
        phone_number=PHONE_NUMBER,
        cert=CERT,
        method=METHOD,
        pin=PIN
    )

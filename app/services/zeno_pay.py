import httpx
import os
from dotenv import load_dotenv
from .sms import send_sms
import asyncio
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)


# Constants
ZENO_PAY_ID = os.getenv("ZENO_PAY_ID")
BASE_URL = "https://api.zeno.africa"

async  def make_payment(amount:str, phone_number:str,name:str):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/payment", data={
            'create_order': 1,
            'buyer_email': 'vudozo@gmail.com',
            'buyer_name': name,
            'buyer_phone': phone_number ,
            'amount': amount,
            'account_id': ZENO_PAY_ID,
            'api_key': '',
            'secret_key': '',
        })
        logging.info(f"Initiating payment of {amount} for {donor_name} using mobile number {wa_id}.")
        await asyncio.sleep(2)
        reponse = response.json()
        order_id = reponse.get('order_id', '')
        sms_to_send =f'Thank you {name} for your generous donation of {amount}.The ministry is grateful for your support. God bless you!,payment id: {order_id}'
        send_sms(sms_to_send, phone_number)
        # print(reponse)
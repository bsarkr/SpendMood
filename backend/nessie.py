import requests
import json
import os 
import random
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SECRET_NESSIE")

def account(customer_id):
    url = 'http://api.nessieisreal.com/customers/{}/accounts?key={}'.format(customer_id,api_key)
    payload = {
        "type": "Savings",
        "nickname": "test",
        "rewards": 10000,
        "balance": 10000,	
    }

    response = requests.post( 
        url, 
        data=json.dumps(payload),
        headers={'content-type':'application/json'},
    )
    print(response.json())
    if response.status_code == 201:
        print('Account created')

    return response.json()['objectCreated']['_id']

def create_cust():
    url = 'http://api.nessieisreal.com/customers?key={}'.format(api_key)

    payload = {
        "first_name": "Mary",
        "last_name": "Shelley",
        "address": {
            "street_number": "2960",
            "street_name": "Broadway",
            "city": "New York",
            "state": "NY",
            "zip": "10027"
        }
    }

    response = requests.post( 
        url, 
        data=json.dumps(payload),
        headers={'content-type':'application/json'},
    )

    print(response.json())
    if response.status_code == 201:
        print('Customer created')

    return response.json()['objectCreated']['_id']

def create_merch():
    url = 'http://api.nessieisreal.com/merchants?key={}'.format(api_key)

    payload = {
        "name": "Test1",
        "category": "Retail",
        "address": {
            "street_number": "123",
            "street_name": "Main Street",
            "city": "San Francisco",
            "state": "CA",
            "zip": "94105"
        },
        "geocode": {
            "lat": 37.7890,
            "lng": -122.4010
        }
    }

    return url, payload
    #68e1bf829683f20dd519a4ee

def create_purch(account_id):
    merchant_id = "68e1bf829683f20dd519a4ee"  # Fixed for now
    products = ["T-shirt", "Coffee", "Book", "Shoes", "Headphones", "Snack", "Notebook"]

    today = datetime.now()

    for i in range(7):  # Past 7 days
        purchase_date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        amount = round(random.uniform(5, 100), 2)
        description = random.choice(products)

        url = f'http://api.nessieisreal.com/accounts/{account_id}/purchases?key={api_key}'
        payload = {
            "merchant_id": merchant_id,
            "medium": "balance",
            "purchase_date": purchase_date,
            "amount": amount,
            "status": "completed",
            "description": description
        }

        response = requests.post(
            url,
            data=json.dumps(payload),
            headers={'content-type': 'application/json'}
        )

        if response.status_code == 201:
            print(f"✅ Purchase on {purchase_date} (${amount}) for '{description}'")
        else:
            print(f"❌ Failed to create purchase on {purchase_date}:", response.text)

        time.sleep(1)

def test_data():
    cust_id = create_cust()
    account_id = account(cust_id)
    create_purch(account_id)

test_data()

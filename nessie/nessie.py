import requests
import json
import os 
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SECRET_NESSIE")

def saving_account(customer_id):
    url = 'http://api.nessieisreal.com/customers/{}/accounts?key={}'.format(customer_id,api_key)
    payload = {
        "type": "Savings",
        "nickname": "test",
        "rewards": 10000,
        "balance": 10000,	
    }

    return url, payload

def create_cust():
    url = 'http://api.nessieisreal.com/customers?key={}'.format(api_key)

    payload = {
        "first_name": "Thomas",
        "last_name": "Paine",
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
    url = 'http://api.nessieisreal.com/accounts/{}/purchases?key={}'.format(account_id, api_key)

    payload = {
        "merchant_id": "68e1bf829683f20dd519a4ee",
        "medium": "balance",
        "purchase_date": "2025-10-04",
        "amount": 10,
        "status": "completed",
        "description": "tshirt"
    }

    return url, payload


"""     
url, payload = create_purch('68e1b1699683f20dd519a46b')

response = requests.post( 
	url, 
	data=json.dumps(payload),
	headers={'content-type':'application/json'},
	)

print(response.json())

if response.status_code == 201:
	print('Post worked')
     

def view_cust(customer_id):
    url = 'http://api.nessieisreal.com/customers/{}?key={}'.format(customer_id, api_key)

    params = {
        "key": api_key
    }

    return url, params
     

url, params = view_cust('68e19ec19683f20dd519a410')
response = requests.get(url)

print(response.json())

if response.status_code == 200:
    print('Post worked')
"""
repsonse = create_cust()
data = repsonse.json()
print(data['objectCreated']['_id'])
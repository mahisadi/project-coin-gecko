import os
import json
import requests
from dotenv import load_dotenv
from typing import Optional, Dict, Any, List
from ops.secrets_manager import SecretsManager
from ops.persistence_manager import PersistenceManager
from decimal import Decimal

load_dotenv()

PRICE_URL = os.getenv('API_URL_BASE_PATH') + os.getenv('API_PRICE_RESOURCE_PATH')

# Global variable to store the API_KEY. Don't need to call secretmanager everytime
API_KEY = None

def load_secret():
    global API_KEY
    if API_KEY is None:
        API_KEY = SecretsManager.get_secret(os.getenv('API_SECRET_KEY'))
    return API_KEY


class ServiceManager:
    @staticmethod
    def fetch_coin_dataset(coin: Optional[str], cur: Optional[str]) -> List[str]:
        print(' Inside fetch_coin_dataset ')
        pk_value = ''
        if coin and cur:
            pk_value = coin+'_'+cur
        print(' pk_value ', pk_value)
        dataSet = PersistenceManager.fetch_coin_dataset(pk_value)
        print(f"Fetching data from dataSet :: {dataSet}")
        return dataSet
    

    @staticmethod
    def get_coin_rank(coin: Optional[str], cur: Optional[str]) -> int:
        pk_value = coin+'_'+cur
        return PersistenceManager.fetch_coin_ranks(pk_value)

    @staticmethod
    def fetch_coin_price(coin: Optional[str], cur: Optional[str]) -> Dict[str, Any]:
        load_secret()
        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": API_KEY
        }
        query_params = {
            "ids": coin,
            "vs_currencies": cur
        }
        #ids=btc&vs_currencies=usd
        pk_value = coin+'_'+cur
        print(f"Fetching data from {PRICE_URL} with params: {query_params}")
        print(f"Using headers: {headers}")
        try:
            response = requests.get(PRICE_URL, headers=headers, params=query_params)
            if response.status_code == 200:
                print(response.text)
                data = response.json()
                print(" # response from coin gecko", data)
                price = data.get(coin, {}).get(cur)
                if price is not None:
                    price_decimal = Decimal(str(price))
                    data = {
                        'cur': cur,
                        'price': price_decimal
                    }
                    PersistenceManager.add_coin_record(pk_value, data)
                    return price
                else:
                    return ServiceManager.default_response("Requested combination not found")

            else:
                print('response ', response)
                return PersistenceManager.get_coin_price(pk_value)
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return {}
        
    @staticmethod
    def default_response(message: Optional[str]):
        if not message:
            message = "Resource not found"
        return {
            "statusCode": 404,
            "body": json.dumps({"message": message})
        }
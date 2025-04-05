
from service.service_manager import ServiceManager
from typing import Dict, Any, Optional
import json

def handler(event, context):
    try:
        path = event.get('path', '')
        query_params = event.get('queryStringParameters', {})
        coin, cur = '', '' 
        if query_params:
            coin = query_params.get('coin', '')
            cur = query_params.get('cur', '')
            coin, cur = coin.lower() if coin else coin, cur.lower() if cur else cur

        path_handlers = {
            '/coin/price': lambda: get_coin_price(coin, cur),
            '/coin/dataset': lambda: fetch_coin_dataset(coin, cur),
            '/coin/volrank': lambda: get_coin_volatile_rank(coin, cur)
        }
        result = path_handlers.get(path, lambda: handle_default())()
        print(" ###### result ", result)
        return {
                "statusCode": result.get("statusCode", 200) if isinstance(result, dict) else 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({
                    "data": result 
                })
            }
    except AttributeError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


def handle_default():
    return ServiceManager.default_response()


def get_coin_price(coin, cur):
    try:
        if not coin or not cur:
            return generate_error_response("Error processing price request. Missing query params")
        return ServiceManager.fetch_coin_price(coin, cur)
    except Exception as e:
        print(f"Error in fetch_coin_price: {e}")
        return generate_error_response("Error processing price request")

def fetch_coin_dataset(coin, cur):
    try:
        # if not coin or not cur:
        #     return generate_error_response("Error processing data set request. Missing query params")
        return ServiceManager.fetch_coin_dataset(coin, cur)
    except Exception as e:
        print(f"Error in fetch_coin_dataset: {e}")
        return generate_error_response("Error processing data set request")

def get_coin_volatile_rank(coin, cur):
    try:
        return ServiceManager.get_coin_rank(coin, cur)
    except Exception as e:
        print(f"Error in get_coin_volatile_rank: {e}")
        return generate_error_response("Error processing volatile rank request")

def generate_error_response(message):
    return {
        "statusCode": 400,
        "body": json.dumps({"error": message})
    }

import os
import boto3
import math
from typing import List, Dict, Optional
from boto3.dynamodb.conditions import Key
from collections import defaultdict
from botocore.exceptions import ClientError
from datetime import datetime
import random



dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.getenv('COIN_CURRENCY_TRACKER_TABLE'))
partition_key = 'key'
sort_key = 'dateTime'

def calculate_coin_deviation(prices):
    mean = sum(prices) / len(prices)
    variance = sum((price - mean) ** 2 for price in prices) / len(prices)
    std_deviation = math.sqrt(variance)
    round_dev = round(std_deviation, 2)
    return round_dev

def generate_random_color():
    #Generate a random hex color code for display
    return f"#{''.join(random.choices('0123456789ABCDEF', k=6))}"

class PersistenceManager:

    @staticmethod
    def add_coin_record(pk_value, data):
        try:
            record = {
                partition_key: pk_value,
                sort_key: datetime.now().isoformat()
            }
            record.update(data)
            print('adding record ', record)
            response = table.put_item(Item=record)
            print("Add record succeeded:", response)
        except ClientError as e:
            print("Error adding record:", e)

    @staticmethod
    def fetch_coin_ranks(pk_value: Optional[str]) -> List[Dict[str, str]]:
        response = table.scan()
        items = response.get('Items', [])
        grouped_items = defaultdict(list)
        for item in items:
            partition_key = item.get('key')
            grouped_items[partition_key].append(item)
        ranked_items = []
        for partition_key, records in grouped_items.items():
            prices = [(item['price']) for item in records if 'price' in item]
            std_deviation = calculate_coin_deviation(prices)
            rank_item = {
                'key': partition_key,
                'std_deviation': std_deviation
            }
            ranked_items.append(rank_item)
        sorted_items = sorted(ranked_items, key=lambda x: x.get('std_deviation', 0), reverse=True)
        for index, record in enumerate(sorted_items, start=1):
            record['rank'] = index
        if pk_value:
            filtered_data = [item for item in sorted_items if item["key"] == pk_value] 
            return filtered_data if filtered_data else sorted_items
        return sorted_items
    
    @staticmethod
    def get_coin_price(coinKey: str) -> Dict[str, str]:
        print('inside get_coin_price in PersistenceManager')
        table = dynamodb.Table(os.getenv('COIN_CURRENCY_TRACKER_TABLE'))
        response = table.query(
            KeyConditionExpression=Key('partitionKeyName').eq(coinKey),
            ScanIndexForward=False,
            Limit=1
        )
        items = response.get('Items', [])
        return float(items[0]["price"]) if items else {}

    @staticmethod
    def fetch_coin_dataset(coinKey: str) -> List[Dict[str, str]]:
        print(' pk_value ', coinKey)
        table = dynamodb.Table(os.getenv('COIN_CURRENCY_TRACKER_TABLE'))
        if coinKey:
            response = table.query(
                KeyConditionExpression=Key('key').eq(coinKey),
            )
            items = response['Items']

            return {
                coinKey: {
                    "label": coinKey,
                    "borderColor": generate_random_color(),
                    "data": [
                        {
                            "x": item["dateTime"],
                            "y": float(item["price"])
                        } for item in items
                    ]
                }
            }
        else:
            # Scan entire table if no coinKey provided
            response = table.scan()
            items = response['Items']
            grouped_data = {}
            for item in items:
                key = item["key"]
                if key not in grouped_data:
                    # Initialize new coin group with label and color
                    grouped_data[key] = {
                        "label": key,
                        "borderColor": generate_random_color(),
                        "data": []
                    }
                    grouped_data[key]["data"].append({
                        "x": item["dateTime"],
                        "y": float(item["price"])
                    })
            return grouped_data
        
# response = PersistenceManager.fetch_coin_dataset('bitcoin_usd')

# print(' # response data ', response)
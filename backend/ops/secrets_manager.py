import boto3
import json
from botocore.exceptions import ClientError

class SecretsManager:
    @staticmethod
    def get_secret(secret_name: str, region_name: str = "us-east-1") -> dict:
        client = boto3.client("secretsmanager", region_name=region_name)
        try:
            response = client.get_secret_value(SecretId=secret_name)
            if "SecretString" in response:
                secret_response = json.loads(response["SecretString"])
                print(f"Fetched secret_response {secret_response}")
                return secret_response["GECKO_API_KEY"]
            else:
                return json.loads(response["SecretBinary"].decode("utf-8"))
        except ClientError as e:
            print(f"Error fetching secret: {e}")
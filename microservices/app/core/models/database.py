import boto3
from core.settings import (AWS_DYNAMODB_ACCESS_KEY, AWS_DYNAMODB_ACCESS_KEY_ID,
                           AWS_DYNAMODB_REGION, AWS_DYNAMODB_TABLE_NAME)

dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_DYNAMODB_REGION,
    aws_access_key_id=AWS_DYNAMODB_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_DYNAMODB_ACCESS_KEY,
)

table = dynamodb.Table(AWS_DYNAMODB_TABLE_NAME)

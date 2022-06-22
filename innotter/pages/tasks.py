import boto3
from django.conf import settings

from innotter.celery import app


@app.task
def upload_file_to_s3(file_path, key):
    client = boto3.client(
        "s3", aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    client.upload_file(
        Filename=file_path,
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=key,
    )

from django.conf import settings
from innotter.celery import app
from users.services import client


@app.task
def upload_file_to_s3(file_path, key):
    client.upload_file(
        Filename=file_path,
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=key,
    )

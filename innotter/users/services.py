from datetime import datetime, timedelta

import boto3
import jwt
from django.conf import settings
from rest_framework.exceptions import NotFound, ValidationError

from innotter.settings import JWT_ACCESS_TTL, JWT_REFRESH_TTL, JWT_SECRET
from pages.models import Page
from pages.tasks import upload_file_to_s3
from users.models import User

client = boto3.client(
    "s3", aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
)


def upload_user_image_to_s3(file_path: str, user: User) -> str:
    if not is_allowed_file_extension(file_path=file_path):
        error_msg = "Files with this extension are not allowed."
        raise ValidationError(error_msg)

    key = generate_file_name(file_path=file_path, key=user.username, is_user_image=True)

    user.image_s3_path = key
    user.save()

    try:
        upload_file_to_s3.delay(file_path=file_path, key=key)
    except FileNotFoundError:
        error_msg = f"No such file or directory: {file_path}"
        raise NotFound(error_msg)

    presigned_url = get_presigned_url(key=key)

    return presigned_url


def get_presigned_url(key: str) -> str:
    presigned_url = client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": settings.AWS_STORAGE_BUCKET_NAME, "Key": key},
        ExpiresIn=3600,
    )
    return presigned_url


def generate_file_name(file_path: str, key: str, is_user_image: bool) -> str:
    extension = file_path.split(".")[-1]
    prefix_folder = "users" if is_user_image else "pages"
    return f"{prefix_folder}/{key}.{extension}"


def is_allowed_file_extension(file_path: str) -> bool:
    return file_path.split(".")[-1] in settings.ALLOWED_FILE_EXTENSIONS


def block_or_unblock_all_pages(user: User):
    pages = Page.objects.filter(owner=user)
    for page in pages:
        page.is_blocked = user.is_blocked
        page.save()


def set_access_to_admin_panel(user: User):
    if user.role == "admin":
        user.is_staff = True
        user.is_superuser = True
        user.save()
    else:
        user.is_staff = False
        user.is_superuser = False
        user.save()


def create_jwt_token_dict(to_refresh: bool, validated_data) -> dict:
    jwt_token_dict = {
        "access": _generate_jwt_token(is_access=True, to_refresh=to_refresh, validated_data=validated_data),
        "refresh": _generate_jwt_token(is_access=False, to_refresh=to_refresh, validated_data=validated_data),
    }
    return jwt_token_dict


def _generate_jwt_token(is_access: bool, to_refresh: bool, validated_data) -> str:
    """Generate acces or refresh token"""

    payload = _create_payload(is_access=is_access, to_refresh=to_refresh, validated_data=validated_data)
    token = jwt.encode(payload=payload, key=JWT_SECRET)
    return token


def _create_payload(is_access: bool, to_refresh: bool, validated_data) -> dict:
    """Create payload dict for jwt-token generation"""

    payload = {
        "iss": "backend-api",
        "token_type": "access" if is_access else "refresh",
        "user_id": validated_data["payload"]["user_id"] if to_refresh else validated_data["user"].id,
        "exp": datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TTL if is_access else JWT_REFRESH_TTL),
    }
    return payload

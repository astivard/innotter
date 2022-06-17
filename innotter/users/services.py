from datetime import datetime, timedelta

import jwt

from innotter.settings import JWT_SECRET, JWT_ACCESS_TTL, JWT_REFRESH_TTL


def create_jwt_token_dict(to_refresh: bool, validated_data) -> dict:
    jwt_token_dict = {
        'access': _generate_jwt_token(is_access=True, to_refresh=to_refresh, validated_data=validated_data),
        'refresh': _generate_jwt_token(is_access=False, to_refresh=to_refresh, validated_data=validated_data)
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
        'iss': 'backend-api',
        'token_type': 'access' if is_access else 'refresh',
        'user_id': validated_data['payload']['user_id'] if to_refresh else validated_data['user'].id,
        'exp': datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TTL if is_access else JWT_REFRESH_TTL),
    }
    return payload

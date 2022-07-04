from core.settings import SECRET_KEY
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBearer
from jose import jwt
from jose.exceptions import JOSEError

security = HTTPBearer()


async def has_access(credentials: HTTPBasicCredentials = Depends(security)):
    """Function that is used to validate the token in the case that it requires it"""

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token, key=SECRET_KEY, options={"verify_signature": False, "verify_aud": False, "verify_iss": False}
        )
    except JOSEError as e:
        raise HTTPException(status_code=401, detail=str(e))
    return payload["user_id"]

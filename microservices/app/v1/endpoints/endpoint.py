from core.jwt_auth import has_access
from core.models.services import get_user_statistics
from fastapi import APIRouter, Depends

router = APIRouter(tags=["items"], responses={404: {"description": "Page not found"}})


@router.get("/statistics", summary="Get statistics of jwt-token owner")
async def get_statistics(user_id: int = Depends(has_access)):
    return get_user_statistics(user_id)

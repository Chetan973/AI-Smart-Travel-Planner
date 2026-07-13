from fastapi import APIRouter
from fastapi import HTTPException

from app.api.travel_schemas import (
    TravelSearchRequest,
    TravelSearchResponse
)
from app.services.travel_service import TravelService

router = APIRouter(
    prefix="/api/travel",
    tags=["Travel"]
)


@router.post(
    "/search",
    response_model=TravelSearchResponse
)
def search_travel(
    request: TravelSearchRequest
):

    try:

        return TravelService.search(
            request
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )
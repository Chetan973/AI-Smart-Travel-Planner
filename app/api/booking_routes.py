from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.api.booking_schemas import (
    BookingResponse,
    CreateBookingRequest
)
from app.database import get_db
from app.services.booking_service import BookingService

router = APIRouter(
    prefix="/api/bookings",
    tags=["Bookings"]
)


@router.post(
    "/create",
    response_model=BookingResponse
)
def create_booking(
    request: CreateBookingRequest,
    db: Session = Depends(get_db)
):

    try:

        return BookingService.create_booking(
            db,
            request
        )

    except ValueError as ex:

        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.booking_schemas import (
    BookingHistoryResponse,
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

@router.get(
    "/user/{user_id}",
    response_model=List[BookingHistoryResponse]
)
def get_user_bookings(

    user_id: int,

    db: Session = Depends(get_db)

):

    return BookingService.get_user_bookings(

        db,

        user_id

    )
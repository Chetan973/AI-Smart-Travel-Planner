from datetime import date

from pydantic import BaseModel

from app.enums.booking_status import BookingStatus


class CreateBookingRequest(BaseModel):
    """
    Request received from frontend.
    """

    user_id: int

    session_id: str

    option_id: int

    passengers: int = 1


class BookingResponse(BaseModel):

    booking_reference: str

    booking_status: BookingStatus

    provider: str

    transport_name: str

    source: str

    destination: str

    journey_date: date

    departure_time: str

    arrival_time: str

    passengers: int

    total_amount: float

    payment_completed: bool

    message: str


class BookingHistoryResponse(BaseModel):

    booking_id: int

    booking_reference: str

    provider: str

    travel_mode: str

    transport_name: str

    transport_number: str

    source: str

    destination: str

    journey_date: date

    departure_time: str

    arrival_time: str

    passengers: int

    total_amount: float

    booking_status: BookingStatus

    payment_completed: bool
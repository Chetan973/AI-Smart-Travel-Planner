from datetime import date
from typing import Optional

from pydantic import BaseModel

from app.enums.payment_status import PaymentStatus
from app.enums.travel_mode import TravelMode


class TravelState(BaseModel):

    # User
    user_id: Optional[int] = None
    session_id: Optional[str] = None

    full_name: Optional[str] = None
    email: Optional[str] = None

    # Travel
    source: Optional[str] = None
    destination: Optional[str] = None

    journey_date: Optional[date] = None
    return_date: Optional[date] = None

    travel_mode: Optional[TravelMode] = None

    passengers: int = 1

    # AI Response
    ai_response: Optional[str] = None

    # Provider
    provider: Optional[str] = None
    available_options: list = []

    # Booking
    booking_id: Optional[str] = None

    # Payment
    payment_status: Optional[PaymentStatus] = None

    # Workflow
    next_node: Optional[str] = None
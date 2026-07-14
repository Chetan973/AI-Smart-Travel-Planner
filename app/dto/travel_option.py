from decimal import Decimal

from pydantic import BaseModel
from pydantic import Field


class TravelOption(BaseModel):
    """
    Common DTO returned by all travel providers.
    """
    option_id: int | None = None

    provider: str

    travel_mode: str

    transport_name: str

    transport_number: str | None = None

    source: str

    destination: str

    departure_time: str

    arrival_time: str

    duration: str

    price: Decimal

    available_seats: int

    currency: str = "INR"

    booking_url: str | None = None

    rating: float | None = None

    amenities: list[str] = Field(default_factory=list)
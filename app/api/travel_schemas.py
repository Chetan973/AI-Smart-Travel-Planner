from datetime import date

from pydantic import BaseModel

from app.dto.travel_option import TravelOption
from app.enums.travel_mode import TravelMode


class TravelSearchRequest(BaseModel):

    user_id: int

    session_id: str

    source: str

    destination: str

    journey_date: date

    travel_mode: TravelMode

    passengers: int = 1


class TravelSearchResponse(BaseModel):

    recommendation: str

    provider: str

    travel_options: list[TravelOption]
from pydantic import BaseModel


class HotelOption(BaseModel):

    hotel_id: str

    provider: str

    hotel_name: str

    city: str

    room_type: str

    room_count: int

    check_in_date: str

    check_out_date: str

    adults: int

    children: int

    price: float

    currency: str

    rating: float

    amenities: list[str]

    booking_url: str
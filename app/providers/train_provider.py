from decimal import Decimal

from app.dto.travel_option import TravelOption
from app.enums.provider_type import ProviderType
from app.providers.base_provider import BaseProvider


class TrainProvider(BaseProvider):
    """
    Mock MakeMyTrip Train Provider

    Later replace the mock response with the
    real MakeMyTrip Affiliate API.
    """

    def search(
        self,
        source: str,
        destination: str,
        journey_date: str
    ) -> list[TravelOption]:

        return [

            TravelOption(

                provider=ProviderType.MAKEMYTRIP.value,

                travel_mode="TRAIN",

                transport_name="Vande Bharat Express",

                transport_number="20661",

                source=source,

                destination=destination,

                departure_time="06:00",

                arrival_time="10:45",

                duration="4h 45m",

                price=Decimal("875.00"),

                available_seats=43,

                currency="INR",

                booking_url="https://mock.makemytrip.com/train",

                rating=4.8,

                amenities=[
                    "WiFi",
                    "Charging Point",
                    "Food",
                    "AC Chair Car"
                ]

            )

        ]
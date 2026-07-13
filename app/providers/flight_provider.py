from decimal import Decimal

from app.dto.travel_option import TravelOption
from app.enums.provider_type import ProviderType
from app.providers.base_provider import BaseProvider


class FlightProvider(BaseProvider):
    """
    Mock Agoda Flight Provider

    Later replace with the
    Agoda Affiliate Flight API.
    """

    def search(
        self,
        source: str,
        destination: str,
        journey_date: str
    ) -> list[TravelOption]:

        return [

            TravelOption(

                provider=ProviderType.AGODA.value,

                travel_mode="FLIGHT",

                transport_name="IndiGo",

                transport_number="6E-721",

                source=source,

                destination=destination,

                departure_time="09:30",

                arrival_time="10:35",

                duration="1h 05m",

                price=Decimal("3499.00"),

                available_seats=12,

                currency="INR",

                booking_url="https://mock.agoda.com/flight",

                rating=4.7,

                amenities=[
                    "Cabin Bag",
                    "Window Seat",
                    "Meal",
                    "Priority Boarding"
                ]

            )

        ]
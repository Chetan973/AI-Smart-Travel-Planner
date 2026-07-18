from decimal import Decimal
from app.dto.travel_option import TravelOption
from app.enums.provider_type import ProviderType
from app.providers.aviationstack_provider import AviationStackProvider
from app.providers.base_provider import BaseProvider

class FlightProvider(BaseProvider):
    def get_mode(self) -> str:
        return "FLIGHT"
    
    def _search_live(
        self,
        source,
        destination,
        journey_date,
    ):

        provider = AviationStackProvider()

        flights = provider.future_flights(
            source,
            destination,
            journey_date,
        )

        options = []

        for item in flights:

            options.append(
                TravelOption(
                    provider=ProviderType.AGODA.value,
                    travel_mode="FLIGHT",
                    transport_name=item["airline"]["name"],
                    transport_number=item["flight"]["iata"],
                    source=source,
                    destination=destination,
                    departure_time=item["departure"]["scheduled"],
                    arrival_time=item["arrival"]["scheduled"],
                    duration="Unknown",
                    price=Decimal("0.00"),
                    available_seats=0,
                    currency="INR",
                    booking_url=None,
                    rating=4.5,
                    amenities=[],
                )
            )

        return options

    def get_mock_data(self, source: str, destination: str, journey_date: str) -> list[TravelOption]:
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
                amenities=["Cabin Bag", "Window Seat", "Meal", "Priority Boarding"]
            )
        ]
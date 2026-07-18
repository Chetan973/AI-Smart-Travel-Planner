from decimal import Decimal
from app.dto.travel_option import TravelOption
from app.enums.provider_type import ProviderType
from app.providers.base_provider import BaseProvider

class BusProvider(BaseProvider):
    def get_mode(self) -> str:
        return "BUS"

    def get_mock_data(self, source: str, destination: str, journey_date: str) -> list[TravelOption]:
        return [
            TravelOption(
                provider=ProviderType.REDBUS.value,
                travel_mode="BUS",
                transport_name="KSRTC Airavat Club Class",
                transport_number="KA-01-F-1024",
                source=source,
                destination=destination,
                departure_time="22:00",
                arrival_time="05:30",
                duration="7h 30m",
                price=Decimal("650.00"),
                available_seats=18,
                currency="INR",
                booking_url="https://mock.redbus.com/bus",
                rating=4.6,
                amenities=["AC", "Blanket", "Charging Point", "Water Bottle", "Live Tracking"]
            )
        ]
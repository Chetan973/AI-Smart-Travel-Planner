from decimal import Decimal

from app.dto.travel_option import TravelOption
from app.enums.provider_type import ProviderType
from app.providers.base_provider import BaseProvider


class HotelProvider(BaseProvider):
    """Mock hotel provider kept compatible with the common provider contract."""

    def search(self, source: str, destination: str, journey_date: str) -> list[TravelOption]:
        return [
            TravelOption(
                provider=ProviderType.AGODA.value,
                travel_mode="HOTEL",
                transport_name="City Stay Hotel",
                transport_number=None,
                source=source,
                destination=destination,
                departure_time="15:00",
                arrival_time="11:00",
                duration="1 night",
                price=Decimal("3200.00"),
                available_seats=5,
                currency="INR",
                booking_url="https://mock.agoda.com/hotel",
                rating=4.5,
                amenities=["Wi-Fi", "Breakfast", "Air conditioning"],
            )
        ]

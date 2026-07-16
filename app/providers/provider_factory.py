from app.enums.travel_mode import TravelMode
from app.providers.base_provider import BaseProvider
from app.providers.bus_provider import BusProvider
from app.providers.flight_provider import FlightProvider
from app.providers.train_provider import TrainProvider
from app.providers.hotel_provider import HotelProvider

class ProviderFactory:
    # """
    # Factory class responsible for returning the
    # appropriate travel provider based on travel mode.

    # Current Providers
    # -----------------
    # TRAIN  -> MakeMyTrip (Mock)
    # BUS    -> RedBus (Mock)
    # FLIGHT -> Agoda (Mock)

    # Future
    # ------
    # Replace the mock providers with real Affiliate APIs
    # without changing the rest of the application.
    # """

    """
    Returns provider implementation based on travel mode.
    """

    @staticmethod
    def get_provider(
        travel_mode: TravelMode
    ) -> BaseProvider:

        if travel_mode == TravelMode.TRAIN:
            return TrainProvider()

        elif travel_mode == TravelMode.BUS:
            return BusProvider()

        elif travel_mode == TravelMode.FLIGHT:
            return FlightProvider()
        
        elif travel_mode == TravelMode.HOTEL:
            return HotelProvider()
        
        

        raise ValueError(
            f"Unsupported travel mode: {travel_mode}"
        )
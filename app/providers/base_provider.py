from abc import ABC, abstractmethod

from app.config import settings
from app.dto.travel_option import TravelOption


class BaseProvider(ABC):
    """
    Base contract for all travel providers.

    Search Priority

    1. Provider-specific live API
    2. Google Search
    3. Serper Search
    4. Mock Data
    """

    def search(
        self,
        source: str,
        destination: str,
        journey_date: str,
    ) -> list[TravelOption]:

        try:
            # 1. Provider API
            options = self.search_provider(
                source,
                destination,
                journey_date,
            )
            if options:
                print(f"✅ {self.get_mode()} Provider API")
                return options

            # 2. Google Search
            if settings.google_search_enabled:
                options = self.search_google(
                    source,
                    destination,
                    journey_date,
                )
                if options:
                    print("✅ Google Search")
                    return options
            # 3. Serper
            if settings.serper_enabled:
                options = self.search_serper(
                    source,
                    destination,
                    journey_date,
                )
                if options:
                    print("✅ Serper Search")
                    return options
        except Exception as ex:

            print(f"{self.get_mode()} provider failed : {ex}")
        print("⚠ Falling back to mock data")
        return self.get_mock_data(
            source,
            destination,
            journey_date,
        )

    @abstractmethod
    def get_mock_data(
        self,
        source: str,
        destination: str,
        journey_date: str,
    ) -> list[TravelOption]:
        ...

    @abstractmethod
    def get_mode(self) -> str:
        ...
from abc import ABC
from abc import abstractmethod

from app.dto.travel_option import TravelOption


class BaseProvider(ABC):

    @abstractmethod
    def search(
        self,
        source: str,
        destination: str,
        journey_date: str
    ) -> list[TravelOption]:
        pass
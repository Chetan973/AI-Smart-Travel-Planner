from abc import ABC
from abc import abstractmethod

from app.dto.travel_option import TravelOption


class BaseProvider(ABC):
    """
    Base contract for all travel providers.

    Every provider (Train / Flight / Hotel / Bus)
    must return List[TravelOption].

    This allows LangGraph to remain provider-agnostic.
    """

    @abstractmethod
    def search(
        self,
        source: str,
        destination: str,
        journey_date: str,
    ) -> list[TravelOption]:
        """
        Search available travel options.

        Returns
        -------
        List[TravelOption]
        """
        raise NotImplementedError
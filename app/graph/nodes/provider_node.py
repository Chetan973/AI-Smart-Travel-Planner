from httpx import options

from app.graph.state.travel_state import TravelState
from app.providers.provider_factory import ProviderFactory
from app.memory.travel_memory import TravelMemory


class ProviderNode:
    """
    Provider Search Node

    This node calls the appropriate provider
    based on the selected travel mode.

    Current Providers
    -----------------
    TRAIN   -> MakeMyTrip (Mock)

    BUS     -> RedBus (Mock)

    FLIGHT  -> Agoda (Mock)

    Future
    ------
    Replace mock providers with real
    affiliate APIs without changing
    LangGraph.
    """

    @staticmethod
    def search(
        state: TravelState
    ) -> TravelState:

        print("=" * 60)
        print("Searching Travel Provider")
        print("=" * 60)

        provider = ProviderFactory.get_provider(
            state.travel_mode
        )

        options = provider.search(

            source=state.source,

            destination=state.destination,

            journey_date=str(state.journey_date)

        )
        state.travel_options = []

        if options:

            state.provider = options[0].provider

            for index, option in enumerate(options, start=1):

                item = option.model_dump()

                item["option_id"] = index

                state.travel_options.append(item)

            print(f"Provider : {state.provider}")

            print(f"Options  : {len(state.travel_options)}")

        else:

            state.provider = None

            print("No travel options found.")
        TravelMemory.save(state)

        return state
from app.graph.state.travel_state import TravelState
from app.providers.provider_factory import ProviderFactory


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

        if options:

            state.provider = options[0].provider

            state.travel_options = [

                option.model_dump()

                for option in options

            ]

            print(f"Provider : {state.provider}")

            print(f"Options  : {len(state.travel_options)}")

        else:

            state.provider = None

            state.travel_options = []

            print("No travel options found.")

        return state
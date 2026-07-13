from app.graph.state.travel_state import TravelState


class TravelNode:

    @staticmethod
    def validate_request(
        state: TravelState
    ) -> TravelState:

        print("=" * 60)
        print("Travel Request Validation")
        print("=" * 60)

        if not state.source:
            raise ValueError("Source is required.")

        if not state.destination:
            raise ValueError("Destination is required.")

        if state.source == state.destination:
            raise ValueError(
                "Source and Destination cannot be same."
            )

        print("Travel Request Validated Successfully")

        return state
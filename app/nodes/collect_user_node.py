from app.state.travel_state import TravelState


def collect_user_node(state: TravelState) -> TravelState:

    print("Collecting User Information")

    state.response = (
        f"Welcome {state.full_name} to AI Smart Travel Planner"
    )

    return state
from app.state.travel_state import TravelState


def validate_user_node(state: TravelState) -> TravelState:

    print("Validating User")

    if not state.full_name:
        raise ValueError("Full Name is required")

    if not state.email:
        raise ValueError("Email is required")

    return state
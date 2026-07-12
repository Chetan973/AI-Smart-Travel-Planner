from app.state.travel_state import TravelState


def welcome_node(state: TravelState):

    state["response"] = (
        f"Welcome {state['full_name']} "
        "to AI Smart Travel Planner"
    )

    return state
from app.enums import GraphStatus
from app.state.travel_state import TravelState


def start_node(state: TravelState) -> TravelState:

    print("Starting Travel Planner Workflow")

    state.graph_status = GraphStatus.RUNNING

    return state
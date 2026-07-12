from app.enums import GraphStatus
from app.state.travel_state import TravelState


def end_node(state: TravelState) -> TravelState:

    print("Workflow Completed")

    state.graph_status = GraphStatus.COMPLETED

    return state
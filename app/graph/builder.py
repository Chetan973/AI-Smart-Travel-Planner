from langgraph.graph import StateGraph

from app.state.travel_state import TravelState


def build_graph():

    return StateGraph(TravelState)
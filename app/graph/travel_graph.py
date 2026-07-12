from langgraph.graph import END
from langgraph.graph import START
from langgraph.graph import StateGraph

from app.nodes.welcome_node import welcome_node
from app.state.travel_state import TravelState


builder = StateGraph(TravelState)

builder.add_node("welcome", welcome_node)

builder.add_edge(START, "welcome")

builder.add_edge("welcome", END)

travel_graph = builder.compile()
from langgraph.graph import END, START, StateGraph

from app.graph.checkpoints.redis_checkpointer import GraphCheckpointer
from app.graph.nodes.ai_node import AINode
from app.graph.nodes.provider_node import ProviderNode
from app.graph.nodes.travel_node import TravelNode
from app.graph.nodes.user_node import UserNode
from app.graph.state.travel_state import TravelState


class GraphBuilder:
    """Persistent, turn-based travel conversation state machine."""

    @staticmethod
    def build():
        graph = StateGraph(TravelState)
        graph.add_node("classify_intent", UserNode.classify_intent)
        graph.add_node("greet", AINode.greet)
        graph.add_node("collect_details", TravelNode.collect_details)
        graph.add_node("ask_for_details", AINode.ask_for_details)
        graph.add_node("search_options", ProviderNode.search)
        graph.add_node("recommend", AINode.recommend)
        graph.add_node("confirm_selection", AINode.confirm_selection)

        graph.add_edge(START, "classify_intent")
        graph.add_conditional_edges("classify_intent", lambda state: state.next_node, {"greet": "greet", "collect_details": "collect_details", "confirm_selection": "confirm_selection"})
        graph.add_edge("greet", END)
        graph.add_edge("confirm_selection", END)
        graph.add_conditional_edges("collect_details", lambda state: state.next_node, {"ask_for_details": "ask_for_details", "search_options": "search_options"})
        graph.add_edge("ask_for_details", END)
        graph.add_edge("search_options", "recommend")
        graph.add_edge("recommend", END)
        return graph.compile(checkpointer=GraphCheckpointer.get_checkpointer())

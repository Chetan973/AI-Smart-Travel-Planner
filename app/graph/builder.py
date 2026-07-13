from langgraph.graph import END
from langgraph.graph import START
from langgraph.graph import StateGraph

from app.graph.checkpoints.redis_checkpointer import GraphCheckpointer
from app.graph.nodes.ai_node import AINode
from app.graph.nodes.travel_node import TravelNode
from app.graph.nodes.user_node import UserNode
from app.graph.state.travel_state import TravelState


class GraphBuilder:

    @staticmethod
    def build():

        graph = StateGraph(TravelState)

        graph.add_node(
            "initialize_user",
            UserNode.initialize
        )

        graph.add_node(
            "validate_request",
            TravelNode.validate_request
        )

        graph.add_node(
            "ai_recommendation",
            AINode.recommend
        )

        graph.add_edge(
            START,
            "initialize_user"
        )

        graph.add_edge(
            "initialize_user",
            "validate_request"
        )

        graph.add_edge(
            "validate_request",
            "ai_recommendation"
        )

        graph.add_edge(
            "ai_recommendation",
            END
        )

        return graph.compile(
            checkpointer=GraphCheckpointer.get_checkpointer()
        )
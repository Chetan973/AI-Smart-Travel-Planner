# app/memory/travel_memory.py
from app.graph.travel_workflow import travel_agent
from app.graph.state.travel_state import TravelState

class TravelMemory:
    """
    Bridge memory layer.
    Allows legacy services (like BookingService) to read session details 
    directly out of the active LangGraph PostgreSQL/Redis checkpointer threads.
    """

    @staticmethod
    def get(session_id: str) -> TravelState | None:
        """Fetches the current state out of the persistent checkpointer thread."""
        config = {"configurable": {"thread_id": session_id}}
        state_snapshot = travel_agent.get_state(config)
        
        if state_snapshot and state_snapshot.values:
            # Rehydrate the data into the Pydantic TravelState model
            return TravelState(**state_snapshot.values)
        return None

    @staticmethod
    def save(state: TravelState):
        """
        Saves state to the checkpointer thread.
        LangGraph updates state automatically during execution, but this provides
        a safe fallback wrapper for legacy code compatibility.
        """
        if hasattr(state, "session_id") and state.session_id:
            config = {"configurable": {"thread_id": state.session_id}}
            travel_agent.update_state(config, state.model_dump())


class TravelMemory:
    """Read the durable graph checkpoint for booking validation."""

    @staticmethod
    def get(session_id: str) -> dict | None:
        config = {"configurable": {"thread_id": session_id}}
        snapshot = travel_agent.get_state(config)
        return dict(snapshot.values) if snapshot and snapshot.values else None

    @staticmethod
    def load(session_id: str) -> dict | None:
        return TravelMemory.get(session_id)

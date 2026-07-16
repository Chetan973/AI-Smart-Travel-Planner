from app.api.chat_schemas import ChatRequest, ChatResponse
from app.graph.state.travel_state import TravelState
from app.graph.workflow import travel_graph


class ChatService:
    """Application boundary for one LangGraph conversation turn."""

    @staticmethod
    def reply(request: ChatRequest) -> ChatResponse:
        config = {"configurable": {"thread_id": request.session_id}}
        result = travel_graph.invoke(
            {"session_id": request.session_id, "input_message": request.message},
            config=config,
        )
        state = TravelState.model_validate(result)
        return ChatResponse(
            session_id=request.session_id,
            message=state.ai_response or "How can I help with your trip?",
            phase=state.conversation_phase,
            missing_fields=state.missing_fields,
            travel_details={
                "source": state.source,
                "destination": state.destination,
                "journey_date": str(state.journey_date) if state.journey_date else None,
                "travel_mode": state.travel_mode.value if state.travel_mode else None,
                "passengers": state.passengers,
            },
            travel_options=state.travel_options,
        )

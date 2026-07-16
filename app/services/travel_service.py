from app.api.travel_schemas import (
    TravelSearchRequest,
    TravelSearchResponse,
)
from app.graph.state.travel_state import TravelState
from app.graph.workflow import travel_graph


class TravelService:
    """
    Executes the LangGraph workflow for travel search.
    """

    @staticmethod
    def search(
        request: TravelSearchRequest
    ) -> TravelSearchResponse:

        # ==========================================
        # Build LangGraph State
        # ==========================================

        state = TravelState(

            session_id=request.session_id,

            user_id=request.user_id,

            source=request.source,

            destination=request.destination,

            journey_date=request.journey_date,

            travel_mode=request.travel_mode,

            passengers=request.passengers

        )

        # ==========================================
        # LangGraph Config
        # ==========================================

        config = {

            "configurable": {

                "thread_id": request.session_id

            }

        }

        # ==========================================
        # Execute Graph
        # ==========================================

        result = travel_graph.invoke(
            state,
            config=config
        )

        print("=" * 60)
        print(type(result))
        print(result)
        print("=" * 60)


        # Convert dict -> TravelState
        result = TravelState.model_validate(result)

        # ==========================================
        # Build Response
        # ==========================================

        return TravelSearchResponse(

            recommendation=result.ai_response,

            provider=result.provider,

            travel_options=result.travel_options

        )
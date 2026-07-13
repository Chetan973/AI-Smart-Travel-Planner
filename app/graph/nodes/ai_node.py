from app.graph.state.travel_state import TravelState
from app.llm.llm_factory import LLMFactory


class AINode:

    @staticmethod
    def recommend(
        state: TravelState
    ) -> TravelState:

        prompt = f"""
You are an AI Travel Planner.

Traveller Name:
{state.full_name}

Source:
{state.source}

Destination:
{state.destination}

Travel Mode:
{state.travel_mode.value}

Passengers:
{state.passengers}

Give:

1. Best recommendation.

2. Estimated travel duration.

3. Helpful travel tips.

Keep answer under 120 words.
"""

        state.ai_response = LLMFactory.invoke(prompt)

        return state
from app.graph.state.travel_state import TravelState


class AINode:
    """Response-writing nodes. These are deterministic so chat works without API keys."""

    QUESTIONS = {
        "destination": "Where would you like to travel?",
        "source": "Great choice. Which city are you travelling from?",
        "journey_date": "What is your departure date? You can use YYYY-MM-DD, 'tomorrow', or 'next week'.",
        "travel_mode": (
            "Would you like to travel by Train, Bus, Flight, "
            "or should I compare all options?"
        ),
        "budget": "What is your maximum budget in rupees? For example: ₹3000.",
        "travel_preference": "Do you prefer the lowest price or the fastest journey?",
        "passengers": "How many passengers are travelling?",
    }

    @staticmethod
    def greet(_: TravelState) -> dict:
        return {"ai_response": "Hi! I’m your AI travel planner. Tell me where you’d like to go, or say ‘I want to book a trip’.", "conversation_phase": "IDLE"}

    @staticmethod
    def ask_for_details(state: TravelState) -> dict:
        field = state.missing_fields[0]
        return {"ai_response": AINode.QUESTIONS[field]}

    @staticmethod
    def recommend(state: TravelState) -> dict:
        count = len(state.travel_options)
        if not count:
            return {"ai_response": "I couldn't find an option for that journey. Try another date or travel mode.", "conversation_phase": "COLLECTING_DETAILS"}
        choice = next((option for option in state.travel_options if option["option_id"] == state.recommended_option_id), state.travel_options[0])
        return {
            "ai_response": (
                f"I checked train, flight, and bus options. My recommendation is {choice['travel_mode'].title()}: "
                f"{choice['duration']}, ₹{choice['price']}. Say ‘book the {choice['travel_mode'].lower()}’ or choose an option below."
            ),
            "conversation_phase": "OPTIONS_READY",
        }

    @staticmethod
    def confirm_selection(state: TravelState) -> dict:
        option = state.selected_option
        return {"ai_response": f"Great choice. I selected the {option['travel_mode'].title()} for ₹{option['price']}. Please enter traveller details so I can verify your email and issue a mock ticket.", "conversation_phase": "AWAITING_TRAVELLER"}

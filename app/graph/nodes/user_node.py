from app.graph.state.travel_state import TravelState


class UserNode:
    @staticmethod
    def classify_intent(state: TravelState) -> dict:
        text = (state.input_message or "").strip().lower()
        if state.conversation_phase == "OPTIONS_READY" and any(word in text for word in ("book", "yes", "confirm")):
            selected = next((item for item in state.travel_options if item["travel_mode"].lower() in text), None)
            selected = selected or next((item for item in state.travel_options if item["option_id"] == state.recommended_option_id), None)
            if selected:
                return {"selected_option": selected, "selected_option_id": selected["option_id"], "next_node": "confirm_selection"}
        greeting = text in {"hi", "hello", "hey", "hi travel planner", "hello travel planner"}
        wants_booking = any(term in text for term in ("book", "travel", "trip", "flight", "train", "bus", "go to"))
        if greeting and not wants_booking:
            return {"requested_action": "GREETING", "next_node": "greet"}
        return {"requested_action": "BOOKING" if wants_booking or state.conversation_phase != "IDLE" else "GENERAL", "next_node": "collect_details"}

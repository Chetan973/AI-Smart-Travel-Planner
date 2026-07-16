# app/graph/nodes/travel_node.py
import re
from datetime import date, timedelta
from app.enums.travel_mode import TravelMode
from app.graph.state.travel_state import TravelState

# Import the gazetteer we created to block gibberish and correct spelling
from app.utils.city_gazetteer import validate_and_correct_city

class TravelNode:
    """Extract travel slots and decide the next conversational question."""

    REQUIRED_FIELDS = ("destination", "source", "journey_date", "travel_mode", "budget", "travel_preference")

    @staticmethod
    def collect_details(state: TravelState) -> dict:
        message = (state.input_message or "").strip()
        text = message.lower()
        updates = TravelNode._extract(state, message)
        
        # Track if we rejected a location due to gibberish
        rejected_location = False

        # A single word/phrase answers the question currently being asked.
        missing_before = TravelNode._missing(state)
        if missing_before:
            field = missing_before[0]
            if field == "destination" and not updates.get("destination") and TravelNode._looks_like_place(message):
                is_valid, corrected = validate_and_correct_city(message)
                if is_valid:
                    updates["destination"] = corrected
                else:
                    rejected_location = True
            elif field == "source" and not updates.get("source") and TravelNode._looks_like_place(message):
                is_valid, corrected = validate_and_correct_city(message)
                if is_valid:
                    updates["source"] = corrected
                else:
                    rejected_location = True
            elif field == "budget":
                budget = re.search(r"(\d+(?:\.\d+)?)", text)
                if budget:
                    value = float(budget.group(1))
                    if value > 0:
                        updates["budget"] = value
            elif field == "travel_preference" and any(word in text for word in ("budget", "cheap", "fast", "speed", "quick")):
                updates["travel_preference"] = "FASTEST" if any(word in text for word in ("fast", "speed", "quick")) else "BUDGET"
            elif field == "passengers" and message.isdigit() and int(message) > 0:
                updates["passengers"] = int(message)

        merged = state.model_copy(update=updates)
        missing = TravelNode._missing(merged)
        
        # If the user entered gibberish, we intercept the flow here
        if rejected_location:
            return {
                **updates,
                "missing_fields": missing,
                "conversation_phase": "COLLECTING_DETAILS",
                "next_node": "ask_for_details",
                "agent_response": "I didn't quite recognize that city name. Could you please check the spelling and provide a valid location?"
            }

        if missing:
            return {
                **updates,
                "missing_fields": missing,
                "conversation_phase": "COLLECTING_DETAILS",
                "next_node": "ask_for_details",
            }
        return {
            **updates,
            "missing_fields": [],
            "conversation_phase": "PLANNING",
            "next_node": "search_options",
        }

    @staticmethod
    def _missing(state: TravelState) -> list[str]:
        values = {
            "destination": state.destination,
            "source": state.source,
            "journey_date": state.journey_date,
            "travel_mode": state.travel_mode,
            "budget": state.budget,
            "travel_preference": state.travel_preference,
        }
        return [field for field in TravelNode.REQUIRED_FIELDS if not values[field]]

    @staticmethod
    def _extract(state: TravelState, message: str) -> dict:
        text = message.lower()
        updates: dict = {}

        if any(word in text for word in ("flight", "fly", "plane")):
            updates["travel_mode"] = TravelMode.FLIGHT
        elif "train" in text:
            updates["travel_mode"] = TravelMode.TRAIN
        elif "bus" in text:
            updates["travel_mode"] = TravelMode.BUS

        route = re.search(r"(?:from|fr)\s+([a-zA-Z][a-zA-Z .'-]*?)\s+(?:to)\s+([a-zA-Z][a-zA-Z .'-]*?)(?=\s+(?:on|by|via|for|next|tomorrow)|[,.!?]|$)", message, re.I)
        if route:
            # Validate extracted source
            src_valid, src_corr = validate_and_correct_city(route.group(1).strip())
            if src_valid: updates["source"] = src_corr
            
            # Validate extracted destination
            dst_valid, dst_corr = validate_and_correct_city(route.group(2).strip())
            if dst_valid: updates["destination"] = dst_corr
        else:
            destination = re.search(r"\bto\s+([a-zA-Z][a-zA-Z .'-]*?)(?=\s+(?:on|by|via|for|next|tomorrow)|[,.!?]|$)", message, re.I)
            if destination:
                candidate = destination.group(1).strip()
                if candidate.lower() not in {"book", "travel", "trip", "go"}:
                    # Validate extracted destination
                    dst_valid, dst_corr = validate_and_correct_city(candidate)
                    if dst_valid: updates["destination"] = dst_corr

        iso_date = re.search(r"\b(20\d{2}-\d{2}-\d{2})\b", message)
        if iso_date:
            updates["journey_date"] = date.fromisoformat(iso_date.group(1))
        elif "tomorrow" in text:
            updates["journey_date"] = date.today() + timedelta(days=1)
        elif "next week" in text:
            updates["journey_date"] = date.today() + timedelta(days=7)

        passengers = re.search(r"\b(\d+)\s*(?:passengers?|people|persons|travellers?)\b", text)
        if passengers and int(passengers.group(1)) > 0:
            updates["passengers"] = int(passengers.group(1))
            
        budget_match = re.search(
            r"(?:₹|rs\.?|inr|budget|under|less than|within)\s*(\d+(?:\.\d+)?)",text,
        )
        if budget_match:
            value = float(budget_match.group(1))
            if value > 0:
                updates["budget"] = value
                
        if any(word in text for word in ("fastest", "fast", "speed", "quick")):
            updates["travel_preference"] = "FASTEST"
        elif any(word in text for word in ("budget", "cheapest", "cheap", "lowest price")):
            updates["travel_preference"] = "BUDGET"
            
        return updates

    @staticmethod
    def _looks_like_place(message: str) -> bool:
        candidate = message.strip().lower()
        intent_words = {"book", "booking", "want", "travel", "trip", "flight", "train", "bus", "go"}
        return (
            bool(re.fullmatch(r"[a-zA-Z][a-zA-Z .'-]{1,60}", candidate))
            and not any(word in candidate.split() for word in intent_words)
        )
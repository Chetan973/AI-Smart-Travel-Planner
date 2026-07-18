# app/graph/nodes/travel_node.py
from __future__ import annotations
import re
from datetime import date, timedelta
from typing import Any
from app.graph.state.travel_state import TravelState
from app.utils.city_gazetteer import validate_and_correct_city

class TravelQueryExtractor:
    """Parses queries to extract targets, relative dates, preferences, and budgets."""
    
    _route_pattern = re.compile(
        r"\bfrom\s+([a-zA-Z\s]+?)\s+to\s+([a-zA-Z\s]+?)(?=$|\b(?:tomorrow|today|next|this|after|in|on|under|below|within|budget|cheapest|lowest|fastest|best|luxury|economy|sleeper|ac|non-ac|morning|evening|for|with)\b|₹|rs\.?|[0-9])",
        re.IGNORECASE,
    )
    _to_only_pattern = re.compile(
        r"\b(?:to|in|at)\s+([a-zA-Z\s]+?)(?=$|\b(?:tomorrow|today|next|this|after|on|under|below|within|budget|cheapest|lowest|fastest|best|luxury|economy|sleeper|ac|non-ac|morning|evening|for|with)\b|₹|rs\.?|[0-9])",
        re.IGNORECASE,
    )

    def extract_intent(self, text: str, current_phase: int = 1) -> dict[str, Any]:
        updates: dict[str, Any] = {}
        lowered = text.lower()

        if current_phase == 1:
            # 1. Strict Transit Mode Extraction
            if any(w in lowered for w in ["flight", "fly", "plane", "airport"]):
                updates["travel_mode"] = "flight"
            elif any(w in lowered for w in ["train", "rail", "station"]):
                updates["travel_mode"] = "train"
            elif any(w in lowered for w in ["bus", "coach"]):
                updates["travel_mode"] = "bus"
            elif any(w in lowered for w in ["hotel", "stay", "room", "resort"]):
                updates["travel_mode"] = "hotel"

            # 2. Extract Structured Route Locations via Regex
            route = self._route_pattern.search(lowered)
            if route:
                src_valid, src_clean = validate_and_correct_city(route.group(1))
                dest_valid, dest_clean = validate_and_correct_city(route.group(2))
                if src_valid: updates["source"] = src_clean
                if dest_valid: updates["destination"] = dest_clean
            else:
                to_only = self._to_only_pattern.search(lowered)
                if to_only:
                    dest_valid, dest_clean = validate_and_correct_city(to_only.group(1))
                    if dest_valid: updates["destination"] = dest_clean

            # 3. STRICT FILTER: Purge transit keywords falsely flagged as cities
            transit_words = ["flight", "flights", "train", "trains", "bus", "buses", "hotel", "hotels", "ticket", "tickets", "trip", "room", "stay", "travel", "plan", "journey"]
            for key in ["source", "destination"]:
                if updates.get(key) and updates[key].lower() in transit_words:
                    updates[key] = None

            # 4. Date Extraction (Supports Weekdays & Weekends)
            parsed_date = self.parse_relative_date(lowered)
            if parsed_date:
                updates["journey_date"] = parsed_date

            # 5. Budget Extraction (Cleans symbols and commas)
            budget_match = re.search(r"(?:under|below|budget|max|₹|inr|rs\.?)\s*([0-9,]+)", lowered)
            if budget_match:
                updates["budget"] = float(budget_match.group(1).replace(",", ""))

            # 6. Advanced Operational Preference Extraction
            pref_list = []
            if any(w in lowered for w in ["cheap", "lowest", "cheapest", "best"]):
                pref_list.append("lowest_price")
            if any(w in lowered for w in ["fast", "quick", "shortest", "fastest"]):
                pref_list.append("fastest_journey")
            if any(w in lowered for w in ["luxury", "premium", "ac", "sleeper"]):
                pref_list.append("luxury")
                
            if pref_list:
                updates["preferences"] = pref_list

        return updates

    def parse_relative_date(self, text: str) -> str | None:
        """Transforms variable calendar expressions into valid ISO date strings."""
        today = date.today()
        text = text.lower()
        
        if "tomorrow" in text:
            return (today + timedelta(days=1)).isoformat()
        if "today" in text:
            return today.isoformat()
        if "next weekend" in text:
            days_idx = (5 - today.weekday()) % 7 or 7
            return (today + timedelta(days=days_idx + 7)).isoformat()
        if "this weekend" in text:
            days_idx = (5 - today.weekday()) % 7
            return (today + timedelta(days=days_idx)).isoformat()
            
        # Day of week parsing logic (e.g., "next monday", "on Friday")
        weekdays = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6}
        for day, weekday_int in weekdays.items():
            if f"next {day}" in text:
                days_ahead = weekday_int - today.weekday()
                if days_ahead <= 0: days_ahead += 7
                return (today + timedelta(days=days_ahead + 7)).isoformat()
            elif f"this {day}" in text or f"on {day}" in text or day in text:
                days_ahead = weekday_int - today.weekday()
                if days_ahead < 0: days_ahead += 7
                return (today + timedelta(days=days_ahead)).isoformat()
                
        days_match = re.search(r"after\s+(\d+)\s+days?", text)
        if days_match:
            return (today + timedelta(days=int(days_match.group(1)))).isoformat()

        iso_match = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", text)
        if iso_match:
            return iso_match.group(1)
            
        return None

extractor = TravelQueryExtractor()

def extract_travel_intent(state: TravelState) -> dict[str, Any]:
    """LangGraph node targeting inputs and calculating state loop updates."""
    messages = state.get("messages", [])
    phase = state.get("current_phase", 1)
    
    if not messages:
        return {"current_phase": 1, "missing_fields": ["source", "destination", "journey_date", "travel_mode"]}
        
    last_user_msg = messages[-1]["content"].strip()
    
    # 🛑 CRITICAL FIXED LAYER: Wipes persistent checkpointer variables on initialization requests
    if "travel plan" in last_user_msg.lower() or "plan a trip" in last_user_msg.lower():
        return {
            "current_phase": 1,
            "source": None, "destination": None, "journey_date": None, "travel_mode": None, "budget": None,
            "preferences": [], "travel_options": [], "missing_fields": ["source", "destination", "journey_date", "travel_mode"],
            "selected_option_id": None, "generated_otp": None, "otp_verified": False, "active_booking_reference": None,
            "search_error": None
        }

    # Run primary structural parsing
    updates = extractor.extract_intent(last_user_msg, phase)
    merged = {**state, **updates}
    current_mode = merged.get("travel_mode", "")
    
    if current_mode == "hotel":
        merged["source"] = "N/A"
        updates["source"] = "N/A"
    
    if phase == 1:
        required_now = ["destination", "journey_date", "travel_mode"]
        if current_mode != "hotel":
            required_now.append("source")
            
        missing_before = [f for f in required_now if not merged.get(f)]

        # Extract isolated relative dates
        if "journey_date" in missing_before and "journey_date" not in updates:
            loose_date = extractor.parse_relative_date(last_user_msg.lower())
            if loose_date:
                updates["journey_date"] = loose_date
                merged["journey_date"] = loose_date
                missing_before.remove("journey_date")

        # Context-Aware Scanner: Detects what slot the agent requested in the previous message
        assistant_asked_source = False
        assistant_asked_destination = False
        for msg in reversed(messages):
            if msg.get("role") == "assistant":
                content_lower = msg.get("content", "").lower()
                if "source" in content_lower:
                    assistant_asked_source = True
                if "destination" in content_lower:
                    assistant_asked_destination = True
                break

        # Extract loose words and validate them through the city gazetteer database
        text_without_date = last_user_msg
        if "journey_date" in updates:
            text_without_date = re.sub(r'\b(\d{4}-\d{2}-\d{2})\b', '', text_without_date)

        raw_words = re.split(r'[,]+|\s+', text_without_date)
        
        # 💡 THE FIX: Track assigned cities to prevent the "Double-Dip" bug!
        assigned_cities = set()
        if merged.get("source"): assigned_cities.add(merged.get("source"))
        if merged.get("destination"): assigned_cities.add(merged.get("destination"))
        
        for w in raw_words:
            clean_word = re.sub(r'[^a-zA-Z]', '', w).strip()
            if len(clean_word) > 2:
                is_valid, correct_city = validate_and_correct_city(clean_word)
                
                # Ensure we don't map the same city to both Source AND Destination
                if is_valid and correct_city not in assigned_cities:
                    # Map slot dynamically based on conversational context clues
                    if assistant_asked_destination and "destination" in missing_before and not updates.get("destination"):
                        updates["destination"] = correct_city
                        merged["destination"] = correct_city
                        missing_before.remove("destination")
                        assigned_cities.add(correct_city)
                    elif assistant_asked_source and "source" in missing_before and not updates.get("source"):
                        updates["source"] = correct_city
                        merged["source"] = correct_city
                        missing_before.remove("source")
                        assigned_cities.add(correct_city)
                    # Fallback structural sequence handling
                    elif "source" in missing_before and not updates.get("source"):
                        updates["source"] = correct_city
                        merged["source"] = correct_city
                        missing_before.remove("source")
                        assigned_cities.add(correct_city)
                    elif "destination" in missing_before and not updates.get("destination"):
                        updates["destination"] = correct_city
                        merged["destination"] = correct_city
                        missing_before.remove("destination")
                        assigned_cities.add(correct_city)

    # Re-evaluate all remaining parameters
    final_required = ["destination", "journey_date", "travel_mode"]
    if merged.get("travel_mode") != "hotel":
        final_required.append("source")
        
    updates["missing_fields"] = [f for f in final_required if not merged.get(f)]
    
    # Auto-advance orchestrator phases when slots are fully filled
    if phase == 1 and not updates["missing_fields"]:
        updates["current_phase"] = 2
        
    return updates
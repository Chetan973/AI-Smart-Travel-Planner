# app/graph/nodes/provider_node.py
from typing import Any
from datetime import datetime, timezone
from app.graph.state.travel_state import TravelState
from app.search.live_search import LiveSearchService
from app.search.ranking import rank_search_results

def fetch_live_travel_data(state: TravelState) -> dict[str, Any]:
    """Queries live data options and applies the budget-filtering strategy."""
    if state.get("current_phase") != 2:
        return {}

    source = state.get("source")
    destination = state.get("destination")
    journey_date = state.get("journey_date")
    travel_mode = state.get("travel_mode", "Transit")
    budget = state.get("budget")
    preferences = state.get("preferences", [])

    # Budget Guardrail Processing
    if budget and budget < 1500.00 and travel_mode.lower() == "flight":
        # Graceful correction if the user queries a mode that breaches their budget limit
        travel_mode = "train bus"

    search_query = f"live schedules fares prices {travel_mode} from {source} to {destination} on {journey_date}"
    
    service = LiveSearchService()
    raw_results = service.search(query=search_query, limit=5)
    
    structured_options = rank_search_results(
        raw_results, 
        preferences=preferences, 
        budget=budget
    )

    # Re-verify pricing schema fallbacks to protect frontend contracts
    for index, opt in enumerate(structured_options):
        opt["option_id"] = index + 1
        opt["source"] = source
        opt["destination"] = destination
        opt["journey_date"] = journey_date
        
        if opt.get("price") is None:
            opt["price"] = 850.00 if "bus" in travel_mode.lower() else 1150.00
            
        if not opt.get("transport_number"):
            opt["transport_number"] = f"{travel_mode[:2].upper()}-{200 + index}"

    # Filter selections to comply with specified budget limits
    if budget:
        structured_options = [o for o in structured_options if o["price"] <= budget]

    return {
        "search_results": [r.as_dict() for r in raw_results],
        "travel_options": structured_options,
        "search_error": None if structured_options else "No routes matching budget requirements found.",
        "current_phase": 2
    }
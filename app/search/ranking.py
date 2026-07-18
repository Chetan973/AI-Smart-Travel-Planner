# app/search/ranking.py
"""Turn live search snippets into transparent, source-linked comparison cards."""
from __future__ import annotations

import re
from typing import Any
from app.search.live_search import LiveSearchResult

PRICE_PATTERN = re.compile(
    r"(?:₹|INR|Rs\.?|rupees)\s*([0-9,]+(?:\.\d{1,2})?)",
    re.IGNORECASE,
)
DURATION_PATTERN = re.compile(
    r"\b(?:(\d+)\s*(?:h|hr|hrs|hour|hours))?\s*(?:(\d+)\s*(?:m|min|mins|minute|minutes))\b",
    re.IGNORECASE,
)
TIME_PATTERN = re.compile(r"\b([01]?\d|2[0-3]):[0-5]\d\b")

def rank_search_results(
    results: list[LiveSearchResult],
    *,
    preferences: list[str],
    budget: float | None,
) -> list[dict[str, Any]]:
    """Rank only values explicitly present in a live title or snippet."""
    
    # FIX: Pass the budget variable down to the helper function
    options = [_to_option(result, budget) for result in _deduplicate(results)]
    
    options.sort(key=lambda option: _rank_key(option, preferences, budget))
    for index, option in enumerate(options, start=1):
        option["option_id"] = index
    return options

# FIX: Add budget to the function signature
def _to_option(result: LiveSearchResult, budget: float | None) -> dict[str, Any]:
    text = f"{result.title} {result.snippet}"
    price_match = PRICE_PATTERN.search(text)
    price = float(price_match.group(1).replace(",", "")) if price_match else None
    duration = _duration_minutes(text)
    times = TIME_PATTERN.findall(text)
    
    return {
        "option_id": None,
        "provider": result.source,
        "transport_name": result.title,
        "travel_mode": _infer_mode(text),
        "source": None,
        "destination": None,
        "departure_time": times[0] if times else None,
        "arrival_time": times[1] if len(times) > 1 else None,
        "duration_minutes": duration,
        "duration": _format_duration(duration),
        "price": price,
        "currency": "INR" if price is not None else None,
        "availability": _availability(text),
        "booking_url": result.url,
        "source_url": result.url,
        "search_summary": result.snippet,
        "observed_at": result.observed_at,
        "query": result.query,
        "budget_match": None if price is None or budget is None else price <= budget,
    }

def _rank_key(option: dict[str, Any], preferences: list[str], budget: float | None) -> tuple:
    unknown_price = option["price"] is None
    unknown_duration = option["duration_minutes"] is None
    over_budget = bool(budget is not None and option["price"] is not None and option["price"] > budget)
    
    if "fastest_journey" in preferences or "shortest_duration" in preferences:
        return (over_budget, unknown_duration, option["duration_minutes"] or float("inf"), unknown_price, option["price"] or float("inf"))
    if "best_value" in preferences:
        return (over_budget, unknown_price, option["price"] or float("inf"), unknown_duration, option["duration_minutes"] or float("inf"))
        
    # Lowest price is the default because it is the least surprising ordering
    # when no explicit optimisation objective was given.
    return (over_budget, unknown_price, option["price"] or float("inf"), unknown_duration, option["duration_minutes"] or float("inf"))

def _deduplicate(results: list[LiveSearchResult]) -> list[LiveSearchResult]:
    seen: set[str] = set()
    deduplicated: list[LiveSearchResult] = []
    for result in results:
        if result.url not in seen:
            seen.add(result.url)
            deduplicated.append(result)
    return deduplicated

def _duration_minutes(text: str) -> int | None:
    match = DURATION_PATTERN.search(text)
    if not match:
        return None
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    total = hours * 60 + minutes
    return total or None

def _format_duration(total_minutes: int | None) -> str | None:
    if total_minutes is None:
        return None
    hours, minutes = divmod(total_minutes, 60)
    return f"{hours}h {minutes}m" if hours else f"{minutes}m"

def _availability(text: str) -> str | None:
    lowered = text.lower()
    if "sold out" in lowered or "unavailable" in lowered:
        return "Unavailable (as stated in the live result)"
    if "available" in lowered:
        return "Availability mentioned in the live result; verify with provider"
    return None

def _infer_mode(text: str) -> str | None:
    lowered = text.lower()
    for word, mode in (("flight", "flight"), ("airline", "flight"), ("train", "train"), ("bus", "bus"), ("hotel", "hotel"), ("attraction", "tourist_place")):
        if word in lowered:
            return mode
    return None
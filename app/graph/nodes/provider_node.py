from concurrent.futures import ThreadPoolExecutor

from app.enums.travel_mode import TravelMode
from app.graph.state.travel_state import TravelState
from app.memory.travel_memory import TravelMemory
from app.providers.provider_factory import ProviderFactory


class ProviderNode:
    """Runs the independent mock providers concurrently and ranks their options."""

    @staticmethod
    def search(state: TravelState) -> dict:
        modes = (TravelMode.TRAIN, TravelMode.FLIGHT, TravelMode.BUS)

        def search_mode(mode: TravelMode):
            return ProviderFactory.get_provider(mode).search(state.source, state.destination, str(state.journey_date))

        with ThreadPoolExecutor(max_workers=len(modes)) as executor:
            results = list(executor.map(search_mode, modes))

        options = []
        for group in results:
            for option in group:
                options.append(option.model_dump())
        options = ProviderNode._rank(options, state.budget, state.travel_preference)
        for index, option in enumerate(options, start=1):
            option["option_id"] = index

        recommended = options[0] if options else None
        state.travel_options = options
        state.provider = recommended["provider"] if recommended else None
        state.recommended_option_id = recommended["option_id"] if recommended else None
        TravelMemory.save(state)
        return {"provider": state.provider, "travel_options": options, "recommended_option_id": state.recommended_option_id}

    @staticmethod
    def _rank(options: list[dict], budget: float | None, preference: str | None) -> list[dict]:
        def duration_minutes(value: str) -> int:
            hours, minutes = 0, 0
            for part in value.lower().replace("h", " h ").replace("m", " m ").split():
                if part.isdigit():
                    if "h" in value.lower()[value.lower().find(part) + len(part):]:
                        hours = int(part)
                    else:
                        minutes = int(part)
            return hours * 60 + minutes

        def key(option: dict):
            price = float(option["price"])
            within_budget = budget is None or price <= budget
            duration = duration_minutes(option["duration"])
            preference_key = duration if preference == "FASTEST" else price
            return (not within_budget, preference_key, price, duration)

        return sorted(options, key=key)

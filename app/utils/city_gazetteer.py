# app/utils/city_gazetteer.py
import difflib

# A curated list of major cities and tourist destinations (expandable)
VALID_CITIES = {
    "bengaluru": "Bangalore",
    "bangalore": "Bangalore",
    "delhi": "Delhi",
    "new delhi": "Delhi",
    "mumbai": "Mumbai",
    "bombay": "Mumbai",
    "pune": "Pune",
    "chennai": "Chennai",
    "madras": "Chennai",
    "kolkata": "Kolkata",
    "calcutta": "Kolkata",
    "hyderabad": "Hyderabad",
    "goa": "Goa",
    "jaipur": "Jaipur",
    "agra": "Agra",
    "kochi": "Kochi",
    "cochin": "Kochi",
    "mysore": "Mysuru",
    "mysuru": "Mysuru",
    "mangalore": "Mangaluru",
    "mangaluru": "Mangaluru",
    "huvina hadagali": "Huvina Hadagali",
    "hadagali": "Huvina Hadagali",
    "hubli": "Hubballi",
    "hubballi": "Hubballi",
    "dharwad": "Dharwad",
    "chennai": "Chennai"
}

def validate_and_correct_city(input_name: str) -> tuple[bool, str]:
    """
    Validates a city name, handles spell correction, and filters gibberish.
    Returns:
        (is_valid: bool, corrected_name: str)
    """
    if not input_name or not isinstance(input_name, str):
        return False, ""

    cleaned = input_name.strip().lower()
    
    # 1. Direct match check
    if cleaned in VALID_CITIES:
        return True, VALID_CITIES[cleaned]
    
    # 2. Spelling distance/similarity check (auto-correct matches >= 70% similarity)
    matches = difflib.get_close_matches(cleaned, VALID_CITIES.keys(), n=1, cutoff=0.7)
    if matches:
        best_match = matches[0]
        return True, VALID_CITIES[best_match]
    
    # 3. Reject as gibberish if no close match is found
    return False, ""
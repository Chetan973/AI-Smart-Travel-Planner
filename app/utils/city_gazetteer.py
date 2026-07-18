# app/utils/city_gazetteer.py
import difflib

# A curated list of major cities, states, and tourist destinations
VALID_CITIES = {
    # ==========================================
    # CORE METROS & PREVIOUSLY ADDED
    # ==========================================
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

    # ==========================================
    # ALL INDIAN STATES & UNION TERRITORIES
    # ==========================================
    "andhra pradesh": "Andhra Pradesh",
    "arunachal pradesh": "Arunachal Pradesh",
    "assam": "Assam",
    "bihar": "Bihar",
    "chhattisgarh": "Chhattisgarh",
    "gujarat": "Gujarat",
    "haryana": "Haryana",
    "himachal pradesh": "Himachal Pradesh",
    "jharkhand": "Jharkhand",
    "karnataka": "Karnataka",
    "kerala": "Kerala",
    "madhya pradesh": "Madhya Pradesh",
    "maharashtra": "Maharashtra",
    "manipur": "Manipur",
    "meghalaya": "Meghalaya",
    "mizoram": "Mizoram",
    "nagaland": "Nagaland",
    "odisha": "Odisha",
    "orissa": "Odisha",
    "punjab": "Punjab",
    "rajasthan": "Rajasthan",
    "sikkim": "Sikkim",
    "tamil nadu": "Tamil Nadu",
    "telangana": "Telangana",
    "tripura": "Tripura",
    "uttar pradesh": "Uttar Pradesh",
    "uttarakhand": "Uttarakhand",
    "west bengal": "West Bengal",
    "andaman and nicobar": "Andaman and Nicobar Islands",
    "chandigarh": "Chandigarh",
    "dadra and nagar haveli": "Dadra and Nagar Haveli",
    "daman and diu": "Daman and Diu",
    "lakshadweep": "Lakshadweep",
    "puducherry": "Puducherry",
    "pondicherry": "Puducherry",
    "ladakh": "Ladakh",
    "jammu and kashmir": "Jammu and Kashmir",
    "jammu": "Jammu",
    "kashmir": "Kashmir",

    # ==========================================
    # KARNATAKA DISTRICTS & MAJOR CITIES
    # ==========================================
    "mysore": "Mysuru",
    "mysuru": "Mysuru",
    "mangalore": "Mangaluru",
    "mangaluru": "Mangaluru",
    "huvina hadagali": "Huvina Hadagali",
    "hadagali": "Huvina Hadagali",
    "hubli": "Hubballi",
    "hubballi": "Hubballi",
    "dharwad": "Dharwad",
    "hospet": "Hospet",
    "hosapete": "Hospet",
    "shivamogga": "Shivamogga",
    "shimoga": "Shivamogga",
    "kolar": "Kolar",
    "belagavi": "Belagavi",
    "belgaum": "Belagavi",
    "kalaburagi": "Kalaburagi",
    "gulbarga": "Kalaburagi",
    "ballari": "Ballari",
    "bellary": "Ballari",
    "vijayapura": "Vijayapura",
    "bijapur": "Vijayapura",
    "raichur": "Raichur",
    "bidar": "Bidar",
    "gadag": "Gadag",
    "hassan": "Hassan",
    "udupi": "Udupi",
    "chitradurga": "Chitradurga",
    "tumakuru": "Tumakuru",
    "tumkur": "Tumakuru",
    "mandya": "Mandya",
    "davanagere": "Davanagere",
    "davangere": "Davanagere",
    "karwar": "Karwar",
    "gokarna": "Gokarna",
    "murdeshwar": "Murdeshwar",
    "chikkamagaluru": "Chikkamagaluru",
    "chikmagalur": "Chikkamagaluru",
    "madikeri": "Madikeri",
    "kodagu": "Kodagu",
    "coorg": "Kodagu",
    "bagalkot": "Bagalkot",
    "koppal": "Koppal",
    "haveri": "Haveri",
    "yadgir": "Yadgir",
    "chamarajanagar": "Chamarajanagar",
    "ramanagara": "Ramanagara",
    "chikkaballapur": "Chikkaballapur",
    "sirsi": "Sirsi",
    "dandeli": "Dandeli",
    "bhatkal": "Bhatkal",
    "puttur": "Puttur",
    "kundapura": "Kundapura",
    "nanjangud": "Nanjangud",
    "bhadravati": "Bhadravati",
    "sindhanur": "Sindhanur"
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
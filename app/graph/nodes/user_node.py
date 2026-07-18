# app/graph/nodes/user_node.py
from app.graph.state.travel_state import TravelState

def ask_missing_info(state: TravelState) -> dict:
    """Follow-up node used only when a mandatory travel field is absent."""
    missing = state.get("missing_fields", [])
    validation_error = state.get("validation_error")
    
    if validation_error:
        message = validation_error
        
    # 💡 NEW: Handle generic introductions (e.g. "I have a travel plan", "Hi")
    elif len(missing) >= 4:
        message = "✨ **AI Smart Travel Planner**\n\nAwesome! What's your plan? Where would you like to travel, and when are you planning to go?\n*(e.g., 'I want to go from Bangalore to Mangalore tomorrow with the lowest price under ₹1500')*"
        
    elif "travel_mode" in missing:
        message = "Would you like to check options for a **Bus, Train, Flight, or Hotel**?"
        
    elif len(missing) == 1:
        message = f"Please tell me the {missing[0].replace('_', ' ').title()}."
        
    elif missing:
        readable = ", ".join(field.replace("_", " ").title() for field in missing)
        message = f"To search live options, I need a bit more info. Could you please provide your: **{readable}**?"
        
    else:
        message = "I need some more details to proceed."
        
    return {"messages": [{"role": "assistant", "content": message}]}
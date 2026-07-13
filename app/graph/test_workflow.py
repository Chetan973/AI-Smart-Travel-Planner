from datetime import date

from app.enums.travel_mode import TravelMode
from app.graph.state.travel_state import TravelState
from app.graph.workflow import travel_graph

# =====================================================
# Initial State
# =====================================================

state = TravelState(

    session_id="travel-session-001",

    user_id=1,

    full_name="Chetan",

    email="chetan@gmail.com",

    mobile_no="9876543210",

    source="Bangalore",

    destination="Shimoga",

    journey_date=date(2026, 7, 15),

    travel_mode=TravelMode.TRAIN,

    passengers=2

)

# =====================================================
# LangGraph Config
# =====================================================

config = {

    "configurable": {

        "thread_id": state.session_id

    }

}

# =====================================================
# Execute Graph
# =====================================================

result = travel_graph.invoke(

    state,

    config=config

)

# =====================================================
# Convert Dict -> TravelState
# =====================================================

result = TravelState.model_validate(result)

# =====================================================
# Output
# =====================================================

print()

print("=" * 60)
print("AI Recommendation")
print("=" * 60)

print(result.ai_response)

print()

print("=" * 60)
print("Provider")
print("=" * 60)

print(result.provider)

print()

print("=" * 60)
print("Travel Options")
print("=" * 60)

for option in result.travel_options:

    print(option)

print()

print("=" * 60)
print("Workflow Completed")
print("=" * 60)
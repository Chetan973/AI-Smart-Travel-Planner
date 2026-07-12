from app.enums import TravelMode
from app.graph.workflow import travel_graph
from app.state.travel_state import TravelState

state = TravelState(
    full_name="Chetan",
    email="chetan@gmail.com",
    mobile_no="9876543210",
    source="Bangalore",
    destination="Shimoga",
    travel_mode=TravelMode.TRAIN,
)

result = travel_graph.invoke(state)

print(result.model_dump())
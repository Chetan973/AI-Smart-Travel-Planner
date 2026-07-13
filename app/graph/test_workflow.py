from app.enums.travel_mode import TravelMode
from app.graph.state.travel_state import TravelState
from app.graph.workflow import travel_graph


def test():

    state = TravelState(

        user_id=1,

        full_name="Chetan",

        email="chetan@gmail.com",

        source="Bangalore",

        destination="Shimoga",

        travel_mode=TravelMode.TRAIN,

        passengers=2

    )

    result = travel_graph.invoke(
        state,
        config={
            "configurable": {
                "thread_id": "travel-session-001"
            }
        }
    )

    print()

    print("=" * 60)

    print(result)

    print("=" * 60)


if __name__ == "__main__":
    test()
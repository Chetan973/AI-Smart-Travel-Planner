from fastapi import APIRouter

from app.graph.travel_graph import travel_graph

router = APIRouter()


@router.get("/graph")

def run_graph():

    result = travel_graph.invoke(
        {
            "full_name": "Chetan",
            "email": "abc@gmail.com",
            "source": "Bangalore",
            "destination": "Shimoga",
            "travel_mode": "Train",
        }
    )

    return result
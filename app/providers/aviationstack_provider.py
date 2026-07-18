import requests

from app.config import settings


class AviationStackProvider:

    BASE_URL = "http://api.aviationstack.com/v1"

    def future_flights(
        self,
        departure_iata: str,
        arrival_iata: str,
        flight_date: str,
    ):

        response = requests.get(
            f"{self.BASE_URL}/flightsFuture",
            params={
                "access_key": settings.AVIATIONSTACK_API_KEY,
                "dep_iata": departure_iata,
                "arr_iata": arrival_iata,
                "flight_date": flight_date,
            },
            timeout=20,
        )

        response.raise_for_status()

        return response.json().get("data", [])
# streamlit-ui/services/api_client.py
import requests

BASE_URL = "http://127.0.0.1:8000"


class ChatAPI:
    @staticmethod
    def message(session_id: str, message: str):
        response = requests.post(
            f"{BASE_URL}/api/chat/message",
            json={"session_id": session_id, "message": message},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()


class TravelAPI:

    @staticmethod
    def search(data: dict):

        response = requests.post(
            f"{BASE_URL}/api/travel/search",
            json=data
        )

        response.raise_for_status()

        return response.json()


class BookingAPI:

    @staticmethod
    def create(data: dict):

        response = requests.post(
            f"{BASE_URL}/api/bookings/create",
            json=data
        )

        response.raise_for_status()

        return response.json()

    @staticmethod
    def history(user_id: int):

        response = requests.get(
            f"{BASE_URL}/api/bookings/user/{user_id}"
        )

        response.raise_for_status()

        return response.json()


class PaymentAPI:

    @staticmethod
    def status(booking_reference: str):

        response = requests.get(
            f"{BASE_URL}/api/payments/status/{booking_reference}",
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def create_order(booking_reference: str):

        response = requests.post(
            f"{BASE_URL}/api/payments/create-order",
            json={
                "booking_reference": booking_reference
            }
        )

        response.raise_for_status()

        return response.json()

    @staticmethod
    def verify(data: dict):

        response = requests.post(
            f"{BASE_URL}/api/payments/verify",
            json=data
        )

        response.raise_for_status()

        return response.json()

    @staticmethod
    def checkout_url(booking_reference: str):

        return (
            f"{BASE_URL}/checkout"
            f"?booking_reference={booking_reference}"
        )

    @staticmethod
    def demo_bypass(data: dict):
        """Hits the backend demo-bypass route to skip Razorpay during presentations."""
        response = requests.post(
            f"{BASE_URL}/api/payments/demo-bypass",
            json=data,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

class OTPAPI:

    @staticmethod
    def initialize_user(data: dict):

        response = requests.post(
            f"{BASE_URL}/api/users/init",
            json=data,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    @staticmethod
    def verify(email: str, otp: str):

        response = requests.post(
            f"{BASE_URL}/api/users/verify-otp",
            json={"email": email, "otp": otp},
            timeout=30,
        )

        response.raise_for_status()

        return response.json()
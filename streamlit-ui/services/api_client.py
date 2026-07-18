# streamlit-ui/services/api_client.py
import requests
import streamlit as st

# (Keep your existing base URL configuration)
BASE_URL = "http://127.0.0.1:8000/api"
ROOT_URL = "http://127.0.0.1:8000"

class APIClient:
    
    @staticmethod
    def send_chat_message(session_id: str, message: str) -> dict:
        url = "http://127.0.0.1:8000/api/chat/message"
        
        payload = {
            "session_id": session_id, 
            "message": message
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code != 200:
                raise Exception(f"FastAPI Validation Error: {response.text}")
                
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network failure: {str(e)}")

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
            f"{ROOT_URL}/checkout"
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

    @staticmethod
    def configuration() -> dict:
        response = requests.get(f"{BASE_URL}/payments/configuration", timeout=15)
        response.raise_for_status()
        return response.json()

from datetime import datetime

from sqlalchemy.orm import Session

from app.api.booking_schemas import (
    BookingResponse,
    CreateBookingRequest,
)
from app.enums.booking_status import BookingStatus
from app.memory.travel_memory import TravelMemory
from app.models.booking import Booking
from app.repository.booking_repository import BookingRepository


class BookingService:

    @staticmethod
    def create_booking(
        db: Session,
        request: CreateBookingRequest
    ) -> BookingResponse:

        # -----------------------------
        # Load Travel Session from Redis
        # -----------------------------
        state = TravelMemory.load(
            request.session_id
        )

        if state is None:
            raise ValueError(
                "Travel session expired or not found."
            )

        # -----------------------------
        # Find Selected Travel Option
        # -----------------------------
        selected_option = None

        for option in state.travel_options:

            if option["option_id"] == request.option_id:

                selected_option = option

                break

        if selected_option is None:

            raise ValueError(
                "Travel option not found."
            )

        # -----------------------------
        # Calculate Amount
        # -----------------------------
        total_amount = (
            float(selected_option["price"])
            * request.passengers
        )

        # -----------------------------
        # Create Booking
        # -----------------------------
        booking = Booking(

            user_id=request.user_id,

            provider=selected_option["provider"],

            travel_mode=selected_option["travel_mode"],

            transport_name=selected_option["transport_name"],

            transport_number=selected_option["transport_number"],

            source=selected_option["source"],

            destination=selected_option["destination"],

            journey_date=state.journey_date,

            departure_time=selected_option["departure_time"],

            arrival_time=selected_option["arrival_time"],

            passengers=request.passengers,

            total_amount=total_amount,

            booking_status=BookingStatus.PENDING,

            payment_completed=False

        )

        booking = BookingRepository.save(
            db,
            booking
        )

        # -----------------------------
        # Booking Reference
        # -----------------------------
        booking.booking_reference = (
            f"BK-{datetime.now():%Y%m%d}-{booking.booking_id:06d}"
        )

        booking = BookingRepository.update(
            db,
            booking
        )

        # -----------------------------
        # Response
        # -----------------------------
        return BookingResponse(

            booking_reference=booking.booking_reference,

            booking_status=booking.booking_status,

            provider=booking.provider,

            transport_name=booking.transport_name,

            source=booking.source,

            destination=booking.destination,

            journey_date=booking.journey_date,

            departure_time=booking.departure_time,

            arrival_time=booking.arrival_time,

            passengers=booking.passengers,

            total_amount=float(booking.total_amount),

            payment_completed=booking.payment_completed,

            message="Booking created successfully."

        )
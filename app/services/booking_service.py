# app/services/booking_service.py
from datetime import datetime
from sqlalchemy.orm import Session

from app.api.booking_schemas import (
    BookingHistoryResponse,
    BookingResponse,
    CreateBookingRequest,
)
from app.enums.booking_status import BookingStatus
from app.memory.travel_memory import TravelMemory
from app.models.booking import Booking
from app.repository.booking_repository import BookingRepository
from app.repository.user_repository import UserRepository


class BookingService:

    @staticmethod
    def create_booking(
        db: Session,
        request: CreateBookingRequest
    ) -> BookingResponse:

        # -----------------------------
        # 1. Load Travel Session from Redis
        # -----------------------------
        state = TravelMemory.load(request.session_id)
        if state is None:
            raise ValueError("Travel session expired or not found.")

        # -----------------------------
        # 2. STRICT LOCK: Check OTP Verification
        # -----------------------------
        user = UserRepository.find_by_id(db, request.user_id)
        if not user:
            raise ValueError("User not found.")

        # Ensure that the user's email has been verified via OTP
        if not user.email_verified:
            raise ValueError(
                "Booking rejected. Email verification with OTP must be completed first."
            )

        # -----------------------------
        # 3. Find Selected Travel Option
        # -----------------------------
        selected_option = None
        for option in state.travel_options:
            if option["option_id"] == request.option_id:
                selected_option = option
                break

        if selected_option is None:
            raise ValueError("Travel option not found.")

        # -----------------------------
        # 4. Calculate Amount
        # -----------------------------
        total_amount = float(selected_option["price"]) * request.passengers

        # -----------------------------
        # 5. Create Booking
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

        booking = BookingRepository.save(db, booking)

        # -----------------------------
        # 6. Booking Reference Assignment
        # -----------------------------
        booking.booking_reference = (
            f"BK-{datetime.now():%Y%m%d}-{booking.booking_id:06d}"
        )
        booking = BookingRepository.update(db, booking)

        # -----------------------------
        # 7. Response
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

    @staticmethod
    def get_user_bookings(
        db: Session,
        user_id: int
    ) -> list[BookingHistoryResponse]:

        bookings = BookingRepository.find_by_user(db, user_id)

        return [
            BookingHistoryResponse(
                booking_id=b.booking_id,
                booking_reference=b.booking_reference,
                provider=b.provider,
                travel_mode=b.travel_mode,
                transport_name=b.transport_name,
                transport_number=b.transport_number,
                source=b.source,
                destination=b.destination,
                journey_date=b.journey_date,
                departure_time=b.departure_time,
                arrival_time=b.arrival_time,
                passengers=b.passengers,
                total_amount=float(b.total_amount),
                booking_status=b.booking_status,
                payment_completed=b.payment_completed
            )
            for b in bookings
        ]
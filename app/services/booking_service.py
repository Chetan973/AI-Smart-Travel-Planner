# app/services/booking_service.py
from sqlalchemy.orm import Session
from app.api.booking_schemas import BookingHistoryResponse
from app.repository.booking_repository import BookingRepository

class BookingService:
    @staticmethod
    def get_user_bookings(
        db: Session,
        user_id: int
    ) -> list[BookingHistoryResponse]:
        """Fetches booking history for the user."""
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
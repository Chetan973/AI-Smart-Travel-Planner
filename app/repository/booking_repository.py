from sqlalchemy.orm import Session

from app.models.booking import Booking


class BookingRepository:
    """
    Repository for Booking operations.
    """

    @staticmethod
    def save(
        db: Session,
        booking: Booking
    ) -> Booking:

        db.add(booking)

        db.commit()

        db.refresh(booking)

        return booking

    @staticmethod
    def find_by_booking_id(
        db: Session,
        booking_id: int
    ) -> Booking | None:

        return (
            db.query(Booking)
            .filter(
                Booking.booking_id == booking_id
            )
            .first()
        )

    @staticmethod
    def find_by_booking_reference(
        db: Session,
        booking_reference: str
    ) -> Booking | None:

        return (
            db.query(Booking)
            .filter(
                Booking.booking_reference == booking_reference
            )
            .first()
        )

    @staticmethod
    def find_by_user(
        db: Session,
        user_id: int
    ) -> list[Booking]:

        return (
            db.query(Booking)
            .filter(
                Booking.user_id == user_id
            )
            .order_by(
                Booking.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        booking: Booking
    ) -> Booking:

        db.commit()

        db.refresh(booking)

        return booking

    @staticmethod
    def delete(
        db: Session,
        booking: Booking
    ) -> None:

        db.delete(booking)

        db.commit()

    # @staticmethod
    # def find_by_reference(
    #     db: Session,
    #     booking_reference: str
    # ) -> Booking | None:

    #     return (
    #         db.query(Booking)
    #         .filter(
    #             Booking.booking_reference == booking_reference
    #         )
    #         .first()
    #     )
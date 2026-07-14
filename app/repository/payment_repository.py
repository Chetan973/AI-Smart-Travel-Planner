from sqlalchemy.orm import Session

from app.models.payment import Payment


class PaymentRepository:

    @staticmethod
    def save(
        db: Session,
        payment: Payment
    ) -> Payment:

        db.add(payment)

        db.commit()

        db.refresh(payment)

        return payment

    @staticmethod
    def update(
        db: Session,
        payment: Payment
    ) -> Payment:

        db.commit()

        db.refresh(payment)

        return payment

    @staticmethod
    def find_by_payment_id(
        db: Session,
        payment_id: int
    ) -> Payment | None:

        return (
            db.query(Payment)
            .filter(
                Payment.payment_id == payment_id
            )
            .first()
        )

    @staticmethod
    def find_by_booking_id(
        db: Session,
        booking_id: int
    ) -> Payment | None:

        return (
            db.query(Payment)
            .filter(
                Payment.booking_id == booking_id
            )
            .first()
        )

    @staticmethod
    def find_by_order_id(
        db: Session,
        razorpay_order_id: str
    ) -> Payment | None:

        return (
            db.query(Payment)
            .filter(
                Payment.razorpay_order_id == razorpay_order_id
            )
            .first()
        )

    @staticmethod
    def find_by_payment_gateway_id(
        db: Session,
        razorpay_payment_id: str
    ) -> Payment | None:

        return (
            db.query(Payment)
            .filter(
                Payment.razorpay_payment_id == razorpay_payment_id
            )
            .first()
        )
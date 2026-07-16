# app/services/payment_service.py
import os
import traceback
from sqlalchemy.orm import Session
import razorpay

from app.api.payment_schemas import (
    CreatePaymentOrderRequest,
    CreatePaymentOrderResponse,
    VerifyPaymentRequest,
    VerifyPaymentResponse,
)
from app.enums.booking_status import BookingStatus
from razorpay.errors import SignatureVerificationError
from app.config import settings
from app.models.payment import Payment
from app.repository.booking_repository import BookingRepository
from app.repository.payment_repository import PaymentRepository
from app.repository.user_repository import UserRepository
from app.services.email_service import EmailService


class PaymentService:

    @staticmethod
    def get_status(db: Session, booking_reference: str) -> VerifyPaymentResponse:
        booking = BookingRepository.find_by_booking_reference(db, booking_reference)
        if booking is None:
            raise ValueError("Booking not found.")
        payment = PaymentRepository.find_by_booking_id(db, booking.booking_id)
        status = payment.payment_status if payment else "pending"
        return VerifyPaymentResponse(
            booking_reference=booking_reference,
            payment_status=status,
            message=f"Payment status: {status}",
        )

    @staticmethod
    def create_order(
        db: Session,
        request: CreatePaymentOrderRequest
    ) -> CreatePaymentOrderResponse:

        booking = BookingRepository.find_by_booking_reference(db, request.booking_reference)
        if booking is None:
            raise ValueError("Booking not found.")

        existing_payment = PaymentRepository.find_by_booking_id(db, booking.booking_id)
        if existing_payment is not None and existing_payment.payment_completed:
            raise ValueError("Booking already paid.")

        client = razorpay.Client(
            auth=(settings.razorpay_key_id, settings.razorpay_key_secret)
        )

        amount_in_paise = int(float(booking.total_amount) * 100)

        razorpay_order = client.order.create({
            "amount": amount_in_paise,
            "currency": "INR",
            "receipt": booking.booking_reference,
            "payment_capture": 1
        })

        payment = Payment(
            booking_id=booking.booking_id,
            amount=booking.total_amount,
            currency=razorpay_order["currency"],
            razorpay_order_id=razorpay_order["id"],
            payment_status=razorpay_order["status"],
            payment_completed=False
        )  
        payment = PaymentRepository.save(db, payment)

        try:
            # Safely pass all possible required fields including payment_reference
            return CreatePaymentOrderResponse(
                booking_reference=booking.booking_reference,
                payment_reference=payment.razorpay_order_id,  # <-- Added to satisfy Pydantic Schema!
                razorpay_order_id=payment.razorpay_order_id,
                amount=float(payment.amount),
                currency=payment.currency,
                razorpay_key=settings.razorpay_key_id,
                razorpay_key_id=settings.razorpay_key_id,
                payment_status=payment.payment_status,
                message="Payment order created successfully."
            )
        except Exception as e:
            print("="*80)
            print("🚨 SCHEMA VALIDATION ERROR IN CREATE_ORDER 🚨")
            traceback.print_exc()
            print("="*80)
            raise ValueError(f"Schema mismatch: {str(e)}")
    
    @staticmethod
    def verify_payment(
        db: Session,
        request: VerifyPaymentRequest
    ) -> VerifyPaymentResponse:

        payment = PaymentRepository.find_by_order_id(db, request.razorpay_order_id)
        if payment is None:
            raise ValueError("Payment not found.")

        client = razorpay.Client(
            auth=(settings.razorpay_key_id, settings.razorpay_key_secret)
        )

        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": request.razorpay_order_id,
                "razorpay_payment_id": request.razorpay_payment_id,
                "razorpay_signature": request.razorpay_signature
            })
        except SignatureVerificationError:
            payment.payment_status = "signature_verification_failed"
            payment.payment_completed = False
            PaymentRepository.update(db, payment)
            raise ValueError("Payment signature verification failed.")

        razorpay_payment = client.payment.fetch(request.razorpay_payment_id)

        payment.razorpay_payment_id = razorpay_payment["id"]
        payment.razorpay_signature = request.razorpay_signature
        payment_status = razorpay_payment.get("status", "").lower()
        payment.payment_status = payment_status
        payment.payment_completed = (payment_status == "captured")

        PaymentRepository.update(db, payment)

        booking = BookingRepository.find_by_booking_id(db, payment.booking_id)

        if payment_status == "captured":
            booking.booking_status = BookingStatus.CONFIRMED
            booking.payment_completed = True
            BookingRepository.update(db, booking)

            # --- SEND EMAIL TICKET ON SUCCESS ---
            PaymentService._trigger_confirmation_email(db, booking)
        else:
            booking.payment_completed = False
            BookingRepository.update(db, booking)

        return VerifyPaymentResponse(
            booking_reference=request.booking_reference,
            payment_status=payment.payment_status,
            message=f"Payment status : {payment.payment_status}"
        )

    @staticmethod
    def process_demo_bypass(db: Session, booking_reference: str) -> dict:
        """
        Bypasses the Razorpay gateway and forces payment status to SUCCESS for demonstration purposes.
        """
        demo_mode_enabled = os.getenv("DEMO_MODE_ENABLED", "True").lower() == "true"

        if not demo_mode_enabled:
            raise ValueError("Demo mode is disabled. Please complete standard Razorpay payment.")

        booking = BookingRepository.find_by_booking_reference(db, booking_reference)
        if booking is None:
            raise ValueError("Booking not found.")

        booking.booking_status = BookingStatus.CONFIRMED
        booking.payment_completed = True
        BookingRepository.update(db, booking)

        payment = PaymentRepository.find_by_booking_id(db, booking.booking_id)
        if payment:
            payment.payment_status = "captured"
            payment.payment_completed = True
            payment.razorpay_payment_id = f"demo_pay_{booking.booking_id}"
            PaymentRepository.update(db, payment)
        else:
            payment = Payment(
                booking_id=booking.booking_id,
                amount=booking.total_amount,
                currency="INR",
                razorpay_order_id=f"demo_order_{booking.booking_id}",
                payment_status="captured",
                payment_completed=True
            )
            PaymentRepository.save(db, payment)

        # --- SEND EMAIL TICKET ON DEMO SUCCESS ---
        PaymentService._trigger_confirmation_email(db, booking)

        return {
            "status": "SUCCESS",
            "message": "Payment skipped successfully under Demo Mode. Ticket issued.",
            "booking_reference": booking.booking_reference
        }

    @staticmethod
    def _trigger_confirmation_email(db: Session, booking):
        """Helper method to map booking details and trigger the EmailService."""
        try:
            user = UserRepository.find_by_id(db, booking.user_id)
            if user and user.email:
                booking_dict = {
                    "booking_reference": booking.booking_reference,
                    "transport_name": booking.transport_name,
                    "transport_number": booking.transport_number,
                    "source": booking.source,
                    "destination": booking.destination,
                    "journey_date": booking.journey_date,
                    "departure_time": booking.departure_time,
                    "arrival_time": booking.arrival_time,
                    "passengers": booking.passengers,
                    "total_amount": float(booking.total_amount)
                }
                EmailService.send_booking_confirmation(user.email, booking_dict)
        except Exception as e:
            print(f"Silent Failure: Could not trigger confirmation email: {e}")
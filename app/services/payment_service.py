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


class PaymentService:

    @staticmethod
    def create_order(
        db: Session,
        request: CreatePaymentOrderRequest
    ) -> CreatePaymentOrderResponse:

        # -----------------------------------------
        # Find Booking
        # -----------------------------------------

        booking = BookingRepository.find_by_booking_reference(
            db,
            request.booking_reference
        )

        if booking is None:
            raise ValueError(
                "Booking not found."
            )

        # -----------------------------------------
        # Prevent duplicate payment
        # -----------------------------------------

        existing_payment = PaymentRepository.find_by_booking_id(
            db,
            booking.booking_id
        )

        if (
            existing_payment is not None
            and existing_payment.payment_completed
        ):
            raise ValueError(
                "Booking already paid."
            )

        # -----------------------------------------
        # Razorpay Client
        # -----------------------------------------

        client = razorpay.Client(
            auth=(
                settings.razorpay_key_id,
                settings.razorpay_key_secret
            )
        )

        # -----------------------------------------
        # Create Razorpay Order
        # -----------------------------------------

        amount_in_paise = int(
            float(booking.total_amount) * 100
        )

        razorpay_order = client.order.create({

            "amount": amount_in_paise,

            "currency": "INR",

            "receipt": booking.booking_reference,

            "payment_capture": 1

        })

        # -----------------------------------------
        # Payment Entity
        # -----------------------------------------

        payment = Payment(

            booking_id=booking.booking_id,

            amount=booking.total_amount,

            currency=razorpay_order["currency"],

            razorpay_order_id=razorpay_order["id"],

            payment_status=razorpay_order["status"],

            payment_completed=False

        )  

        payment = PaymentRepository.save(
            db,
            payment
        )

        # -----------------------------------------
        # Response
        # -----------------------------------------

        return CreatePaymentOrderResponse(

            booking_reference=booking.booking_reference,

            razorpay_order_id=payment.razorpay_order_id,

            amount=float(payment.amount),

            currency=payment.currency,

            razorpay_key=settings.razorpay_key_id,

            payment_status=payment.payment_status

        )
    
    @staticmethod
    def verify_payment(
        db: Session,
        request: VerifyPaymentRequest
    ) -> VerifyPaymentResponse:

        # -----------------------------------------
        # Find Payment
        # -----------------------------------------

        payment = PaymentRepository.find_by_order_id(
            db,
            request.razorpay_order_id
        )

        if payment is None:
            raise ValueError("Payment not found.")

        client = razorpay.Client(
            auth=(
                settings.razorpay_key_id,
                settings.razorpay_key_secret
            )
        )

        # -----------------------------------------
        # Verify Signature
        # -----------------------------------------

        try:

            client.utility.verify_payment_signature({

                "razorpay_order_id": request.razorpay_order_id,

                "razorpay_payment_id": request.razorpay_payment_id,

                "razorpay_signature": request.razorpay_signature

            })

        except SignatureVerificationError:

            payment.payment_status = "signature_verification_failed"

            payment.payment_completed = False

            PaymentRepository.update(
                db,
                payment
            )

            raise ValueError("Payment signature verification failed.")

        # -----------------------------------------
        # Fetch Actual Razorpay Payment
        # -----------------------------------------

        razorpay_payment = client.payment.fetch(
            request.razorpay_payment_id
        )

        # -----------------------------------------
        # Update Payment
        # -----------------------------------------

        payment.razorpay_payment_id = razorpay_payment["id"]

        payment.razorpay_signature = request.razorpay_signature

        payment_status = razorpay_payment.get("status", "").lower()

        payment.payment_status = payment_status

        payment.payment_completed = (
            razorpay_payment["status"] == "captured"
        )

        PaymentRepository.update(
            db,
            payment
        )

        # -----------------------------------------
        # Update Booking
        # -----------------------------------------

        booking = BookingRepository.find_by_booking_id(
            db,
            payment.booking_id
        )

        if payment_status == "captured":

            booking.booking_status = BookingStatus.CONFIRMED

            booking.payment_completed = True

        else:

            booking.payment_completed = False

        BookingRepository.update(
            db,
            booking
        )

        # -----------------------------------------
        # Response
        # -----------------------------------------

        return VerifyPaymentResponse(

            booking_reference=request.booking_reference,

            payment_status=payment.payment_status,

            message=f"Payment status : {payment.payment_status}"

        )
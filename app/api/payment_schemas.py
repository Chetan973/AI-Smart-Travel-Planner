from pydantic import BaseModel

from app.enums.payment_status import PaymentStatus


class CreatePaymentOrderRequest(BaseModel):

    booking_reference: str


class CreatePaymentOrderResponse(BaseModel):

    booking_reference: str

    razorpay_order_id: str

    amount: float

    currency: str

    razorpay_key: str

    payment_status: str


class VerifyPaymentRequest(BaseModel):

    booking_reference: str

    razorpay_order_id: str

    razorpay_payment_id: str

    razorpay_signature: str


class VerifyPaymentResponse(BaseModel):

    booking_reference: str

    payment_status: str

    message: str
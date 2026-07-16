from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy.sql import func

from app.database import Base


class Payment(Base):
    """
    Razorpay Payment
    """

    __tablename__ = "payments"

    payment_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    booking_id = Column(
        Integer,
        ForeignKey("bookings.booking_id"),
        nullable=False
    )

    amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    currency = Column(
        String(10),
        default="INR"
    )

    razorpay_order_id = Column(
        String(100),
        unique=True
    )

    razorpay_payment_id = Column(
        String(100),
        unique=True
    )

    razorpay_signature = Column(
        String(255)
    )

    # payment_status = Column(
    #     Enum(PaymentStatus),
    #     default=PaymentStatus.PENDING
    # )

    payment_status = Column(
        String(50),
        nullable=False
    )

    payment_completed = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy.sql import func

from app.database import Base
from app.enums.booking_status import BookingStatus
from sqlalchemy import Enum


class Booking(Base):
    """
    Travel Booking
    """

    __tablename__ = "bookings"

    booking_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    booking_reference = Column(
        String(30),
        unique=True,
        nullable=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    provider = Column(
        String(50),
        nullable=False
    )

    travel_mode = Column(
        String(20),
        nullable=False
    )

    transport_name = Column(
        String(100),
        nullable=False
    )

    transport_number = Column(
        String(30)
    )

    source = Column(
        String(100),
        nullable=False
    )

    destination = Column(
        String(100),
        nullable=False
    )

    journey_date = Column(
        Date,
        nullable=False
    )

    departure_time = Column(
        String(20)
    )

    arrival_time = Column(
        String(20)
    )

    passengers = Column(
        Integer,
        nullable=False
    )

    total_amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    booking_status = Column(
        Enum(BookingStatus),
        default=BookingStatus.PENDING
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
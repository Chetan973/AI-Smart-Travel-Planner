"""Import all SQLAlchemy models so metadata is complete at startup."""

from .booking import Booking
from .otp import OTP
from .payment import Payment
from .user import User

__all__ = ["Booking", "OTP", "Payment", "User"]

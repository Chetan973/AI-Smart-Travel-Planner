from enum import Enum


class BookingStatus(str, Enum):
    PENDING = "PENDING"
    SEARCHING = "SEARCHING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"
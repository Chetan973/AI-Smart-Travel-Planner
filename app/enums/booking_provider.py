from enum import Enum


class BookingProvider(str, Enum):
    MAKEMYTRIP = "MAKEMYTRIP"
    REDBUS = "REDBUS"
    AGODA = "AGODA"
    IRCTC = "IRCTC"